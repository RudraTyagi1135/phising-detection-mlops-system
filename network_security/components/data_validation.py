import os
import sys
import warnings

import pandas as pd
from scipy.stats import ks_2samp

from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file

warnings.filterwarnings("ignore", category=DeprecationWarning)


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @property
    def required_columns(self) -> list[str]:
        columns = self._schema_config.get("columns", [])
        required_columns: list[str] = []
        for column in columns:
            if isinstance(column, dict):
                required_columns.extend(column.keys())
            else:
                required_columns.append(str(column))
        return required_columns

    def validate_no_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            required_columns = self.required_columns
            actual_columns = list(dataframe.columns)

            logging.info("Schema requires %s columns.", len(required_columns))
            logging.info("DataFrame contains %s columns.", len(actual_columns))

            missing_cols = set(required_columns) - set(actual_columns)
            extra_cols = set(actual_columns) - set(required_columns)

            if missing_cols or extra_cols:
                logging.error(
                    "Column validation failed. Missing: %s, Extra: %s",
                    missing_cols,
                    extra_cols,
                )
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05,
    ) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                if column not in current_df.columns:
                    logging.warning("Column %s missing in current dataset. Skipping drift check.", column)
                    continue

                d1 = base_df[column].dropna()
                d2 = current_df[column].dropna()

                if pd.api.types.is_numeric_dtype(d1):
                    ks_result = ks_2samp(d1, d2)
                    p_value = ks_result.pvalue
                    drift_detected = p_value < threshold
                else:
                    freq1 = d1.value_counts(normalize=True)
                    freq2 = d2.value_counts(normalize=True)
                    diff = sum(
                        abs(freq1.get(category, 0) - freq2.get(category, 0))
                        for category in set(freq1.index).union(freq2.index)
                    )
                    p_value = 1 - diff
                    drift_detected = diff > threshold

                if drift_detected:
                    status = False

                report[column] = {
                    "p_value": float(p_value),
                    "drift_detected": bool(drift_detected),
                }

            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path,
                content=report,
                replace=True,
            )
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_dataframe = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_dataframe = self.read_data(self.data_ingestion_artifact.test_file_path)

            valid_train = self.validate_no_of_columns(train_dataframe)
            valid_test = self.validate_no_of_columns(test_dataframe)

            if not (valid_train and valid_test):
                logging.error("Schema validation failed for one or both datasets.")
                return DataValidationArtifact(
                    validation_status=False,
                    valid_train_file_path=None,  # type: ignore[arg-type]
                    valid_test_file_path=None,  # type: ignore[arg-type]
                    invalid_train_file_path=(
                        self.data_ingestion_artifact.trained_file_path if not valid_train else None
                    ),  # type: ignore[arg-type]
                    invalid_test_file_path=(
                        self.data_ingestion_artifact.test_file_path if not valid_test else None
                    ),  # type: ignore[arg-type]
                    drift_report_file_path=self.data_validation_config.drift_report_file_path,
                )

            drift_status = self.detect_dataset_drift(
                base_df=train_dataframe,
                current_df=test_dataframe,
            )

            os.makedirs(
                os.path.dirname(self.data_validation_config.valid_train_file_path),
                exist_ok=True,
            )
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            return DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,  # type: ignore[arg-type]
                invalid_test_file_path=None,  # type: ignore[arg-type]
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

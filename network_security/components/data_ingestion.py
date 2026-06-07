import os
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.db.mongodb import get_mongo_collection
from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.entity.config_entity import DataIngestionConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
            if self.data_ingestion_config.source == "local":
                logging.info(
                    "Reading training data from local CSV: %s",
                    self.data_ingestion_config.local_data_file_path,
                )
                return pd.read_csv(self.data_ingestion_config.local_data_file_path)

            logging.info(
                "Reading training data from MongoDB collection %s.%s",
                self.data_ingestion_config.database_name,
                self.data_ingestion_config.collection_name,
            )
            collection = get_mongo_collection(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name,
                required=True,
            )
            dataframe = pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns:
                dataframe.drop(columns=["_id"], axis=1, inplace=True)

            dataframe.replace({"na": np.nan}, inplace=True)
            logging.info("Fetched %s rows for data ingestion", dataframe.shape[0])
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        try:
            stratify = dataframe[TARGET_COLUMN] if TARGET_COLUMN in dataframe.columns else None
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=self.data_ingestion_config.random_state,
                stratify=stratify,
            )
            logging.info("Performed train-test split on dataset")

            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True,
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True,
            )
            logging.info("Exported train-test split files successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            return DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)

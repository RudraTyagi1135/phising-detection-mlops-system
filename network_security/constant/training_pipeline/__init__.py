import os

import numpy as np

from network_security.config.settings import get_settings


settings = get_settings()

TARGET_COLUMN: str = settings.data.target_column
PIPELINE_NAME: str = settings.training.pipeline_name
ARTIFACT_DIR: str = str(settings.paths.artifact_dir)

FILE_NAME: str = settings.data.file_name
TRAIN_FILE_NAME: str = settings.data.train_file_name
TEST_FILE_NAME: str = settings.data.test_file_name
SCHEMA_FILE_PATH: str = str(settings.paths.schema_file_path)

SAVED_MODEL_DIR: str = str(settings.paths.saved_model_dir)
FINAL_MODEL_DIR: str = str(settings.paths.final_model_dir)
MODEL_FILE_NAME: str = settings.training.model_file_name
PREPROCESSOR_FILE_NAME: str = settings.training.preprocessor_file_name

DATA_INGESTION_COLLECTION_NAME: str = settings.mongodb.collection_name
DATA_INGESTION_DATABASE_NAME: str = settings.mongodb.database_name
DATA_INGESTION_SOURCE: str = settings.data.ingestion_source
DATA_INGESTION_LOCAL_DATA_FILE_PATH: str = str(settings.paths.local_dataset_path)

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = settings.data.train_test_split_ratio
DATA_INGESTION_RANDOM_STATE: int = settings.data.random_state

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_store"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"
PREPROCESSING_OBJECT_FILE_NAME: str = settings.training.preprocessor_file_name

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = settings.training.model_file_name
MODEL_TRAINER_EXPECTED_SCORE: float = settings.training.expected_score
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = (
    settings.training.overfitting_underfitting_threshold
)

FINAL_MODEL_FILE_PATH: str = os.path.join(FINAL_MODEL_DIR, MODEL_FILE_NAME)
FINAL_PREPROCESSOR_FILE_PATH: str = os.path.join(FINAL_MODEL_DIR, PREPROCESSOR_FILE_NAME)

# S3 is intentionally not used for ML artifact storage. The value remains for legacy
# cloud helpers only; model and dataset artifacts are versioned through DVC + DagsHub.
TRAINING_BUCKET_NAME: str = os.getenv("TRAINING_BUCKET_NAME", "")

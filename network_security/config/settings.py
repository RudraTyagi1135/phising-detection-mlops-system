from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def _load_dotenv() -> None:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)
    else:
        load_dotenv(override=False)


def _read_yaml(file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8") as file_obj:
        return yaml.safe_load(file_obj) or {}


def _get(config: dict[str, Any], key: str, default: Any = None) -> Any:
    value: Any = config
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]
    return value


def _env(name: str, default: Any = None, *aliases: str) -> Any:
    for candidate in (name, *aliases):
        value = os.getenv(candidate)
        if value not in (None, ""):
            return value
    return default


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _resolve_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


@dataclass(frozen=True)
class ApiSettings:
    host: str
    port: int
    cors_origins: list[str]


@dataclass(frozen=True)
class AppSettings:
    name: str
    environment: str
    training_endpoint_enabled: bool
    api: ApiSettings


@dataclass(frozen=True)
class PathSettings:
    artifact_dir: Path
    final_model_dir: Path
    saved_model_dir: Path
    prediction_output_dir: Path
    prediction_output_file_name: str
    templates_dir: Path
    static_dir: Path
    schema_file_path: Path
    local_dataset_path: Path
    log_dir: Path
    model_file_name: str
    preprocessor_file_name: str

    @property
    def final_model_file_path(self) -> Path:
        return self.final_model_dir / self.model_file_name

    @property
    def final_preprocessor_file_path(self) -> Path:
        return self.final_model_dir / self.preprocessor_file_name

    @property
    def prediction_output_file_path(self) -> Path:
        return self.prediction_output_dir / self.prediction_output_file_name


@dataclass(frozen=True)
class DataSettings:
    target_column: str
    file_name: str
    train_file_name: str
    test_file_name: str
    ingestion_source: str
    train_test_split_ratio: float
    random_state: int


@dataclass(frozen=True)
class MongoDBSettings:
    uri: str
    database_name: str
    collection_name: str
    prediction_log_collection_name: str
    max_pool_size: int
    server_selection_timeout_ms: int
    connect_timeout_ms: int
    socket_timeout_ms: int
    retry_attempts: int
    retry_sleep_seconds: float


@dataclass(frozen=True)
class TrainingSettings:
    pipeline_name: str
    expected_score: float
    overfitting_underfitting_threshold: float
    model_file_name: str
    preprocessor_file_name: str
    scoring_metric: str


@dataclass(frozen=True)
class MLflowSettings:
    tracking_uri: str
    experiment_name: str
    registered_model_name: str
    log_model: bool


@dataclass(frozen=True)
class DagsHubSettings:
    enabled: bool
    repo_owner: str
    repo_name: str
    token: str


@dataclass(frozen=True)
class DVCSettings:
    remote_name: str
    remote_url: str


@dataclass(frozen=True)
class AWSSettings:
    region: str
    ecr_repository_name: str


@dataclass(frozen=True)
class Settings:
    root_dir: Path
    config_path: Path
    app: AppSettings
    paths: PathSettings
    data: DataSettings
    mongodb: MongoDBSettings
    training: TrainingSettings
    mlflow: MLflowSettings
    dagshub: DagsHubSettings
    dvc: DVCSettings
    aws: AWSSettings
    log_level: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    _load_dotenv()

    config_path = _resolve_path(_env("CONFIG_PATH", DEFAULT_CONFIG_PATH))
    config = _read_yaml(config_path)

    dagshub_owner = str(_env("DAGSHUB_REPO_OWNER", _get(config, "dagshub.repo_owner", "")))
    dagshub_repo = str(_env("DAGSHUB_REPO_NAME", _get(config, "dagshub.repo_name", "")))
    dvc_remote_url = str(_env("DVC_REMOTE_URL", _get(config, "dvc.remote_url", "")))
    mlflow_tracking_uri = str(
        _env("MLFLOW_TRACKING_URI", _get(config, "mlflow.tracking_uri", ""))
    )

    if not dvc_remote_url and dagshub_owner and dagshub_repo:
        dvc_remote_url = f"https://dagshub.com/{dagshub_owner}/{dagshub_repo}.dvc"

    if not mlflow_tracking_uri and dagshub_owner and dagshub_repo:
        mlflow_tracking_uri = f"https://dagshub.com/{dagshub_owner}/{dagshub_repo}.mlflow"

    app_environment = str(_env("APP_ENV", _get(config, "app.environment", "development")))

    paths = PathSettings(
        artifact_dir=_resolve_path(_get(config, "paths.artifact_dir", "Artifacts")),
        final_model_dir=_resolve_path(_get(config, "paths.final_model_dir", "final_model")),
        saved_model_dir=_resolve_path(_get(config, "paths.saved_model_dir", "saved_models")),
        prediction_output_dir=_resolve_path(
            _get(config, "paths.prediction_output_dir", "prediction_output")
        ),
        prediction_output_file_name=str(
            _get(config, "paths.prediction_output_file_name", "output.csv")
        ),
        templates_dir=_resolve_path(_get(config, "paths.templates_dir", "templates")),
        schema_file_path=_resolve_path(_get(config, "paths.schema_file_path", "data_schema/schema.yaml")),
        local_dataset_path=_resolve_path(
            _env("LOCAL_DATA_FILE_PATH", _get(config, "paths.local_dataset_path", "network_data/phisingData.csv"))
        ),
        log_dir=_resolve_path(_get(config, "paths.log_dir", "logs")),
        model_file_name=str(_get(config, "training.model_file_name", "model.pkl")),
        preprocessor_file_name=str(
            _get(config, "training.preprocessor_file_name", "preprocessor.pkl")
        ),
    )

    api_settings = ApiSettings(
        host=str(_env("API_HOST", _get(config, "app.api.host", "0.0.0.0"))),
        port=_as_int(_env("API_PORT", _get(config, "app.api.port", 8000)), 8000),
        cors_origins=_as_list(_env("CORS_ORIGINS", _get(config, "app.api.cors_origins", ["*"]))),
    )

    return Settings(
        root_dir=PROJECT_ROOT,
        config_path=config_path,
        app=AppSettings(
            name=str(_get(config, "app.name", "phishing-detection-mlops-system")),
            environment=app_environment,
            training_endpoint_enabled=_as_bool(
                _env(
                    "TRAINING_ENDPOINT_ENABLED",
                    _get(config, "app.training_endpoint_enabled", True),
                ),
                default=True,
            ),
            api=api_settings,
        ),
        paths=paths,
        data=DataSettings(
            target_column=str(_get(config, "data.target_column", "Result")),
            file_name=str(_get(config, "data.file_name", "phisingData.csv")),
            train_file_name=str(_get(config, "data.train_file_name", "train.csv")),
            test_file_name=str(_get(config, "data.test_file_name", "test.csv")),
            ingestion_source=str(
                _env("DATA_INGESTION_SOURCE", _get(config, "data.ingestion_source", "local"))
            ).lower(),
            train_test_split_ratio=_as_float(
                _get(config, "data.train_test_split_ratio", 0.2), 0.2
            ),
            random_state=_as_int(_get(config, "data.random_state", 42), 42),
        ),
        mongodb=MongoDBSettings(
            uri=str(_env("MONGODB_URI", "", "MONGO_DB_URL")),
            database_name=str(
                _env("MONGODB_DATABASE", _get(config, "mongodb.database_name", "RUDRA1"))
            ),
            collection_name=str(
                _env("MONGODB_COLLECTION", _get(config, "mongodb.collection_name", "Network_data"))
            ),
            prediction_log_collection_name=str(
                _env(
                    "MONGODB_PREDICTION_LOG_COLLECTION",
                    _get(config, "mongodb.prediction_log_collection_name", "prediction_logs"),
                )
            ),
            max_pool_size=_as_int(
                _env("MONGODB_MAX_POOL_SIZE", _get(config, "mongodb.max_pool_size", 50)), 50
            ),
            server_selection_timeout_ms=_as_int(
                _env(
                    "MONGODB_SERVER_SELECTION_TIMEOUT_MS",
                    _get(config, "mongodb.server_selection_timeout_ms", 10000),
                ),
                10000,
            ),
            connect_timeout_ms=_as_int(
                _env("MONGODB_CONNECT_TIMEOUT_MS", _get(config, "mongodb.connect_timeout_ms", 10000)),
                10000,
            ),
            socket_timeout_ms=_as_int(
                _env("MONGODB_SOCKET_TIMEOUT_MS", _get(config, "mongodb.socket_timeout_ms", 10000)),
                10000,
            ),
            retry_attempts=_as_int(_get(config, "mongodb.retry_attempts", 3), 3),
            retry_sleep_seconds=_as_float(_get(config, "mongodb.retry_sleep_seconds", 2), 2),
        ),
        training=TrainingSettings(
            pipeline_name=str(_get(config, "pipeline.name", "NetworkSecurity")),
            expected_score=_as_float(_get(config, "training.expected_score", 0.6), 0.6),
            overfitting_underfitting_threshold=_as_float(
                _get(config, "training.overfitting_underfitting_threshold", 0.05), 0.05
            ),
            model_file_name=str(_get(config, "training.model_file_name", "model.pkl")),
            preprocessor_file_name=str(
                _get(config, "training.preprocessor_file_name", "preprocessor.pkl")
            ),
            scoring_metric=str(_get(config, "training.scoring_metric", "f1")),
        ),
        mlflow=MLflowSettings(
            tracking_uri=mlflow_tracking_uri,
            experiment_name=str(
                _env("MLFLOW_EXPERIMENT_NAME", _get(config, "mlflow.experiment_name", "phishing-detection"))
            ),
            registered_model_name=str(
                _env(
                    "MLFLOW_REGISTERED_MODEL_NAME",
                    _get(config, "mlflow.registered_model_name", "phishing-detection-model"),
                )
            ),
            log_model=_as_bool(_get(config, "mlflow.log_model", True), True),
        ),
        dagshub=DagsHubSettings(
            enabled=_as_bool(_get(config, "dagshub.enabled", True), True),
            repo_owner=dagshub_owner,
            repo_name=dagshub_repo,
            token=str(_env("DAGSHUB_TOKEN", "")),
        ),
        dvc=DVCSettings(
            remote_name=str(_get(config, "dvc.remote_name", "dagshub")),
            remote_url=dvc_remote_url,
        ),
        aws=AWSSettings(
            region=str(_env("AWS_REGION", _get(config, "aws.region", "us-east-1"))),
            ecr_repository_name=str(
                _env(
                    "ECR_REPOSITORY_NAME",
                    _get(config, "aws.ecr_repository_name", "phishing-detection-api"),
                )
            ),
        ),
        log_level=str(_env("LOG_LEVEL", "INFO")).upper(),
    )

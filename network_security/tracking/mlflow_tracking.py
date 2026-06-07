from __future__ import annotations

import os

import mlflow

from network_security.config.settings import Settings, get_settings
from network_security.logging.logger import logging


def configure_mlflow(settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    tracking_uri = settings.mlflow.tracking_uri

    if settings.dagshub.enabled and settings.dagshub.repo_owner and settings.dagshub.repo_name:
        os.environ.setdefault("MLFLOW_TRACKING_USERNAME", settings.dagshub.repo_owner)
        if settings.dagshub.token:
            os.environ.setdefault("MLFLOW_TRACKING_PASSWORD", settings.dagshub.token)
        tracking_uri = tracking_uri or (
            f"https://dagshub.com/{settings.dagshub.repo_owner}/"
            f"{settings.dagshub.repo_name}.mlflow"
        )

        try:
            import dagshub

            dagshub.init(
                repo_owner=settings.dagshub.repo_owner,
                repo_name=settings.dagshub.repo_name,
                mlflow=True,
            )
        except Exception as exc:
            logging.warning("DagsHub initialization skipped or failed: %s", exc)

    if not tracking_uri:
        tracking_uri = str(settings.root_dir / "mlruns")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(settings.mlflow.experiment_name)
    logging.info("MLflow tracking URI configured: %s", tracking_uri)
    return tracking_uri

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from network_security.config.settings import get_settings
from network_security.db.mongodb import get_mongo_collection
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


class PredictionLogger:
    def __init__(self):
        self.settings = get_settings()
        self.prediction_log_path = self.settings.paths.log_dir / "predictions.jsonl"
        self.prediction_log_path.parent.mkdir(parents=True, exist_ok=True)

    def _write_local(self, records: list[dict[str, Any]]) -> None:
        with self.prediction_log_path.open("a", encoding="utf-8") as file_obj:
            for record in records:
                file_obj.write(json.dumps(record, default=str) + "\n")

    def _write_mongodb(self, records: list[dict[str, Any]]) -> None:
        collection = get_mongo_collection(
            collection_name=self.settings.mongodb.prediction_log_collection_name,
            required=False,
        )
        if collection is None:
            return
        collection.insert_many(records)

    def log_batch(
        self,
        features: pd.DataFrame,
        predictions,
        source: str = "api",
    ) -> str:
        try:
            request_id = str(uuid.uuid4())
            timestamp = datetime.now(timezone.utc).isoformat()
            records: list[dict[str, Any]] = []

            for index, row in features.reset_index(drop=True).iterrows():
                records.append(
                    {
                        "request_id": request_id,
                        "source": source,
                        "created_at": timestamp,
                        "row_index": int(index),
                        "features": row.to_dict(),
                        "prediction": int(predictions[index]),
                    }
                )

            self._write_local(records)

            try:
                self._write_mongodb(records)
            except Exception as exc:
                logging.warning("Prediction MongoDB logging skipped: %s", exc)

            logging.info("Logged %s predictions with request_id=%s", len(records), request_id)
            return request_id

        except Exception as e:
            raise NetworkSecurityException(e, sys)

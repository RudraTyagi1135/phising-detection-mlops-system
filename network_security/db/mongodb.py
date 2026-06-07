from __future__ import annotations

import time
from typing import Any

import certifi
import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

from network_security.config.settings import MongoDBSettings, get_settings
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


def _client_kwargs(settings: MongoDBSettings) -> dict[str, Any]:
    return {
        "tlsCAFile": certifi.where(),
        "maxPoolSize": settings.max_pool_size,
        "serverSelectionTimeoutMS": settings.server_selection_timeout_ms,
        "connectTimeoutMS": settings.connect_timeout_ms,
        "socketTimeoutMS": settings.socket_timeout_ms,
        "retryReads": True,
        "retryWrites": True,
    }


def get_mongo_client(required: bool = True) -> pymongo.MongoClient:
    settings = get_settings().mongodb
    if not settings.uri:
        message = "MONGODB_URI is not configured."
        if required:
            raise NetworkSecurityException(RuntimeError(message), __import__("sys"))
        logging.warning(message)
        return None  # type: ignore[return-value]

    last_error: Exception | None = None
    for attempt in range(1, settings.retry_attempts + 1):
        try:
            client = pymongo.MongoClient(settings.uri, **_client_kwargs(settings))
            client.admin.command("ping")
            return client
        except Exception as exc:
            last_error = exc
            logging.warning("MongoDB connection attempt %s failed: %s", attempt, exc)
            if attempt < settings.retry_attempts:
                time.sleep(settings.retry_sleep_seconds)

    raise NetworkSecurityException(last_error or RuntimeError("MongoDB connection failed"), __import__("sys"))


def get_mongo_database(database_name: str | None = None, required: bool = True) -> Database:
    settings = get_settings().mongodb
    client = get_mongo_client(required=required)
    if client is None:
        return None  # type: ignore[return-value]
    return client[database_name or settings.database_name]


def get_mongo_collection(
    database_name: str | None = None,
    collection_name: str | None = None,
    required: bool = True,
) -> Collection:
    settings = get_settings().mongodb
    database = get_mongo_database(database_name=database_name, required=required)
    if database is None:
        return None  # type: ignore[return-value]
    return database[collection_name or settings.collection_name]


def check_mongodb_health(required: bool = False) -> dict[str, Any]:
    settings = get_settings().mongodb
    if not settings.uri:
        status = {"status": "skipped", "reason": "MONGODB_URI is not configured"}
        if required:
            raise NetworkSecurityException(RuntimeError(status["reason"]), __import__("sys"))
        return status

    try:
        client = get_mongo_client(required=True)
        server_info = client.server_info()
        return {
            "status": "ok",
            "database": settings.database_name,
            "collection": settings.collection_name,
            "version": server_info.get("version"),
        }
    except Exception as exc:
        if required:
            raise
        return {"status": "error", "reason": str(exc)}

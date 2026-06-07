import os
import pickle
import sys
from pathlib import Path

import numpy as np
import yaml
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


def read_yaml_file(file_path: str | Path) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file) or {}
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def write_yaml_file(file_path: str | Path, content: object, replace: bool = False) -> None:
    try:
        file_path = str(file_path)
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file_obj:
            yaml.dump(content, file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str | Path, array: np.ndarray) -> None:
    try:
        file_path = str(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array_data(file_path: str | Path) -> np.ndarray:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str | Path, obj: object) -> None:
    try:
        file_path = str(file_path)
        logging.info("Entered save_object")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited save_object")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_object(file_path: str | Path) -> object:
    try:
        file_path = str(file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file does not exist: {file_path}")

        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def evaluate_models(X_train, y_train, X_test, y_test, models, param) -> dict:
    try:
        report: dict[str, float] = {}

        for model_name, model in models.items():
            parameters = param.get(model_name, {})
            grid_search = GridSearchCV(
                estimator=model,
                param_grid=parameters,
                cv=3,
                scoring="f1",
                n_jobs=-1,
            )
            grid_search.fit(X_train, y_train)

            model.set_params(**grid_search.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = f1_score(y_test, y_test_pred)
            report[model_name] = float(test_model_score)

            logging.info(
                "Model candidate %s selected params=%s f1=%s",
                model_name,
                grid_search.best_params_,
                test_model_score,
            )

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)

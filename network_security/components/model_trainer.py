import os
import sys

import mlflow
import mlflow.sklearn
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

try:
    from xgboost import XGBClassifier
except ImportError:  # pragma: no cover - dependency is installed in production requirements
    XGBClassifier = None

from network_security.config.settings import get_settings
from network_security.constant.training_pipeline import FINAL_MODEL_FILE_PATH
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.tracking.mlflow_tracking import configure_mlflow
from network_security.utils.main_utils.utils import (
    evaluate_models,
    load_numpy_array_data,
    load_object,
    save_object,
)
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from network_security.utils.ml_utils.model.estimator import NetworkModel


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.settings = get_settings()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def _track_mlflow(
        self,
        best_model_name: str,
        best_model,
        train_metric,
        test_metric,
        model_artifact_path: str,
    ) -> None:
        tracking_uri = configure_mlflow(self.settings)
        logging.info("Tracking model training run in MLflow: %s", tracking_uri)

        with mlflow.start_run(run_name=f"{best_model_name}-training"):
            mlflow.log_param("best_model_name", best_model_name)
            mlflow.log_param("expected_score", self.model_trainer_config.expected_accuracy)
            mlflow.log_param("scoring_metric", self.settings.training.scoring_metric)

            mlflow.log_metric("train_f1_score", train_metric.f1_score)
            mlflow.log_metric("train_precision", train_metric.precision_score)
            mlflow.log_metric("train_recall", train_metric.recall_score)
            mlflow.log_metric("test_f1_score", test_metric.f1_score)
            mlflow.log_metric("test_precision", test_metric.precision_score)
            mlflow.log_metric("test_recall", test_metric.recall_score)

            mlflow.log_artifact(model_artifact_path, artifact_path="artifacts")
            mlflow.log_artifact(
                self.data_transformation_artifact.transformed_object_file_path,
                artifact_path="artifacts",
            )

            if self.settings.mlflow.log_model:
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    artifact_path="model",
                    registered_model_name=self.settings.mlflow.registered_model_name or None,
                )

    def train_model(self, X_train, y_train, x_test, y_test) -> ModelTrainerArtifact:
        try:
            models = {
                "Random Forest": RandomForestClassifier(random_state=self.settings.data.random_state),
                "Decision Tree": DecisionTreeClassifier(random_state=self.settings.data.random_state),
                "Gradient Boosting": GradientBoostingClassifier(
                    random_state=self.settings.data.random_state
                ),
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "AdaBoost": AdaBoostClassifier(random_state=self.settings.data.random_state),
            }
            params = {
                "Decision Tree": {
                    "criterion": ["gini", "entropy", "log_loss"],
                },
                "Random Forest": {
                    "n_estimators": [16, 32, 128],
                },
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.05, 0.01],
                    "subsample": [0.75, 0.9],
                    "n_estimators": [32, 64, 128],
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    "learning_rate": [0.1, 0.01],
                    "n_estimators": [32, 64, 128],
                },
            }

            if XGBClassifier is not None:
                models["XGBoost"] = XGBClassifier(
                    eval_metric="logloss",
                    random_state=self.settings.data.random_state,
                )
                params["XGBoost"] = {
                    "n_estimators": [64, 128],
                    "max_depth": [3, 5],
                    "learning_rate": [0.1, 0.05],
                }

            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=x_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            if best_model_score < self.model_trainer_config.expected_accuracy:
                raise RuntimeError(
                    f"Best model score {best_model_score} is below expected "
                    f"{self.model_trainer_config.expected_accuracy}"
                )

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(x_test)

            classification_train_metric = get_classification_score(
                y_true=y_train,
                y_pred=y_train_pred,
            )
            classification_test_metric = get_classification_score(
                y_true=y_test,
                y_pred=y_test_pred,
            )

            preprocessor = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )
            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)
            save_object(FINAL_MODEL_FILE_PATH, best_model)

            self._track_mlflow(
                best_model_name=best_model_name,
                best_model=best_model,
                train_metric=classification_train_metric,
                test_metric=classification_test_metric,
                model_artifact_path=self.model_trainer_config.trained_model_file_path,
            )

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )
            logging.info("Model trainer artifact: %s", model_trainer_artifact)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            return self.train_model(x_train, y_train, x_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

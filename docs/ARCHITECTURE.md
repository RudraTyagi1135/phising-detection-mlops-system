# Architecture Overview

## Training Flow

1. `main.py` starts `TrainingPipeline`.
2. Data ingestion reads from `DATA_INGESTION_SOURCE`:
   - `local`: `network_data/phisingData.csv`
   - `mongodb`: MongoDB Atlas database/collection from environment variables
3. Ingestion writes a timestamped feature-store snapshot under `Artifacts/<timestamp>/`.
4. Validation checks `data_schema/schema.yaml` and writes a drift report.
5. Transformation fits the KNN imputer and writes transformed arrays plus the preprocessor.
6. Training evaluates scikit-learn models and XGBoost when installed.
7. The best classifier is selected by F1 score.
8. Final model artifacts are written to `final_model/`.

## Experiment Flow

MLflow is configured by `network_security/tracking/mlflow_tracking.py`.

- If DagsHub settings are present, tracking URI becomes:
  `https://dagshub.com/<owner>/<repo>.mlflow`
- If DagsHub settings are missing, local runs are written to `mlruns/`.

Each training run logs:

- selected model name
- expected score
- train/test F1, precision, recall
- trained model artifact
- preprocessor artifact
- MLflow sklearn model

## Model Registry Flow

The trainer calls `mlflow.sklearn.log_model` with `MLFLOW_REGISTERED_MODEL_NAME`.

The default registered model name is:

```text
phishing-detection-model
```

DagsHub-backed MLflow is the intended registry target for portfolio and production usage.

## Artifact Flow

DVC tracks:

- `network_data/phisingData.csv`
- `final_model/model.pkl`
- `final_model/preprocessor.pkl`

DagsHub is the DVC remote. S3 is intentionally not used for model or dataset storage.

## Inference Flow

1. `app.py` exposes FastAPI.
2. `/predict` accepts a CSV upload.
3. The endpoint loads configured model artifacts from `final_model/`.
4. Predictions are appended to the output dataframe.
5. Output is written to `prediction_output/output.csv`.
6. Every prediction row is written to `logs/predictions.jsonl`.
7. If MongoDB is configured, prediction audit records are also inserted into Atlas.

## Deployment Flow

1. CI validates source, tests, DVC metadata, and Docker health.
2. CD pulls DVC artifacts from DagsHub.
3. CD builds a Docker image.
4. CD pushes the image to Amazon ECR.
5. CD renders the ECS task definition.
6. CD deploys to ECS Fargate.

## CI/CD Flow

```text
push / pull request
    -> Python dependency install
    -> Ruff critical lint
    -> project validation
    -> DVC metadata validation
    -> pytest
    -> docker build
    -> docker health check

main branch / manual deploy
    -> deployment secret validation
    -> DVC pull from DagsHub
    -> AWS auth
    -> ECR push
    -> ECS deploy
```

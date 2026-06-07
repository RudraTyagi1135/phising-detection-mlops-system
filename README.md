# Cloud-Native Phishing Detection MLOps System

Production-oriented phishing detection service with a modular ML pipeline, FastAPI inference,
Docker packaging, DVC/DagsHub artifact versioning, MLflow experiment tracking, MongoDB Atlas data
ingestion, and GitHub Actions CI/CD.

## Current Architecture

```text
Local CSV or MongoDB Atlas
        -> data ingestion
        -> schema validation and drift report
        -> preprocessing
        -> model selection and training
        -> MLflow tracking on DagsHub
        -> DVC-versioned dataset/model artifacts
        -> FastAPI batch prediction service
        -> Docker image
        -> GitHub Actions
        -> Amazon ECR + ECS Fargate
```

Model and dataset artifacts are versioned with DVC and stored through DagsHub. S3 is not used for
model storage.

## Repository Highlights

- `config.yaml` centralizes project configuration.
- `.env.example` documents all variables; `.env.development.example`, `.env.testing.example`,
  and `.env.production.example` provide environment-specific starting points.
- `network_security/db/mongodb.py` provides Atlas connection, retry, TLS, and health checks.
- `network_security/tracking/mlflow_tracking.py` configures local MLflow or DagsHub-backed MLflow.
- `network_security/monitoring/prediction_logger.py` logs every prediction locally and optionally to MongoDB.
- `.github/workflows/ci.yml` validates code, DVC metadata, tests, Docker build, and health checks.
- `.github/workflows/cd.yml` pulls DVC artifacts, builds/pushes ECR images, and deploys ECS.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.development.example .env
```

For local reproducible training without Atlas, keep:

```env
APP_ENV=development
DATA_INGESTION_SOURCE=local
```

Run validation:

```powershell
python scripts/validate_project.py
python scripts/check_dvc_setup.py
pytest -q
```

Run the API:

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Run training:

```powershell
python main.py
```

## Docker

```powershell
docker compose up --build api
docker compose --profile train run --rm trainer
```

API docs: `http://localhost:8000/docs`

## Required Accounts

- DagsHub repository for DVC remote storage and MLflow tracking.
- MongoDB Atlas cluster for production data ingestion and prediction audit storage.
- AWS account with ECR, ECS Fargate, IAM role for GitHub Actions, CloudWatch Logs, and Secrets Manager.

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Local Development Guide](docs/LOCAL_DEVELOPMENT.md)
- [Docker Guide](docs/DOCKER.md)
- [DVC, DagsHub, and MLflow Guide](docs/DVC_DAGSHUB_MLFLOW.md)
- [MongoDB Atlas Guide](docs/MONGODB_ATLAS.md)
- [AWS Deployment Guide](docs/AWS_DEPLOYMENT.md)
- [GitHub Actions Guide](docs/GITHUB_ACTIONS.md)

## Manual Tasks Still Required

1. Create the DagsHub repository and update `DVC_REMOTE_URL`, `DAGSHUB_REPO_OWNER`, and `DAGSHUB_REPO_NAME`.
2. Push current DVC artifacts with `dvc push` after DagsHub credentials are configured.
3. Create the MongoDB Atlas cluster/user/network access entry and set `MONGODB_URI`.
4. Create AWS ECR/ECS/IAM/Secrets Manager resources listed in `docs/AWS_DEPLOYMENT.md`.
5. Add GitHub repository secrets listed in `docs/GITHUB_ACTIONS.md`.

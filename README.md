# PhishGuard AI - Cloud-Native Phishing Detection MLOps System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-red)
![DVC](https://img.shields.io/badge/DVC-Data%20Versioning-purple)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-blue)
![AWS](https://img.shields.io/badge/AWS-ECR%20%7C%20ECS%20Fargate-yellow)

## Proprietary Project Notice

This repository is publicly visible for portfolio and educational review purposes only.

Unauthorized reuse, reproduction, modification, deployment, redistribution, or commercial usage of this project or its components is strictly prohibited.

**Copyright 2026 Rudra Tyagi. All Rights Reserved.**

---

# Project Overview

PhishGuard AI is a production-oriented phishing detection MLOps system that classifies URL/network-security feature records as phishing or legitimate.

The system combines:

- FastAPI inference services
- Modular ML training pipeline
- Schema validation and drift detection
- Scikit-learn and XGBoost model selection
- MLflow experiment tracking
- DVC and DagsHub artifact versioning
- MongoDB Atlas data ingestion and prediction audit logging
- Docker packaging
- GitHub Actions CI/CD
- AWS ECR and ECS Fargate deployment assets

to create an end-to-end phishing detection platform suitable for local development, reproducible training, and cloud deployment.

---

# Project Objective

The goal of PhishGuard AI is to provide a scalable phishing-risk classification service with reproducible ML lifecycle practices.

```text
URL / Network Feature Data
      |
Data Ingestion
      |
Schema Validation + Drift Detection
      |
Feature Imputation
      |
Model Selection + Training
      |
MLflow Tracking
      |
DVC-Versioned Artifacts
      |
FastAPI Batch Prediction
      |
Prediction Logging
      |
AWS-Ready Deployment
```

---

# Supported Predictions

| Prediction Type | Status |
| --- | --- |
| Phishing URL / malicious record detection | Supported |
| Legitimate URL / safe record detection | Supported |
| Batch CSV prediction | Supported |
| Prediction audit logging | Supported |

---

# Prediction Workflow

```text
CSV Upload from Web UI
            |
FastAPI /predict Route
            |
Target Column Removed if Present
            |
Saved Preprocessor Loaded
            |
Saved Classification Model Loaded
            |
Batch Predictions Generated
            |
Results Written to prediction_output/output.csv
            |
Predictions Logged to JSONL and optionally MongoDB
            |
HTML Result Table Rendered
            |
CSV Download Available from /download
```

---

# System Architecture

```text
Local CSV or MongoDB Atlas
            |
Data Ingestion Layer
            |
Data Validation Layer
            |
Data Transformation Layer
            |
Model Training Layer
            |
MLflow + DagsHub Tracking
            |
DVC Dataset and Model References
            |
FastAPI Application
            |
Frontend Templates and Static Assets
            |
Docker Container
            |
GitHub Actions
            |
Amazon ECR + ECS Fargate
```

Model and dataset artifacts are versioned with DVC and configured for DagsHub remote storage. S3 syncing support exists in the codebase, but the current model artifact workflow is DVC/DagsHub-focused.

---

# Architecture Breakdown

## Frontend Layer

### Technologies

- HTML
- CSS
- JavaScript
- Jinja2 templates

### Responsibilities

- CSV upload interface
- Prediction result rendering
- Batch summary display
- Download link for generated prediction output
- Static UI assets under `frontend/static`

---

## Backend Layer

### Technology

- FastAPI
- Uvicorn
- Jinja2Templates

### Responsibilities

- API routing
- CORS configuration
- Health checks
- Optional training endpoint
- Batch prediction orchestration
- Model and preprocessor loading
- Prediction output generation
- Prediction logging

Key routes:

| Route | Method | Responsibility |
| --- | --- | --- |
| `/` | GET | Render upload UI |
| `/health` | GET | Application and artifact health status |
| `/health/mongodb` | GET | Optional MongoDB connectivity check |
| `/train` | GET | Run training pipeline when enabled |
| `/predict` | POST | Run batch CSV prediction |
| `/download` | GET | Download latest prediction CSV |

---

## Data Layer

### Technologies

- Pandas
- MongoDB Atlas
- Local CSV datasets

### Responsibilities

- Load data from local CSV or MongoDB Atlas
- Export feature-store CSV artifacts
- Split train and test datasets
- Support reproducible local training through `DATA_INGESTION_SOURCE=local`
- Support Atlas-backed production ingestion through `DATA_INGESTION_SOURCE=mongodb`

---

## Machine Learning Layer

### Technologies

- Scikit-learn
- XGBoost
- NumPy
- Pandas

### Responsibilities

- Feature preprocessing with `KNNImputer`
- Classification model training
- Candidate model comparison with `GridSearchCV`
- F1-score based model selection
- Final model and preprocessor serialization
- Batch inference through the `NetworkModel` wrapper

---

## Validation and Monitoring Layer

### Technologies

- PyYAML
- SciPy KS test
- JSONL logging
- MongoDB prediction-log collection

### Responsibilities

- Validate dataset columns against `data_schema/schema.yaml`
- Detect train/test drift
- Write drift reports to training artifacts
- Log every prediction request locally to `logs/predictions.jsonl`
- Optionally persist prediction logs to MongoDB Atlas

---

## MLOps and Deployment Layer

### Technologies

- DVC
- DagsHub
- MLflow
- Docker
- GitHub Actions
- AWS ECR
- AWS ECS Fargate
- AWS Secrets Manager

### Responsibilities

- Version datasets and final model artifacts
- Track training experiments and model metrics
- Build and health-check Docker images
- Validate project structure in CI
- Deploy container images to AWS ECS Fargate
- Keep credentials externalized through environment variables and cloud secrets

---

# Core Features

## Phishing Detection

Classifies network-security feature rows into phishing or legitimate outcomes using supervised classification models.

---

## Batch CSV Prediction

The `/predict` endpoint accepts CSV uploads, runs inference over all rows, adds a `predicted_column`, and stores the result in:

```text
prediction_output/output.csv
```

---

## Modular Training Pipeline

The training pipeline is split into separate components:

- Data ingestion
- Data validation
- Data transformation
- Model training
- MLflow tracking
- Artifact persistence

---

## Schema Validation

The project validates incoming training data against:

```text
data_schema/schema.yaml
```

The schema currently defines 30 phishing-related numeric features plus the `Result` target column.

---

## Dataset Drift Detection

Training and test splits are compared during validation. Numeric columns use the Kolmogorov-Smirnov test, while non-numeric columns use normalized distribution differences.

---

## Model Selection

The trainer evaluates multiple classifier families and selects the model with the best F1 score.

Supported candidates include:

- Random Forest
- Decision Tree
- Gradient Boosting
- Logistic Regression
- AdaBoost
- XGBoost, when installed

---

## Experiment Tracking

Training runs log parameters, metrics, and artifacts to MLflow. When DagsHub settings are configured, MLflow tracking is routed to the DagsHub repository.

---

## Prediction History

Every prediction row is logged with:

- Request ID
- Timestamp
- Source
- Row index
- Input features
- Prediction

Logs are written locally and optionally inserted into MongoDB Atlas.

---

# Project Structure

```text
phising-detection-mlops-system/
|
|-- app.py
|-- main.py
|-- push_data.py
|-- config.yaml
|-- requirements.txt
|-- setup.py
|-- pyproject.toml
|-- Dockerfile
|-- docker-compose.yml
|-- dvc_workflow.txt
|
|-- .github/
|   |-- workflows/
|       |-- ci.yml
|       |-- cd.yml
|
|-- data_schema/
|   |-- schema.yaml
|
|-- demo_data/
|   |-- recruiter_demo.csv
|
|-- deploy/
|   |-- aws/
|       |-- ecs-task-definition.json
|
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- AWS_DEPLOYMENT.md
|   |-- DOCKER.md
|   |-- DVC_DAGSHUB_MLFLOW.md
|   |-- GITHUB_ACTIONS.md
|   |-- LOCAL_DEVELOPMENT.md
|   |-- MONGODB_ATLAS.md
|
|-- final_model/
|   |-- model.pkl.dvc
|   |-- preprocessor.pkl.dvc
|
|-- frontend/
|   |-- templates/
|   |   |-- index.html
|   |   |-- table.html
|   |-- static/
|       |-- css/
|       |-- js/
|
|-- network_data/
|   |-- phisingData.csv.dvc
|
|-- network_security/
|   |-- cloud/
|   |-- components/
|   |-- config/
|   |-- constant/
|   |-- db/
|   |-- entity/
|   |-- exception/
|   |-- logging/
|   |-- monitoring/
|   |-- pipeline/
|   |-- tracking/
|   |-- utils/
|
|-- scripts/
|   |-- check_dvc_setup.py
|   |-- validate_project.py
|   |-- validate_secrets.py
|
|-- tests/
|   |-- test_api_health.py
|   |-- test_config.py
|   |-- test_dvc_metadata.py
|   |-- test_fetch_data.py
|   |-- test_mongodb.py
```

---

# Machine Learning Design

## Feature Schema

The model expects phishing-detection feature columns such as:

- `having_IP_Address`
- `URL_Length`
- `Shortining_Service`
- `having_At_Symbol`
- `SSLfinal_State`
- `Domain_registeration_length`
- `HTTPS_token`
- `URL_of_Anchor`
- `web_traffic`
- `Page_Rank`
- `Google_Index`
- `Statistical_report`

The target column is:

```text
Result
```

During transformation, `Result = -1` is normalized to `0`.

## Pipeline Components

| Component | Responsibility |
| --- | --- |
| `data_ingestion.py` | Read local or MongoDB data, write feature store, split train/test |
| `data_validation.py` | Validate schema and generate drift report |
| `data_transformation.py` | Apply KNN imputation and persist transformed arrays |
| `model_trainer.py` | Train candidate models, select best F1 model, log MLflow run |
| `training_pipeline.py` | Orchestrate end-to-end training |
| `estimator.py` | Wrap preprocessor and model for prediction |
| `prediction_logger.py` | Log prediction records locally and optionally to MongoDB |
| `settings.py` | Load `config.yaml` and environment overrides |

---

# Experiment Tracking and Artifact Versioning

PhishGuard AI uses MLflow for training visibility and DVC for reproducibility.

Tracked training outputs include:

- Best model name
- Expected score
- Scoring metric
- Train F1, precision, and recall
- Test F1, precision, and recall
- Serialized model artifact
- Serialized preprocessing artifact

DVC-tracked artifacts include:

```text
network_data/phisingData.csv
final_model/model.pkl
final_model/preprocessor.pkl
```

The repository includes `.dvc` pointer files for these assets, so the real dataset and model binaries can be pulled from the configured DVC remote.

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>
cd phising-detection-mlops-system
```

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 4. Configure Environment Variables

Create a local `.env` from the example file.

### Windows

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Important variables:

```env
APP_ENV=development
DATA_INGESTION_SOURCE=local
LOCAL_DATA_FILE_PATH=network_data/phisingData.csv
MONGODB_URI=your_mongodb_atlas_uri
DAGSHUB_REPO_OWNER=your_dagshub_username_or_org
DAGSHUB_REPO_NAME=phising-detection-mlops-system
DAGSHUB_TOKEN=your_dagshub_token
MLFLOW_TRACKING_URI=your_mlflow_tracking_uri
API_HOST=0.0.0.0
API_PORT=8000
TRAINING_ENDPOINT_ENABLED=true
```

## 5. Pull DVC Artifacts

After configuring the DVC remote and credentials:

```bash
dvc pull
```

## 6. Validate Project

```bash
python scripts/validate_project.py
python scripts/check_dvc_setup.py
pytest -q
```

## 7. Run Training

```bash
python main.py
```

Training can also be triggered from the API when `TRAINING_ENDPOINT_ENABLED=true`:

```text
GET /train
```

## 8. Run Application

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Application URLs:

```text
Web UI: http://localhost:8000
API docs: http://localhost:8000/docs
Health: http://localhost:8000/health
MongoDB health: http://localhost:8000/health/mongodb
```

---

# Docker

## Build and Run API

```bash
docker compose up --build api
```

## Build Image Directly

```bash
docker build -t phishguard-ai:local .
docker run --env-file .env -p 8000:8000 phishguard-ai:local
```

The container exposes port `8000` and includes a `/health` health check.

---

# Future Roadmap

## Short-Term

- Complete and wire the standalone `batch_prediction.py` pipeline module
- Add richer API request validation for uploaded CSV files
- Add model performance reports to the UI
- Add automated DVC artifact pull checks before application startup
- Add more tests around prediction logging and training pipeline behavior

## Long-Term

- Add Airflow orchestration for scheduled retraining
- Add SageMaker training and model registry integration
- Add AWS S3 data lake support where required
- Add model monitoring dashboards
- Add drift-triggered retraining workflows
- Add blue/green or canary deployment on ECS
- Add authentication and authorization for training/admin endpoints

---

# Technology Stack

| Layer | Technologies |
| --- | --- |
| Backend | FastAPI, Uvicorn, Jinja2 |
| ML | Scikit-learn, XGBoost, NumPy, Pandas |
| Validation | PyYAML, SciPy KS test |
| Database | MongoDB Atlas |
| Tracking | MLflow, DagsHub |
| Versioning | DVC |
| Frontend | HTML, CSS, JavaScript |
| Packaging | setuptools, pyproject.toml |
| Testing | pytest |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS ECR, ECS Fargate, Secrets Manager |

---

# Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Local Development Guide](docs/LOCAL_DEVELOPMENT.md)
- [Docker Guide](docs/DOCKER.md)
- [DVC, DagsHub, and MLflow Guide](docs/DVC_DAGSHUB_MLFLOW.md)
- [MongoDB Atlas Guide](docs/MONGODB_ATLAS.md)
- [AWS Deployment Guide](docs/AWS_DEPLOYMENT.md)
- [GitHub Actions Guide](docs/GITHUB_ACTIONS.md)

---

# Screenshots

```markdown
![Upload UI](images/upload-ui.png)

![Prediction Results](images/prediction-results.png)

![MLflow Experiment](images/mlflow-experiment.png)

![AWS Deployment](images/aws-deployment.png)
```

---

# Author

**Rudra Tyagi**

### Focus Areas

- ML Systems
- MLOps
- Cloud-Native AI Infrastructure
- Cybersecurity AI
- Production ML Deployment

---

# Recruiter Notes

This project demonstrates:

- End-to-end ML system design
- Phishing detection classification workflow
- FastAPI backend development
- Modular ML pipeline architecture
- Data validation and drift detection
- MLflow experiment tracking
- DVC dataset and model versioning
- MongoDB Atlas integration
- Prediction audit logging
- Dockerized deployment workflow
- GitHub Actions CI/CD
- AWS ECR and ECS Fargate deployment planning

---

# Manual Tasks Still Required

1. Create the DagsHub repository and update `DVC_REMOTE_URL`, `DAGSHUB_REPO_OWNER`, and `DAGSHUB_REPO_NAME`.
2. Push or pull current DVC artifacts after DagsHub credentials are configured.
3. Create the MongoDB Atlas cluster, database user, network access entry, and set `MONGODB_URI`.
4. Create AWS ECR, ECS, IAM, CloudWatch, and Secrets Manager resources listed in `docs/AWS_DEPLOYMENT.md`.
5. Add GitHub repository secrets listed in `docs/GITHUB_ACTIONS.md`.

---

# License

This repository is proprietary software.

Unauthorized copying, modification, distribution, deployment, or commercial use is prohibited.

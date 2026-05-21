# Production-Ready Phishing Detection ML Pipeline

A cloud-native machine learning system for phishing website detection using modular ML pipelines, FastAPI inference services, MongoDB ingestion, MLflow experiment tracking, Dockerized deployment, and AWS-oriented infrastructure.

## Key Highlights

- End-to-end ML pipeline architecture
- MongoDB-backed ingestion pipeline
- Modular training workflow
- MLflow + DagsHub experiment tracking
- FastAPI inference API
- Dockerized deployment
- AWS deployment ready
- Artifact versioning support
- Schema validation + drift detection

## Overview

This repository implements a modular machine learning workflow for classifying phishing vs. legitimate website records. The project is organized into clear stages:

- `data -> validation -> transformation -> training -> serving`
- raw data can be loaded into MongoDB and exported into the training pipeline
- trained artifacts are stored locally and can be synced to S3
- predictions can be served through a FastAPI application

The current implementation is built around a phishing dataset with engineered tabular features such as URL length, HTTPS token usage, page rank, DNS record presence, and related indicators.

## Features

- Modular package structure under `network_security/`
- MongoDB-based ingestion source
- Schema-based dataset validation using `data_schema/schema.yaml`
- Missing-value handling with `KNNImputer`
- Multiple candidate classifiers with hyperparameter search
- FastAPI endpoint for training and batch-style CSV prediction
- HTML table rendering for prediction results
- Artifact generation for each pipeline run
- Optional S3 sync for artifacts and final model directory
- Dockerfile and GitHub Actions workflow for AWS/ECR deployment

## Project Structure

```text
etl_ml_project/
├── app.py                              # FastAPI app for training + prediction
├── main.py                             # Standalone local pipeline runner
├── push_data.py                        # CSV -> MongoDB loader
├── Dockerfile                          # Container build definition
├── requirements.txt                    # Python dependencies
├── setup.py                            # Package setup
├── data_schema/
│   └── schema.yaml                     # Expected dataset schema
├── network_data/
│   └── phisingData.csv                 # Source dataset sample
├── final_model/
│   ├── model.pkl                       # Saved trained model
│   └── preprocessor.pkl                # Saved preprocessing object
├── prediction_output/
│   └── output.csv                      # Last prediction output
├── templates/
│   └── table.html                      # Prediction result template
└── network_security/
    ├── cloud/                          # S3 sync utility
    ├── components/                     # Data ingestion/validation/transformation/training
    ├── constant/                       # Pipeline constants
    ├── entity/                         # Config and artifact entities
    ├── exception/                      # Custom exception class
    ├── logging/                        # Logging setup
    ├── pipeline/                       # Training pipeline orchestration
    └── utils/                          # YAML, serialization, metrics, model wrapper
```

## Tech Stack

- Backend: FastAPI, Uvicorn
- ML: scikit-learn
- Data: pandas, NumPy, MongoDB
- Tracking: MLflow, DagsHub
- Infra target: AWS S3, ECR, EC2
- Packaging: Docker, setuptools

## Architecture

### 1. Data Ingestion

`network_security/components/data_ingestion.py`

- connects to MongoDB using `MONGO_DB_URL`
- reads the configured collection
- removes MongoDB `_id`
- stores a feature-store CSV snapshot
- splits the dataset into train and test CSV files

### 2. Data Validation

`network_security/components/data_validation.py`

- validates dataset column count against `data_schema/schema.yaml`
- compares train vs. test distributions for drift detection
- writes a drift report as YAML
- writes validated datasets to the validation artifact directory

### 3. Data Transformation

`network_security/components/data_transformation.py`

- separates features and target
- normalizes target label `-1 -> 0`
- applies a `KNNImputer` preprocessing pipeline
- saves transformed NumPy arrays
- saves the fitted preprocessing object

### 4. Model Training

`network_security/components/model_trainer.py`

- trains several candidate estimators:
  - Random Forest
  - Decision Tree
  - Gradient Boosting
  - Logistic Regression
  - AdaBoost
- performs hyperparameter search
- computes classification metrics
- stores the selected model artifact
- logs metrics to MLflow/DagsHub

### 5. Model Serving

`app.py`

- `GET /` redirects to Swagger UI
- `GET /train` triggers the training pipeline
- `POST /predict` accepts a CSV file, loads saved artifacts, generates predictions, writes `prediction_output/output.csv`, and renders an HTML table

## Configuration

The current codebase uses:

- environment variables for secrets and connection details
- constants from `network_security/constant/training_pipeline/__init__.py`
- schema from `data_schema/schema.yaml`

### Required Environment Variables

Create a `.env` file in the project root:

```env
MONGO_DB_URL=<your-mongodb-connection-string>
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
AWS_REGION=us-east-1
```

If you use GitHub Actions deployment, also configure these repository secrets:

```env
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ECR_LOGIN_URI
ECR_REPOSITORY_NAME
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd etl_ml_project
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

## Data Loading

If your MongoDB collection is empty, populate it from the bundled CSV:

```bash
python push_data.py
```

This loads `network_data/phisingData.csv` into:

- database: `RUDRA1`
- collection: `Network_data`

## Running the Project

### Option 1: Run the training pipeline directly

```bash
python main.py
```

This runs:

- data ingestion
- data validation
- data transformation
- model training

Artifacts are written under the timestamped `Artifacts/` directory.

### Option 2: Run the FastAPI app

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open:

- Swagger UI: `http://localhost:8000/docs`

### Trigger training via API

```http
GET /train
```

### Run prediction via API

```http
POST /predict
Content-Type: multipart/form-data
file=<csv file>
```

The API:

- loads `final_model/preprocessor.pkl`
- loads `final_model/model.pkl`
- appends predictions to the uploaded dataset
- writes `prediction_output/output.csv`
- returns an HTML table response

## AWS and Deployment

### Docker

Build the image:

```bash
docker build -t network-security .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 network-security
```

### GitHub Actions

The repository includes `.github/workflows/main.yml` that:

- runs a placeholder CI stage
- builds and pushes a Docker image to Amazon ECR
- deploys on a self-hosted runner

### S3 Artifact Sync

The training pipeline can sync:

- pipeline artifacts to `s3://<bucket>/artifact/<timestamp>`
- final model directory to `s3://<bucket>/final_model/<timestamp>`

Bucket name is currently defined in:

- `network_security/constant/training_pipeline/__init__.py`

## Schema

The expected dataset schema is defined in:

- `data_schema/schema.yaml`

The target column is:

- `Result`

Feature values are currently integer-encoded based on the phishing dataset used by the project.

## Logging

Logs are written to:

```text
logs/<timestamp>.log
```

The custom exception and logger utilities are located in:

- `network_security/exception/exception.py`
- `network_security/logging/logger.py`

## Testing

Current repository test files are lightweight connectivity scripts:

- `test_fetch_data.py`
- `test_mongodb.py`

They are not a full automated test suite yet. Before production use, add:

- unit tests for each pipeline component
- API tests for `/train` and `/predict`
- regression tests for saved model compatibility

## Known Gaps

These are important if you plan to productionize the repository:

- runtime configuration is split across constants and env vars instead of a centralized `config.yaml`
- prediction logging is currently a local CSV overwrite, not an append-only audit log
- CI steps are placeholders and do not run real linting or tests
- deployment settings should be reviewed to keep API port, Docker command, and runtime entrypoint aligned
- secrets must never be hardcoded in utility or test files

## Suggested Next Improvements

- introduce a real `config.yaml` and config loader
- add structured prediction logging to a database or S3
- replace `os.system` AWS sync calls with `subprocess` plus error handling
- add Pydantic request/response contracts for inference
- add proper pytest coverage
- make Docker start the FastAPI app explicitly
- add model registry/versioning around `final_model/`

## Author

Rudra Tyagi


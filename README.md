# Cloud-Native Phishing Detection MLOps System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![MLflow](https://img.shields.io/badge/MLflow-ExperimentTracking-purple)

A production-oriented phishing website detection system designed to demonstrate modular ML pipeline engineering, experiment tracking, API-based inference, Dockerized deployment, and AWS-compatible MLOps workflows.

---

# Problem Statement

Phishing websites remain one of the most common cybersecurity threats, exploiting users through deceptive URLs, fake domains, and malicious web structures.

This project was built to explore how production-oriented machine learning systems can be designed for phishing detection using:

- modular ML pipelines
- schema validation
- experiment tracking
- API-based inference
- cloud-ready deployment workflows
- artifact versioning and reproducibility

The system focuses not only on model training, but also on engineering reliable ML infrastructure components.

---

# Key Features

- End-to-end ML pipeline architecture
- MongoDB-backed data ingestion
- Schema-based dataset validation
- Data drift detection workflow
- Modular preprocessing pipeline
- Multiple model training and evaluation
- MLflow + DagsHub experiment tracking
- FastAPI inference service
- Dockerized deployment
- AWS deployment workflow support
- S3 artifact synchronization
- Modular and scalable project structure

---

# System Architecture

> Add your architecture diagram here

```text
MongoDB / CSV Dataset
            ↓
     Data Ingestion
            ↓
     Data Validation
            ↓
   Data Transformation
            ↓
      Model Training
            ↓
 MLflow Experiment Tracking
            ↓
      Model Artifacts
            ↓
      FastAPI Service
            ↓
 Docker Containerization
            ↓
 AWS Deployment Pipeline
```

---

# Tech Stack

| Category | Technologies |
|---|---|
| Backend | FastAPI, Uvicorn |
| Machine Learning | scikit-learn |
| Data Processing | pandas, NumPy |
| Database | MongoDB |
| Experiment Tracking | MLflow, DagsHub |
| Cloud Services | AWS S3, AWS ECR, EC2 |
| Deployment | Docker, GitHub Actions |
| Packaging | setuptools |

---

# Engineering Highlights

- Modular ML pipeline design
- Schema-driven validation workflow
- Drift detection support
- Reusable preprocessing pipeline
- Experiment tracking integration
- Dockerized inference service
- Cloud-compatible artifact management
- Separation of training and serving workflows
- Reproducible pipeline execution

---

# Pipeline Workflow

## 1. Data Ingestion

Location:

```text
network_security/components/data_ingestion.py
```

Responsibilities:

- Connects to MongoDB
- Reads configured collections
- Removes MongoDB `_id`
- Creates feature-store snapshots
- Splits train and test datasets

---

## 2. Data Validation

Location:

```text
network_security/components/data_validation.py
```

Responsibilities:

- Validates dataset schema
- Detects train/test drift
- Generates validation reports
- Stores validated artifacts

---

## 3. Data Transformation

Location:

```text
network_security/components/data_transformation.py
```

Responsibilities:

- Feature-target separation
- Missing value handling using `KNNImputer`
- Target normalization
- Transformation artifact generation
- Preprocessor serialization

---

## 4. Model Training

Location:

```text
network_security/components/model_trainer.py
```

Models Evaluated:

- Random Forest
- Decision Tree
- Gradient Boosting
- Logistic Regression
- AdaBoost

Responsibilities:

- Hyperparameter tuning
- Model evaluation
- Metric logging
- MLflow experiment tracking
- Model artifact generation

---

## 5. Model Serving

Location:

```text
app.py
```

API Endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Redirects to Swagger UI |
| `/train` | GET | Triggers training pipeline |
| `/predict` | POST | Performs batch CSV inference |

The inference pipeline:

- loads serialized preprocessing artifacts
- loads trained model artifacts
- generates predictions
- exports prediction outputs
- renders HTML prediction tables

---

# Repository Structure

```text
phishing-detection-mlops-system/
│
├── app.py
├── main.py
├── push_data.py
├── Dockerfile
├── requirements.txt
├── setup.py
│
├── data_schema/
│   └── schema.yaml
│
├── network_data/
│   └── phisingData.csv
│
├── templates/
│   └── table.html
│
├── network_security/
│   ├── cloud/
│   ├── components/
│   ├── constant/
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── pipeline/
│   └── utils/
│
└── .github/
    └── workflows/
```

---

# Model Performance

> Replace with your actual metrics

| Metric | Score |
|---|---|
| Accuracy | XX% |
| Precision | XX% |
| Recall | XX% |
| F1 Score | XX% |

Best Performing Model: `Gradient Boosting`

---

# Configuration

The project currently uses:

- environment variables
- schema-driven validation
- pipeline constants
- AWS deployment configuration

---

# Environment Variables

Create a `.env` file:

```env
MONGO_DB_URL=<your-mongodb-connection-string>

AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_REGION=us-east-1
```

For GitHub Actions deployment:

```env
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_ECR_LOGIN_URI
ECR_REPOSITORY_NAME
```

---

# Local Setup

## Clone Repository

```bash
git clone <your-repository-url>
cd phishing-detection-mlops-system
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

### Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

---

# Data Loading

Populate MongoDB from the provided dataset:

```bash
python push_data.py
```

Dataset Source:

```text
network_data/phisingData.csv
```

MongoDB Target:

- Database: `RUDRA1`
- Collection: `Network_data`

---

# Running the Training Pipeline

```bash
python main.py
```

Pipeline stages executed:

- Data Ingestion
- Data Validation
- Data Transformation
- Model Training

Generated artifacts are stored in:

```text
Artifacts/
```

---

# Running the FastAPI Service

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# API Usage

## Trigger Training

```http
GET /train
```

---

## Batch Prediction

```http
POST /predict
Content-Type: multipart/form-data
```

Upload a CSV file for prediction inference.

Prediction outputs are exported to:

```text
prediction_output/output.csv
```

---

# Docker Deployment

## Build Docker Image

```bash
docker build -t phishing-detection-system .
```

---

## Run Docker Container

```bash
docker run --env-file .env -p 8000:8000 phishing-detection-system
```

---

# AWS Deployment Workflow

The repository includes GitHub Actions workflows for:

- Docker image build
- Amazon ECR push
- AWS deployment automation

AWS Services Used:

- Amazon ECR
- Amazon S3
- Amazon EC2

---

# Artifact Management

The pipeline supports optional S3 synchronization for:

- training artifacts
- final trained models
- pipeline outputs

Example structure:

```text
s3://bucket-name/artifacts/<timestamp>
s3://bucket-name/final_model/<timestamp>
```

---

# Logging

Logs are generated under:

```text
logs/<timestamp>.log
```

Custom logging and exception handling utilities:

```text
network_security/logging/logger.py
network_security/exception/exception.py
```

---

# Current Limitations

This repository is currently evolving toward a more production-grade MLOps architecture.

Known gaps include:

- centralized configuration management
- automated CI quality checks
- complete pytest coverage
- model registry integration
- monitoring and observability
- append-only prediction audit logging

---

# Future Improvements

Planned enhancements:

- Kubernetes deployment
- Terraform infrastructure provisioning
- centralized config management
- model registry integration
- monitoring dashboards
- CI/CD quality gates
- real-time inference pipeline
- structured prediction logging
- advanced testing coverage

---

# Repository Status

Current Status: Active Development

This repository is continuously being improved to better reflect production-oriented ML systems engineering practices.

---

# Maintainer

Rudra Tyagi

Focus Areas:

- AWS ML Engineering
- MLOps Systems
- Cloud-Native ML Infrastructure
- Machine Learning Deployment

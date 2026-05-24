# 🛡️ Cloud-Native Phishing Detection MLOps System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge&logo=docker)
![AWS](https://img.shields.io/badge/AWS-Cloud-orange?style=for-the-badge&logo=amazonaws)
![MLflow](https://img.shields.io/badge/MLflow-Experiment_Tracking-purple?style=for-the-badge)
![MLOps](https://img.shields.io/badge/MLOps-Production_Architecture-red?style=for-the-badge)

</p>

---

# 📌 Project Overview

The **Cloud-Native Phishing Detection MLOps System** is a production-oriented machine learning platform designed for phishing website detection using modular MLOps architecture principles.

The project focuses not only on machine learning model training, but also on building a scalable and deployable ML infrastructure including:

- modular ML pipelines
- schema validation
- experiment tracking
- FastAPI inference serving
- Dockerized deployment
- AWS-compatible workflows
- artifact versioning
- reproducible ML engineering

---

# 🎯 Problem Statement

Phishing websites remain one of the most common cybersecurity threats.

Attackers exploit:
- fake domains
- malicious URLs
- deceptive website structures
- fraudulent redirects

to steal:
- credentials
- financial information
- user identity data

This project explores how modern MLOps systems can be designed to detect phishing websites using cloud-native machine learning workflows.

---

# 🧠 System Objective

The platform was designed to demonstrate:

```text
Raw Dataset
        ↓
ML Pipeline Engineering
        ↓
Experiment Tracking
        ↓
Artifact Management
        ↓
FastAPI Inference
        ↓
Docker Deployment
        ↓
AWS-Compatible MLOps Infrastructure
```

The primary engineering focus is:
- reproducibility
- modularity
- deployability
- scalable ML architecture

---

# ✨ Core Features

## ⚙️ End-to-End ML Pipeline

Supports:
- ingestion
- validation
- transformation
- training
- evaluation
- deployment workflows

---

## 🗄️ MongoDB Data Ingestion

The system supports:
- MongoDB-backed ingestion
- dataset snapshot creation
- feature-store generation

---

## 📊 Schema-Based Validation

Includes:
- schema enforcement
- train/test validation
- data drift detection

---

## 🧠 Modular ML Training

Evaluates multiple models:
- Random Forest
- Decision Tree
- Gradient Boosting
- Logistic Regression
- AdaBoost

---

## 📈 MLflow + DagsHub Tracking

Supports:
- experiment tracking
- metric logging
- artifact logging
- reproducibility workflows

---

## 🌐 FastAPI Inference Service

Provides:
- API-based prediction serving
- Swagger UI
- batch CSV inference

---

## 🐳 Dockerized Deployment

Supports:
- containerized inference
- reproducible deployment environments

---

## ☁️ AWS-Compatible Architecture

Designed for:
- Amazon S3
- Amazon ECR
- Amazon EC2
- GitHub Actions deployment workflows

---

# 🏗️ System Architecture

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

# ⚙️ Architecture Breakdown

---

# 📥 Data Ingestion Layer

Location:

```text
network_security/components/data_ingestion.py
```

Responsibilities:
- MongoDB ingestion
- dataset extraction
- `_id` removal
- train/test splitting
- feature-store snapshot generation

---

# 🧪 Data Validation Layer

Location:

```text
network_security/components/data_validation.py
```

Responsibilities:
- schema validation
- drift detection
- validation reporting
- artifact storage

---

# ⚙️ Data Transformation Layer

Location:

```text
network_security/components/data_transformation.py
```

Responsibilities:
- feature-target separation
- missing value handling
- KNN imputation
- preprocessing artifact generation
- serialization workflows

---

# 🤖 Model Training Layer

Location:

```text
network_security/components/model_trainer.py
```

Responsibilities:
- model training
- hyperparameter tuning
- metric evaluation
- experiment logging
- model serialization

---

# 📈 Experiment Tracking Layer

Built using:
- MLflow
- DagsHub

Tracks:
- metrics
- parameters
- models
- artifacts
- training runs

---

# 🌐 Inference Serving Layer

Location:

```text
app.py
```

Responsibilities:
- model loading
- batch prediction
- API inference
- HTML result rendering
- CSV prediction export

---

# 🐳 Deployment Layer

Supports:
- Dockerized deployment
- AWS deployment automation
- GitHub Actions workflows

---

# 📂 Repository Structure

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

# 📊 Pipeline Workflow

```text
Dataset
    ↓
Ingestion
    ↓
Validation
    ↓
Transformation
    ↓
Training
    ↓
MLflow Tracking
    ↓
Artifact Generation
    ↓
FastAPI Serving
    ↓
Docker Deployment
```

---

# 🤖 Models Evaluated

| Model | Purpose |
|---|---|
| Random Forest | Ensemble baseline |
| Decision Tree | Interpretable classifier |
| Gradient Boosting | Sequential boosting |
| Logistic Regression | Linear baseline |
| AdaBoost | Adaptive boosting |

---

# 📈 Model Performance

> Replace placeholder values with actual evaluated metrics.

| Metric | Score |
|---|---|
| Accuracy | XX% |
| Precision | XX% |
| Recall | XX% |
| F1 Score | XX% |

Best Performing Model:

```text
Gradient Boosting
```

---

# 🌐 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Redirects to Swagger UI |
| `/train` | GET | Triggers training pipeline |
| `/predict` | POST | Performs batch CSV inference |

---

# 📥 Batch Prediction Workflow

The prediction service:

- loads preprocessing artifacts
- loads trained models
- transforms incoming CSV input
- generates predictions
- exports results

Output file:

```text
prediction_output/output.csv
```

---

# ⚙️ Environment Variables

Create:

```text
.env
```

Example:

```env
MONGO_DB_URL=<your-mongodb-connection-string>

AWS_ACCESS_KEY_ID=<your-access-key>

AWS_SECRET_ACCESS_KEY=<your-secret-key>

AWS_REGION=us-east-1
```

---

# ⚙️ Local Setup

---

# 1️⃣ Clone Repository

```bash
git clone <your-repository-url>

cd phishing-detection-mlops-system
```

---

# 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

---

# 3️⃣ Activate Environment

### Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

---

# 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt

pip install -e .
```

---

# 📥 Data Loading

Populate MongoDB:

```bash
python push_data.py
```

Dataset source:

```text
network_data/phisingData.csv
```

---

# ▶️ Running The Training Pipeline

```bash
python main.py
```

Pipeline stages:
- ingestion
- validation
- transformation
- model training

Artifacts are stored under:

```text
Artifacts/
```

---

# 🌐 Running FastAPI Service

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# 🐳 Docker Deployment

## Build Image

```bash
docker build -t phishing-detection-system .
```

---

## Run Container

```bash
docker run --env-file .env -p 8000:8000 phishing-detection-system
```

---

# ☁️ AWS Deployment Workflow

The repository supports:
- Docker image build
- Amazon ECR push
- AWS deployment automation

Supported AWS services:
- Amazon ECR
- Amazon EC2
- Amazon S3

---

# 📦 Artifact Management

Supports optional S3 synchronization for:
- model artifacts
- pipeline outputs
- training snapshots

Example structure:

```text
s3://bucket-name/artifacts/<timestamp>
```

---

# 📝 Logging System

Logs are generated under:

```text
logs/<timestamp>.log
```

Custom logging utilities:

```text
network_security/logging/logger.py
```

Custom exception handling:

```text
network_security/exception/exception.py
```

---

# 📊 Engineering Highlights

- End-to-end MLOps pipeline
- MLflow experiment tracking
- FastAPI inference service
- Dockerized deployment
- AWS-compatible workflows
- Modular ML architecture
- Drift detection support
- Schema-driven validation
- Cloud-oriented artifact management
- Production-style ML system design

---

# ⚠️ Current Limitations

Current gaps include:

- no centralized config service
- incomplete pytest coverage
- no model registry yet
- limited observability stack
- incomplete CI quality gates
- no real-time inference monitoring

---

# 🚀 Planned Future Improvements

Planned enhancements include:

- Kubernetes deployment
- Terraform infrastructure provisioning
- model registry integration
- monitoring dashboards
- centralized configuration management
- advanced CI/CD quality gates
- real-time inference streaming
- structured prediction audit logging
- advanced testing coverage
- distributed training workflows

---

# 📌 Current Repository Status

```text
Active Development
```

The repository is continuously evolving toward a more production-grade cloud-native MLOps architecture.

---

# 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Backend | FastAPI, Uvicorn |
| Machine Learning | scikit-learn |
| Data Processing | pandas, NumPy |
| Database | MongoDB |
| Experiment Tracking | MLflow, DagsHub |
| Cloud Services | AWS S3, ECR, EC2 |
| Deployment | Docker, GitHub Actions |
| Packaging | setuptools |

---

# 🎯 What This Project Demonstrates

This project demonstrates practical understanding of:

- MLOps engineering
- cloud-native ML systems
- experiment tracking
- ML pipeline orchestration
- Docker deployment
- FastAPI serving
- modular ML architecture
- AWS deployment workflows
- production-oriented ML engineering

---

# 📌 Strategic Engineering Value

This project demonstrates significantly more engineering depth than notebook-only ML projects because it includes:

- production-style ML pipelines
- experiment tracking infrastructure
- API-based inference serving
- cloud-compatible deployment workflows
- Dockerized architecture
- modular MLOps engineering

---

# 📸 Recommended Screenshot Section

Add screenshots for stronger recruiter impact:

```markdown
![FastAPI Swagger UI](your-image-link)
![MLflow Dashboard](your-image-link)
![Pipeline Architecture](your-image-link)
```

---

# 👨‍💻 Maintainer

## Rudra Tyagi

### Focus Areas

- AWS ML Engineering
- MLOps Systems
- Cloud-Native ML Infrastructure
- Machine Learning Deployment

---

# ⭐ Recruiter Notes

This repository demonstrates:

- production-oriented ML engineering
- cloud-native MLOps architecture
- FastAPI deployment systems
- experiment tracking workflows
- Docker infrastructure
- scalable ML pipeline design

---

# 📜 License

Review the repository license before reuse or redistribution.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

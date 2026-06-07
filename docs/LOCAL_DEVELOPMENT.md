# Local Development Guide

## Environment Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.development.example .env
```

Use local data first:

```env
APP_ENV=development
DATA_INGESTION_SOURCE=local
LOCAL_DATA_FILE_PATH=network_data/phisingData.csv
```

## Validate Repository

```powershell
python scripts/validate_project.py
python scripts/check_dvc_setup.py
pytest -q
```

## Run API

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open:

```text
http://localhost:8000/docs
```

Health checks:

```text
GET /health
GET /health/mongodb
```

## Run Training

```powershell
python main.py
```

Training outputs:

- timestamped pipeline artifacts: `Artifacts/`
- final model: `final_model/model.pkl`
- final preprocessor: `final_model/preprocessor.pkl`
- MLflow local runs when DagsHub env vars are not set: `mlruns/`

## Prediction Audit Logs

Every `/predict` request writes:

```text
logs/predictions.jsonl
prediction_output/output.csv
```

With MongoDB configured, prediction logs are also inserted into:

```text
<MONGODB_DATABASE>.<MONGODB_PREDICTION_LOG_COLLECTION>
```

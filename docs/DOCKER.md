# Docker Guide

## Build

```powershell
docker build -t phishing-detection-api .
```

## Run API Container

```powershell
docker run --env-file .env -p 8000:8000 phishing-detection-api
```

## Docker Compose

Run API:

```powershell
docker compose up --build api
```

Run training inside a container:

```powershell
docker compose --profile train run --rm trainer
```

## Health Check

```powershell
curl http://localhost:8000/health
```

The Dockerfile runs the FastAPI service by default. Training is explicit through `python main.py` or
the compose `train` profile.

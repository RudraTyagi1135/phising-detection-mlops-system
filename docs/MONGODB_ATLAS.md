# MongoDB Atlas Guide

Official references:

- Atlas client connection guide: https://www.mongodb.com/docs/atlas/driver-connection/
- MongoDB connection string formats: https://www.mongodb.com/docs/v8.2/reference/connection-string-formats/

## Atlas Setup

1. Create a MongoDB Atlas project.
2. Create a cluster.
3. Create a database user with read/write access.
4. Add a network access rule:
   - local development: your current public IP
   - ECS production: VPC/NAT egress IP or private networking if configured
5. Choose Connect -> Drivers / Client Libraries.
6. Copy the `mongodb+srv://...` connection string.
7. Replace username, password, and database placeholders.

## Required Variables

```env
DATA_INGESTION_SOURCE=mongodb
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
MONGODB_DATABASE=RUDRA1
MONGODB_COLLECTION=Network_data
MONGODB_PREDICTION_LOG_COLLECTION=prediction_logs
```

## Load Seed Dataset Into Atlas

```powershell
python push_data.py
```

The loader reads `LOCAL_DATA_FILE_PATH` and inserts rows into:

```text
MONGODB_DATABASE.MONGODB_COLLECTION
```

## Health Check

Local:

```powershell
python -c "from network_security.db.mongodb import check_mongodb_health; print(check_mongodb_health(required=True))"
```

API:

```text
GET /health/mongodb
```

## Prediction Logs

Prediction audit records are inserted into:

```text
MONGODB_DATABASE.MONGODB_PREDICTION_LOG_COLLECTION
```

Each record includes:

- request ID
- timestamp
- row index
- feature values
- prediction

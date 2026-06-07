# DVC, DagsHub, and MLflow Guide

Official references:

- DagsHub MLflow tracking: https://dagshub.com/docs/integration_guide/mlflow_tracking/
- DagsHub client setup: https://dagshub.com/docs/client/reference/setup.html
- DVC remotes: https://dvc.org/doc/command-reference/remote
- DVC getting started: https://dvc.org/doc/start

## DagsHub Repository

Create a DagsHub repository for this project. Recommended name:

```text
phising-detection-mlops-system
```

Set these variables in `.env` and GitHub Actions secrets:

```env
DAGSHUB_REPO_OWNER=<dagshub-username-or-org>
DAGSHUB_REPO_NAME=phising-detection-mlops-system
DAGSHUB_TOKEN=<dagshub-token>
DVC_REMOTE_URL=https://dagshub.com/<dagshub-username-or-org>/phising-detection-mlops-system.dvc
MLFLOW_TRACKING_URI=https://dagshub.com/<dagshub-username-or-org>/phising-detection-mlops-system.mlflow
MLFLOW_TRACKING_USERNAME=<dagshub-username-or-org>
MLFLOW_TRACKING_PASSWORD=<dagshub-token>
```

## Configure DVC Remote

```powershell
dvc remote modify dagshub url $env:DVC_REMOTE_URL
dvc remote modify --local dagshub auth basic
dvc remote modify --local dagshub user $env:DAGSHUB_REPO_OWNER
dvc remote modify --local dagshub password $env:DAGSHUB_TOKEN
```

`--local` keeps credentials out of Git.

## Push Existing Artifacts

If these binary artifacts were already committed to Git, remove them from Git tracking while keeping
the files locally:

```powershell
git rm --cached network_data/phisingData.csv final_model/model.pkl final_model/preprocessor.pkl
```

```powershell
dvc status
dvc push network_data/phisingData.csv.dvc
dvc push final_model/model.pkl.dvc
dvc push final_model/preprocessor.pkl.dvc
```

## Pull Artifacts

```powershell
dvc pull network_data/phisingData.csv.dvc
dvc pull final_model/model.pkl.dvc
dvc pull final_model/preprocessor.pkl.dvc
```

## Track New Model Artifacts After Training

After a successful training run:

```powershell
dvc add final_model/model.pkl
dvc add final_model/preprocessor.pkl
dvc push
git add final_model/*.dvc final_model/.gitignore
```

## MLflow

With DagsHub env vars configured:

```powershell
python main.py
```

Runs appear in:

```text
https://dagshub.com/<owner>/<repo>.mlflow
```

Without DagsHub env vars, MLflow falls back to local `mlruns/`.

import sys

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

from network_security.config.settings import get_settings
from network_security.db.mongodb import check_mongodb_health
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.monitoring.prediction_logger import PredictionLogger
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.main_utils.utils import load_object
from network_security.utils.ml_utils.model.estimator import NetworkModel


settings = get_settings()
app = FastAPI(title=settings.app.name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.app.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=str(settings.paths.templates_dir))
prediction_logger = PredictionLogger()


@app.get("/", tags=["system"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["system"])
async def health():
    return {
        "status": "ok",
        "environment": settings.app.environment,
        "model_file_present": settings.paths.final_model_file_path.exists(),
        "preprocessor_file_present": settings.paths.final_preprocessor_file_path.exists(),
    }


@app.get("/health/mongodb", tags=["system"])
async def mongodb_health():
    return check_mongodb_health(required=False)


@app.get("/train", tags=["training"])
async def train_route():
    if not settings.app.training_endpoint_enabled:
        raise HTTPException(status_code=403, detail="Training endpoint is disabled")

    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training completed successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict", tags=["prediction"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        dataframe = pd.read_csv(file.file)
        features = dataframe.drop(columns=[settings.data.target_column], errors="ignore")

        preprocessor = load_object(settings.paths.final_preprocessor_file_path)
        final_model = load_object(settings.paths.final_model_file_path)
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(features)
        output_dataframe = dataframe.copy()
        output_dataframe["predicted_column"] = y_pred

        settings.paths.prediction_output_dir.mkdir(parents=True, exist_ok=True)
        output_dataframe.to_csv(settings.paths.prediction_output_file_path, index=False)

        request_id = prediction_logger.log_batch(features=features, predictions=y_pred, source="api")
        logging.info("Prediction request completed with request_id=%s", request_id)

        table_html = output_dataframe.to_html(classes="table table-striped", index=False)
        return templates.TemplateResponse(
            "table.html",
            {"request": request, "table": table_html, "request_id": request_id},
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host=settings.app.api.host, port=settings.app.api.port)

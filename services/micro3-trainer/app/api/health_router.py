# app/api/health_router.py
# --------------------------------------------------------------------
# Health check endpoints for Trainer service.
# --------------------------------------------------------------------
from fastapi import APIRouter
import torch

from app.models.response_models import HealthResponse
from app.core.logger import logger
from app.storage.postgres_client import get_postgres_client
from app.storage.minio_client import get_minio_client
from app.services.mlflow_tracker import MLflowTracker

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    logger.debug("health ping")
    
    # Check GPU
    gpu_available = torch.cuda.is_available()
    
    # Check PostgreSQL
    postgres_connected = False
    try:
        pg = get_postgres_client()
        with pg.get_connection():
            postgres_connected = True
    except:
        pass
    
    # Check MinIO
    minio_connected = False
    try:
        minio = get_minio_client()
        minio_connected = True
    except:
        pass
    
    # Check MLflow
    mlflow_tracker = MLflowTracker()
    mlflow_connected = mlflow_tracker.connected
    
    return HealthResponse(
        status="ok",
        service="trainer",
        gpu_available=gpu_available,
        ray_initialized=False,  # TODO: Check Ray
        mlflow_connected=mlflow_connected,
        postgres_connected=postgres_connected,
        minio_connected=minio_connected
    )


@router.get("/ready")
async def readiness():
    """Readiness check for Kubernetes"""
    return {"status": "ready"}

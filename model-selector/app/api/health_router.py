# app/api/health_router.py
# --------------------------------------------------------------------
# Simple health check endpoint for orchestrators and monitoring.
# --------------------------------------------------------------------
from fastapi import APIRouter
from app.core.logger import logger

router = APIRouter()


@router.get("/")
def health():
    """Health check endpoint"""
    logger.debug("health ping")
    return {"status": "ok", "service": "model-selector"}


@router.get("/ready")
def ready():
    """Readiness check - verifies all dependencies are available"""
    # TODO: Add database connectivity check
    return {"status": "ready", "service": "model-selector"}

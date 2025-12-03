# app/api/health_router.py
# --------------------------------------------------------------------
# Simple health check endpoint used by orchestrators and tests.
# --------------------------------------------------------------------

from fastapi import APIRouter
from app.core.logger import logger

router = APIRouter()

@router.get("/")
def health():
    logger.debug("health ping")
    return {"status": "ok"}

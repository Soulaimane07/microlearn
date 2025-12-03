# app/main.py
# --------------------------------------------------------------------
# FastAPI application entrypoint: registers routers and middleware.
# --------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health_router import router as health_router
from app.api.detect_router import router as detect_router
from app.api.prepare_router import router as prepare_router
from app.storage.minio_client import init_minio
from app.core.logger import logger

app = FastAPI(title="MicroLearn DataPreparer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(detect_router, prefix="/detect", tags=["Detect"])
app.include_router(prepare_router, prefix="/prepare", tags=["Prepare"])


@app.on_event("startup")
async def startup_event():
    logger.info("DataPreparer starting...")

    # Initialize MinIO connection and ensure bucket exists
    try:
        logger.info("Initializing MinIO connection...")
        init_minio()
        logger.info("✓ MinIO initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize MinIO: {e}")
        logger.warning("App will continue but MinIO operations may fail")

    logger.info("DataPreparer started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("DataPreparer stopped")
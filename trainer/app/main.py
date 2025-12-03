# app/main.py
# --------------------------------------------------------------------
# Main FastAPI application for Trainer microservice.
# --------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import logger
from app.api import health_router, train_router, models_router
from app.storage.postgres_client import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"{settings.SERVICE_NAME} starting...")
    
    # Initialize database
    try:
        logger.info("Initializing PostgreSQL connection...")
        init_db()
        logger.info("✓ PostgreSQL initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize PostgreSQL: {e}")
        logger.warning("App will continue but database operations may fail")
    
    # Initialize MinIO
    try:
        logger.info("Initializing MinIO connection...")
        from app.storage.minio_client import get_minio_client
        get_minio_client()
        logger.info("✓ MinIO initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize MinIO: {e}")
        logger.warning("App will continue but storage operations may fail")
    
    # Check GPU availability (torch disabled for now)
    # import torch
    # if torch.cuda.is_available():
    #     logger.info(f"✓ GPU available: {torch.cuda.device_count()} device(s)")
    #     for i in range(torch.cuda.device_count()):
    #         logger.info(f"  - GPU {i}: {torch.cuda.get_device_name(i)}")
    # else:
    #     logger.info("ℹ No GPU available, using CPU")
    logger.info("ℹ GPU support disabled (torch not installed), using CPU only")
    
    logger.info(f"{settings.SERVICE_NAME} started successfully")
    
    yield
    
    # Shutdown
    logger.info(f"{settings.SERVICE_NAME} shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Trainer Microservice",
    description="Model training service with GPU support, Ray parallelization, and MLflow tracking",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router.router, prefix="/health", tags=["Health"])
app.include_router(train_router.router, prefix="/train", tags=["Training"])
app.include_router(models_router.router, prefix="/models", tags=["Models"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG
    )

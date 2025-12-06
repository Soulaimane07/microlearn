# app/main.py
# --------------------------------------------------------------------
# FastAPI application entrypoint for ModelSelector microservice.
# Registers routers, middleware, and handles startup/shutdown events.
# --------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health_router import router as health_router
from app.api.select_router import router as select_router
from app.api.models_router import router as models_router
from app.storage.postgres_client import init_db
from app.core.logger import logger

app = FastAPI(
    title="MicroLearn ModelSelector",
    version="1.0.0",
    description="Automatic model selection microservice for MicroLearn AutoML platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(select_router, prefix="/select", tags=["Model Selection"])
app.include_router(models_router, prefix="/models", tags=["Model Catalog"])


@app.on_event("startup")
async def startup_event():
    logger.info("ModelSelector starting...")

    # Initialize PostgreSQL connection and create tables
    try:
        logger.info("Initializing PostgreSQL connection...")
        init_db()
        logger.info("✓ PostgreSQL initialized successfully")
    except Exception as e:
        logger.error(f"✗ Failed to initialize PostgreSQL: {e}")
        logger.warning("App will continue but database operations may fail")

    logger.info("ModelSelector started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("ModelSelector stopped")

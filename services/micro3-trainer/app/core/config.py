# app/core/config.py
# --------------------------------------------------------------------
# Configuration settings for Trainer microservice.
# Uses Pydantic Settings for environment variable management.
# --------------------------------------------------------------------
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Service Configuration
    SERVICE_NAME: str = "trainer"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8002
    DEBUG: bool = False
    
    # PostgreSQL Configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "microlearn"
    
    # MinIO Configuration
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_BUCKET_MODELS: str = "trained-models"
    MINIO_BUCKET_DATA: str = "data-preparer"
    
    # MLflow Configuration
    MLFLOW_TRACKING_URI: str = "http://mlflow:5000"
    MLFLOW_EXPERIMENT_NAME: str = "microlearn-training"
    
    # Ray Configuration
    RAY_ADDRESS: Optional[str] = None  # None = start local cluster
    RAY_NUM_CPUS: Optional[int] = None  # None = use all available
    RAY_NUM_GPUS: Optional[int] = None  # None = auto-detect
    
    # Training Configuration
    MAX_PARALLEL_JOBS: int = 3
    CHECKPOINT_INTERVAL: int = 5  # Save checkpoint every N epochs
    DEFAULT_EPOCHS: int = 100
    DEFAULT_BATCH_SIZE: int = 32
    EARLY_STOPPING_PATIENCE: int = 10
    
    # GPU Configuration
    CUDA_VISIBLE_DEVICES: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# app/core/config.py
# --------------------------------------------------------------------
# Configuration settings for ModelSelector microservice.
# Reads from environment variables with sensible defaults.
# --------------------------------------------------------------------
import os


class Settings:
    # Database settings
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # MinIO settings (for reading prepared datasets)
    MINIO_ENDPOINT: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET: str
    MINIO_SECURE: bool

    # Service settings
    PROJECT_NAME: str
    DATA_PREPARER_URL: str

    def __init__(self):
        # Database
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = int(os.getenv("DB_PORT", "5432"))
        self.DB_NAME = os.getenv("DB_NAME", "microlearn")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

        # MinIO
        self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
        self.MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
        self.MINIO_BUCKET = os.getenv("MINIO_BUCKET", "data-preparer")
        self.MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "yes")

        # Service
        self.PROJECT_NAME = os.getenv("PROJECT_NAME", "Model Selector")
        self.DATA_PREPARER_URL = os.getenv("DATA_PREPARER_URL", "http://data-preparer:8000")


settings = Settings()

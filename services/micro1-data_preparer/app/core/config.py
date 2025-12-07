# app/core/config.py
# --------------------------------------------------------------------
# Lightweight settings loader reading environment variables. This avoids
# pydantic/versions issues and keeps configuration explicit.
# --------------------------------------------------------------------
import os


class Settings:
    MINIO_ENDPOINT: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET: str
    MINIO_SECURE: bool

    def __init__(self):
        self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
        self.MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
        self.MINIO_BUCKET = os.getenv("MINIO_BUCKET", "data-preparer")
        # Convert string to boolean for MINIO_SECURE
        self.MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "yes")

        # Add project name for API metadata
        self.PROJECT_NAME = os.getenv("PROJECT_NAME", "Data Preparer")


settings = Settings()
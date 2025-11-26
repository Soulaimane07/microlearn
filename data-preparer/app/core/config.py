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

    def __init__(self):
        self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
        self.MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin")
        self.MINIO_BUCKET = os.getenv("MINIO_BUCKET", "data-preparer")

settings = Settings()

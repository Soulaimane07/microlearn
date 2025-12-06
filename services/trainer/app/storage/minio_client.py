# app/storage/minio_client.py
# --------------------------------------------------------------------
# MinIO client for storing trained models and checkpoints.
# --------------------------------------------------------------------
from minio import Minio
from minio.error import S3Error
from io import BytesIO
import pickle
from typing import Any, Optional
from datetime import timedelta

from app.core.config import settings
from app.core.logger import logger


class MinIOClient:
    """MinIO client for model storage"""
    
    def __init__(self):
        """Initialize MinIO client"""
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_models = settings.MINIO_BUCKET_MODELS
        self.bucket_data = settings.MINIO_BUCKET_DATA
        
        # Ensure buckets exist
        self._ensure_buckets()
    
    def _ensure_buckets(self):
        """Create buckets if they don't exist"""
        try:
            for bucket in [self.bucket_models, self.bucket_data]:
                if not self.client.bucket_exists(bucket):
                    self.client.make_bucket(bucket)
                    logger.info(f"Created MinIO bucket: {bucket}")
                else:
                    logger.debug(f"MinIO bucket exists: {bucket}")
        except S3Error as e:
            logger.error(f"Failed to ensure buckets: {e}")
            raise
    
    def upload_model(self, model_data: bytes, object_name: str) -> str:
        """
        Upload trained model to MinIO.
        
        Args:
            model_data: Serialized model bytes
            object_name: Object path in bucket
            
        Returns:
            MinIO path to uploaded model
        """
        try:
            data_stream = BytesIO(model_data)
            self.client.put_object(
                self.bucket_models,
                object_name,
                data_stream,
                length=len(model_data),
                content_type="application/octet-stream"
            )
            
            path = f"{self.bucket_models}/{object_name}"
            logger.info(f"Uploaded model to MinIO: {path}")
            return path
            
        except S3Error as e:
            logger.error(f"Failed to upload model: {e}")
            raise
    
    def download_model(self, object_name: str) -> bytes:
        """
        Download model from MinIO.
        
        Args:
            object_name: Object path in bucket
            
        Returns:
            Model data as bytes
        """
        try:
            response = self.client.get_object(self.bucket_models, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.info(f"Downloaded model from MinIO: {object_name}")
            return data
            
        except S3Error as e:
            logger.error(f"Failed to download model: {e}")
            raise
    
    def download_dataset(self, object_name: str) -> bytes:
        """
        Download dataset from data bucket.
        
        Args:
            object_name: Object path in data bucket
            
        Returns:
            Dataset as bytes
        """
        try:
            # Remove bucket prefix if present
            if object_name.startswith(self.bucket_data + "/"):
                object_name = object_name[len(self.bucket_data) + 1:]
            
            response = self.client.get_object(self.bucket_data, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            
            logger.info(f"Downloaded dataset from MinIO: {object_name}")
            return data
            
        except S3Error as e:
            logger.error(f"Failed to download dataset: {e}")
            raise
    
    def get_object_size(self, object_name: str, bucket: Optional[str] = None) -> float:
        """
        Get size of object in MB.
        
        Args:
            object_name: Object path
            bucket: Bucket name (defaults to models bucket)
            
        Returns:
            Size in MB
        """
        try:
            bucket = bucket or self.bucket_models
            stat = self.client.stat_object(bucket, object_name)
            size_mb = stat.size / (1024 * 1024)
            return round(size_mb, 2)
        except S3Error as e:
            logger.error(f"Failed to get object size: {e}")
            return 0.0
    
    def generate_presigned_url(self, object_name: str, expiry: int = 3600) -> str:
        """
        Generate presigned URL for model download.
        
        Args:
            object_name: Object path
            expiry: URL expiry in seconds
            
        Returns:
            Presigned URL
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_models,
                object_name,
                expires=timedelta(seconds=expiry)
            )
            return url
        except S3Error as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise
    
    def list_models(self, prefix: str = "") -> list:
        """
        List all models in bucket.
        
        Args:
            prefix: Object prefix filter
            
        Returns:
            List of object names
        """
        try:
            objects = self.client.list_objects(self.bucket_models, prefix=prefix)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def delete_model(self, object_name: str) -> bool:
        """
        Delete model from MinIO.
        
        Args:
            object_name: Object path
            
        Returns:
            True if successful
        """
        try:
            self.client.remove_object(self.bucket_models, object_name)
            logger.info(f"Deleted model from MinIO: {object_name}")
            return True
        except S3Error as e:
            logger.error(f"Failed to delete model: {e}")
            return False


# Global instance
_minio_client: Optional[MinIOClient] = None


def get_minio_client() -> MinIOClient:
    """Get or create MinIO client instance"""
    global _minio_client
    if _minio_client is None:
        _minio_client = MinIOClient()
    return _minio_client


def upload_model_bytes(model_data: bytes, object_name: str) -> str:
    """Convenience function to upload model"""
    return get_minio_client().upload_model(model_data, object_name)


def download_model_bytes(object_name: str) -> bytes:
    """Convenience function to download model"""
    return get_minio_client().download_model(object_name)


def download_dataset_bytes(object_name: str) -> bytes:
    """Convenience function to download dataset"""
    return get_minio_client().download_dataset(object_name)

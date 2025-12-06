# app/storage/minio_client.py
# --------------------------------------------------------------------
# MinIO client for accessing prepared datasets from DataPreparer service.
# --------------------------------------------------------------------
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from typing import Optional

from app.core.logger import logger
from app.core.config import settings


# Initialize MinIO client
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=settings.MINIO_SECURE
)


def download_bytes(object_name: str, bucket: Optional[str] = None) -> bytes:
    """
    Download an object from MinIO as bytes.
    
    Args:
        object_name: Path/name of object in MinIO
        bucket: Bucket name (defaults to config bucket)
        
    Returns:
        File contents as bytes
        
    Raises:
        FileNotFoundError if object doesn't exist
        Exception for other errors
    """
    bucket_name = bucket or settings.MINIO_BUCKET
    
    try:
        response = minio_client.get_object(bucket_name, object_name)
        data = response.read()
        response.close()
        response.release_conn()
        
        logger.info(f"Downloaded {object_name} from MinIO ({len(data)} bytes)")
        return data
        
    except S3Error as e:
        if e.code == "NoSuchKey":
            logger.error(f"Object not found in MinIO: {object_name}")
            raise FileNotFoundError(f"Object not found: {object_name}")
        logger.error(f"MinIO error downloading {object_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error downloading from MinIO: {e}")
        raise


def check_object_exists(object_name: str, bucket: Optional[str] = None) -> bool:
    """
    Check if an object exists in MinIO.
    
    Args:
        object_name: Path/name of object to check
        bucket: Bucket name (defaults to config bucket)
        
    Returns:
        True if object exists, False otherwise
    """
    bucket_name = bucket or settings.MINIO_BUCKET
    
    try:
        minio_client.stat_object(bucket_name, object_name)
        return True
    except S3Error as e:
        if e.code == "NoSuchKey":
            return False
        raise
    except Exception:
        return False


def list_objects(prefix: str = "", bucket: Optional[str] = None) -> list:
    """
    List objects in MinIO bucket with optional prefix.
    
    Args:
        prefix: Prefix to filter objects
        bucket: Bucket name (defaults to config bucket)
        
    Returns:
        List of object names
    """
    bucket_name = bucket or settings.MINIO_BUCKET
    
    try:
        objects = minio_client.list_objects(bucket_name, prefix=prefix, recursive=True)
        return [obj.object_name for obj in objects]
    except Exception as e:
        logger.error(f"Error listing objects: {e}")
        return []


def get_object_info(object_name: str, bucket: Optional[str] = None) -> Optional[dict]:
    """
    Get metadata about an object in MinIO.
    
    Args:
        object_name: Path/name of object
        bucket: Bucket name (defaults to config bucket)
        
    Returns:
        Dictionary with object metadata, or None if not found
    """
    bucket_name = bucket or settings.MINIO_BUCKET
    
    try:
        stat = minio_client.stat_object(bucket_name, object_name)
        return {
            "name": stat.object_name,
            "size": stat.size,
            "content_type": stat.content_type,
            "last_modified": stat.last_modified.isoformat() if stat.last_modified else None,
            "etag": stat.etag
        }
    except S3Error as e:
        if e.code == "NoSuchKey":
            return None
        raise
    except Exception as e:
        logger.error(f"Error getting object info: {e}")
        return None

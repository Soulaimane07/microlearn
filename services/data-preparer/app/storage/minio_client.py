# app/storage/minio_client.py
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from app.core.logger import logger
from app.core.config import settings

# Initialize MinIO client with bucket_name set
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=settings.MINIO_SECURE
)


def ensure_bucket_exists():
    """Create bucket if it doesn't exist"""
    try:
        # Try-except approach to handle different API versions
        try:
            # Try new API (minio >= 7.0)
            found = minio_client.bucket_exists(settings.MINIO_BUCKET)
        except TypeError:
            # Fallback to old API - bucket_exists takes no args
            # Set bucket first, then check
            try:
                # This is for very old versions where you set bucket on client
                minio_client.bucket_name = settings.MINIO_BUCKET
                found = minio_client.bucket_exists()
            except AttributeError:
                # If that doesn't work, try listing buckets
                buckets = minio_client.list_buckets()
                found = any(b.name == settings.MINIO_BUCKET for b in buckets)

        if not found:
            try:
                # Try new API
                minio_client.make_bucket(settings.MINIO_BUCKET)
            except TypeError:
                # Try with location parameter
                try:
                    minio_client.make_bucket(settings.MINIO_BUCKET, location='us-east-1')
                except TypeError:
                    # Very old API
                    minio_client.bucket_name = settings.MINIO_BUCKET
                    minio_client.make_bucket()

            logger.info(f"Created bucket: {settings.MINIO_BUCKET}")
        else:
            logger.info(f"Bucket already exists: {settings.MINIO_BUCKET}")

    except S3Error as e:
        logger.error(f"S3 error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error with bucket operations: {e}")
        import minio as minio_module
        logger.error(f"MinIO version: {minio_module.__version__}")
        raise


def init_minio():
    """Initialize MinIO - call this from app startup"""
    ensure_bucket_exists()


def upload_bytes(object_name: str, data: bytes, content_type: str = "application/octet-stream"):
    """
    Upload bytes to MinIO

    Args:
        object_name: Path/name of object in MinIO (e.g., "raw/file.csv")
        data: Bytes to upload
        content_type: MIME type of the data

    Returns:
        ObjectWriteResult from MinIO

    Raises:
        Exception if upload fails
    """
    try:
        # Ensure bucket exists before upload
        ensure_bucket_exists()

        # Convert bytes to BytesIO stream
        data_stream = BytesIO(data)
        data_length = len(data)

        result = minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=object_name,
            data=data_stream,
            length=data_length,
            content_type=content_type
        )

        logger.info(f"Uploaded {object_name} to MinIO ({data_length} bytes)")
        return result

    except S3Error as e:
        logger.error(f"S3 error uploading {object_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error uploading {object_name}: {e}")
        raise


def download_bytes(object_name: str) -> bytes:
    """
    Download object from MinIO as bytes

    Args:
        object_name: Path/name of object in MinIO

    Returns:
        bytes: File content

    Raises:
        FileNotFoundError: If object doesn't exist
        Exception: For other errors
    """
    try:
        response = minio_client.get_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=object_name
        )

        # Read all data
        data = response.read()
        response.close()
        response.release_conn()

        logger.info(f"Downloaded {object_name} from MinIO ({len(data)} bytes)")
        return data

    except S3Error as e:
        if e.code == "NoSuchKey":
            logger.error(f"Object not found: {object_name}")
            raise FileNotFoundError(f"Object not found in MinIO: {object_name}")
        else:
            logger.error(f"S3 error downloading {object_name}: {e}")
            raise
    except Exception as e:
        logger.error(f"Error downloading {object_name}: {e}")
        raise


def list_objects(prefix: str = None) -> list:
    """
    List objects in MinIO bucket

    Args:
        prefix: Optional prefix to filter objects (e.g., "raw/")

    Returns:
        list: List of object names
    """
    try:
        objects = minio_client.list_objects(
            bucket_name=settings.MINIO_BUCKET,
            prefix=prefix,
            recursive=True
        )

        object_names = [obj.object_name for obj in objects]
        logger.info(f"Listed {len(object_names)} objects with prefix '{prefix}'")
        return object_names

    except S3Error as e:
        logger.error(f"Error listing objects: {e}")
        raise
    except Exception as e:
        logger.error(f"Error listing objects: {e}")
        raise


def delete_object(object_name: str):
    """
    Delete object from MinIO

    Args:
        object_name: Path/name of object to delete
    """
    try:
        minio_client.remove_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=object_name
        )
        logger.info(f"Deleted {object_name} from MinIO")

    except S3Error as e:
        logger.error(f"Error deleting {object_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error deleting {object_name}: {e}")
        raise


def object_exists(object_name: str) -> bool:
    """
    Check if object exists in MinIO

    Args:
        object_name: Path/name of object

    Returns:
        bool: True if exists, False otherwise
    """
    try:
        minio_client.stat_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=object_name
        )
        return True
    except S3Error as e:
        if e.code == "NoSuchKey":
            return False
        raise
    except Exception as e:
        logger.error(f"Error checking existence of {object_name}: {e}")
        raise
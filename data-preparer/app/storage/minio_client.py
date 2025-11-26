# app/storage/minio_client.py
# --------------------------------------------------------------------
# Robust MinIO helper functions: upload_bytes, download_bytes.
# Tries to be compatible with different minio SDK versions by:
# - using keyword endpoint=...
# - avoiding imports of datatypes specific to SDK versions
# - creating buckets safely
# --------------------------------------------------------------------
from minio import Minio
from app.core.config import settings
from app.core.logger import logger
from io import BytesIO

_client = None

def get_client():
    """
    Return a Minio client instance. Use 'endpoint=' keyword for maximum
    compatibility across MinIO SDK versions.
    """
    global _client
    if _client is None:
        _client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=False
        )
    return _client

def ensure_bucket(bucket_name: str):
    """
    Ensure bucket exists. Different MinIO client versions expose different
    APIs; this function attempts a safe create-when-needed approach.
    """
    client = get_client()
    try:
        # try bucket_exists first if available
        if hasattr(client, "bucket_exists"):
            try:
                exists = client.bucket_exists(bucket_name)
                if exists:
                    return
            except TypeError:
                # some SDK versions expect a single arg object; fall through
                pass
        # fallback: try to create bucket and ignore if it already exists
        try:
            client.make_bucket(bucket_name)
            logger.info(f"Created bucket {bucket_name}")
        except Exception as exc:
            # ignore error if bucket exists; else raise
            msg = str(exc).lower()
            if "already exists" in msg or "bucket already owned by you" in msg or "bucket exists" in msg:
                return
            # bucket_exists may work on second try
            if hasattr(client, "bucket_exists"):
                try:
                    if client.bucket_exists(bucket_name):
                        return
                except Exception:
                    pass
            # re-raise if unknown
            raise
    except Exception as exc:
        logger.error(f"Failed ensuring bucket {bucket_name}: {exc}")
        raise

def upload_bytes(object_name: str, data: bytes):
    """
    Upload bytes to configured bucket at object_name.
    """
    client = get_client()
    bucket = settings.MINIO_BUCKET
    ensure_bucket(bucket)

    try:
        # put_object expects a stream in many versions.
        client.put_object(bucket, object_name, data=BytesIO(data), length=len(data))
        logger.info(f"Uploaded {object_name} to bucket {bucket}")
    except TypeError:
        # some versions accept the data and length as positional args
        client.put_object(bucket, object_name, BytesIO(data), len(data))
        logger.info(f"Uploaded {object_name} to bucket {bucket}")
    except Exception as exc:
        logger.error(f"MinIO upload failed: {exc}")
        raise

def download_bytes(object_name: str) -> bytes:
    """
    Download object bytes from configured bucket.
    """
    client = get_client()
    bucket = settings.MINIO_BUCKET
    ensure_bucket(bucket)  # will create bucket if missing -> not ideal for download but safe

    try:
        response = client.get_object(bucket, object_name)
        data = response.read()
        try:
            response.close()
            response.release_conn()
        except Exception:
            pass
        logger.info(f"Downloaded {object_name} from {bucket}")
        return data
    except Exception as exc:
        logger.error(f"MinIO download failed: {exc}")
        raise

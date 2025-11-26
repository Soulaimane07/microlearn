"""
Minimal S3 client wrapper using boto3 so the service can work with MinIO
or any S3-compatible endpoint. Provides upload_bytes, download_bytes and
object_exists helpers.
"""
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from app.core.config import settings
from app.core.logger import logger

_session = None
_s3 = None
_bucket = settings.S3_BUCKET

def get_client():
    global _session, _s3
    if _s3 is None:
        _session = boto3.session.Session()
        _s3 = _session.client(
            service_name="s3",
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(signature_version="s3v4"),
        )
    return _s3

def ensure_bucket(bucket_name: str):
    cli = get_client()
    try:
        cli.head_bucket(Bucket=bucket_name)
    except ClientError:
        # try create
        try:
            cli.create_bucket(Bucket=bucket_name)
            logger.info("Created bucket %s", bucket_name)
        except Exception as exc:
            logger.error("Failed to create bucket: %s", exc)
            raise

def upload_bytes(key: str, data: bytes):
    cli = get_client()
    ensure_bucket(_bucket)
    try:
        cli.put_object(Bucket=_bucket, Key=key, Body=data)
        logger.info("Uploaded %s to bucket %s", key, _bucket)
    except Exception as exc:
        logger.error("S3 upload failed: %s", exc)
        raise

def download_bytes(key: str) -> bytes:
    cli = get_client()
    try:
        resp = cli.get_object(Bucket=_bucket, Key=key)
        payload = resp["Body"].read()
        return payload
    except Exception as exc:
        logger.error("S3 download failed: %s", exc)
        raise

def object_exists(key: str) -> bool:
    cli = get_client()
    try:
        cli.head_object(Bucket=_bucket, Key=key)
        return True
    except ClientError:
        return False

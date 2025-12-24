from minio import Minio
from app.core.config import *

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def load_predictions(model_id: str):
    """
    Expect file:
    models/{model_id}/predictions.csv
    """
    obj = minio_client.get_object(
        MINIO_BUCKET,
        f"models/{model_id}/predictions.csv"
    )
    return obj.read()
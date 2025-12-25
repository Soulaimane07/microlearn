from minio import Minio
import pandas as pd
import os 
from io import BytesIO

client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

BUCKET = "data-preparer"

def load_dataset(object_name: str) -> pd.DataFrame:
    response = client.get_object(BUCKET, object_name)
    return pd.read_csv(response)

def upload_model(local_path: str, object_name: str):
    """
    Uploads a local file (trained model) to MinIO.
    Args:
        local_path: path to local file
        object_name: name/path in MinIO bucket
    """
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"{local_path} does not exist")

    client.fput_object(
        bucket_name=BUCKET,
        object_name=object_name,
        file_path=local_path
    )
    print(f"Uploaded {local_path} to MinIO as {object_name}")
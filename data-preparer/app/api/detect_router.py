# app/api/detect_router.py
# --------------------------------------------------------------------
# Accepts CSV upload, runs detectors, stores raw CSV to MinIO and a YAML
# describing the automatic pipeline to use for /prepare.
# --------------------------------------------------------------------
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pandas as pd
import io
import yaml

from app.services.autodetect import detect_metadata, metadata_to_pipeline_config
from app.storage.minio_client import upload_bytes
from app.core.logger import logger
from app.models.response_models import DetectResponse
from app.core.config import settings

router = APIRouter()

@router.post("", response_model=DetectResponse)
async def detect(file: UploadFile = File(...), store_to_minio: Optional[bool] = Form(False)):
    """
    Upload a CSV and return detected metadata:
     - stores raw CSV in MinIO at raw/<filename> when store_to_minio=True
     - writes a pipeline YAML at pipelines/<filename_no_ext>.yml when store_to_minio=True
    """
    try:
        raw = await file.read()
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as exc:
        logger.error(f"Failed reading CSV: {exc}")
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    # run detection
    meta = detect_metadata(df)

    response = {
        "id_columns": meta["id_columns"],
        "date_columns": meta["date_columns"],
        "numeric_columns": meta["numeric_columns"],
        "categorical_columns": meta["categorical_columns"],
        "minio_object": None
    }

    if store_to_minio:
        # store raw CSV
        object_name = f"raw/{file.filename}"
        try:
            upload_bytes(object_name, raw)
        except Exception as exc:
            logger.error(f"Failed to store raw file in MinIO: {exc}")
            raise HTTPException(status_code=500, detail="Failed to store raw file in MinIO")
        response["minio_object"] = object_name

        # derive pipeline config (auto) and write YAML to MinIO
        pipeline_conf = metadata_to_pipeline_config(meta)
        yml_bytes = yaml.dump(pipeline_conf, sort_keys=False).encode("utf-8")
        yml_name = f"pipelines/{file.filename.rsplit('.',1)[0]}.yml"
        try:
            upload_bytes(yml_name, yml_bytes)
            # include pipeline path in response
            response["pipeline_yml"] = yml_name
        except Exception as exc:
            logger.error(f"Failed to store pipeline YAML in MinIO: {exc}")
            # not fatal for detect response; just inform
            response["pipeline_yml"] = None

    logger.info("Detection completed")
    return response

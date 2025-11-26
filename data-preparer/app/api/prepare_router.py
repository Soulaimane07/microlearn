# app/api/prepare_router.py
# --------------------------------------------------------------------
# Run the deterministic, automatic pipeline:
# - Accepts file upload OR minio_object pointing to raw CSV
# - Accepts optional pipeline_yml (MinIO path). If not provided we try
#   to infer pipelines/<rawfilename>.yml in MinIO (the one created by /detect).
# - Stores processed CSV to MinIO under processed/
# --------------------------------------------------------------------
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pandas as pd
import io
import yaml

from app.services.pipeline import run_pipeline
from app.storage.minio_client import upload_bytes, download_bytes
from app.core.logger import logger

router = APIRouter()

@router.post("")
async def prepare(file: UploadFile = File(None),
                  minio_object: Optional[str] = Form(None),
                  pipeline_yml: Optional[str] = Form(None)):
    """
    Prepare the dataset. Provide either file OR minio_object.
    Optionally provide pipeline_yml (MinIO path), otherwise the function will
    attempt to use 'pipelines/<rawfilename>.yml' if minio_object is provided.
    """
    # 1) load dataframe
    if file:
        try:
            raw = await file.read()
            df = pd.read_csv(io.BytesIO(raw))
            original_filename = file.filename
        except Exception as exc:
            logger.error(f"Invalid CSV file uploaded: {exc}")
            raise HTTPException(status_code=400, detail="Invalid CSV file")
    elif minio_object:
        try:
            raw = download_bytes(minio_object)  # raises if not found
            df = pd.read_csv(io.BytesIO(raw))
            original_filename = minio_object.split('/')[-1]
        except Exception as exc:
            logger.error(f"Failed to download CSV from MinIO: {exc}")
            raise HTTPException(status_code=400, detail="Cannot download file from MinIO")
    else:
        raise HTTPException(status_code=400, detail="Provide file OR minio_object")

    # 2) determine pipeline YAML
    pipeline_conf = None
    if pipeline_yml:
        try:
            yml_bytes = download_bytes(pipeline_yml)
            pipeline_conf = yaml.safe_load(yml_bytes)
        except Exception as exc:
            logger.error(f"Failed to load pipeline YAML from {pipeline_yml}: {exc}")
            raise HTTPException(status_code=400, detail="Cannot download pipeline YAML")
    else:
        # attempt to use pipelines/<original_filename_no_ext>.yml
        name_no_ext = original_filename.rsplit('.',1)[0]
        guessed = f"pipelines/{name_no_ext}.yml"
        try:
            yml_bytes = download_bytes(guessed)
            pipeline_conf = yaml.safe_load(yml_bytes)
        except Exception:
            # proceed with default automatic pipeline if no YAML available
            pipeline_conf = None

    # 3) run pipeline
    try:
        processed = run_pipeline(df, pipeline_conf)  # pipeline_conf can be None => auto
    except ValueError as exc:
        logger.error(f"Pipeline error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected pipeline failure")
        raise HTTPException(status_code=500, detail="Processing failed")

    # 4) store processed CSV to MinIO
    processed_bytes = processed.to_csv(index=False).encode("utf-8")
    out_name = f"processed/processed_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    try:
        upload_bytes(out_name, processed_bytes)
    except Exception as exc:
        logger.error(f"Failed to store processed CSV: {exc}")
        raise HTTPException(status_code=500, detail="Failed to store processed CSV")

    logger.info(f"Processed stored as {out_name}")
    return {"message": "Processed", "minio_object": out_name, "rows": len(processed)}

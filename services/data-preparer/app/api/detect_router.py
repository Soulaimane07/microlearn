# app/api/detect_router.py
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
async def detect(
    file: UploadFile = File(...),
    store_to_minio: Optional[bool] = Form(True)
):
    """
    Upload a CSV and return detected metadata:
     - stores raw CSV in MinIO at raw/<filename> when store_to_minio=True
     - writes a pipeline YAML at pipelines/<filename_no_ext>.yml when store_to_minio=True
    """

    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Read and parse CSV
    try:
        raw = await file.read()
        if len(raw) == 0:
            raise HTTPException(status_code=400, detail="Empty file provided")
        df = pd.read_csv(io.BytesIO(raw))

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV contains no data")

        logger.info(f"Successfully read CSV: {file.filename} with {len(df)} rows, {len(df.columns)} columns")
    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty")
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as exc:
        logger.error(f"Failed parsing CSV: {exc}")
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(exc)}")
    except Exception as exc:
        logger.error(f"Failed reading CSV: {exc}")
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(exc)}")

    # Run detection
    try:
        meta = detect_metadata(df)
        logger.info(f"Detected metadata: {meta}")
    except Exception as exc:
        logger.error(f"Detection failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Metadata detection failed: {str(exc)}")

    # Build response
    response = {
        "id_columns": meta.get("id_columns", []),
        "date_columns": meta.get("date_columns", []),
        "numeric_columns": meta.get("numeric_columns", []),
        "categorical_columns": meta.get("categorical_columns", []),
        "minio_object": None,
        "pipeline_yml": None
    }

    # Store to MinIO if requested
    if store_to_minio:
        # Store raw CSV
        object_name = f"raw/{file.filename}"
        try:
            upload_bytes(object_name, raw)
            response["minio_object"] = object_name
            logger.info(f"Stored raw CSV to MinIO: {object_name}")
        except Exception as exc:
            logger.error(f"Failed to store raw file in MinIO: {exc}")
            raise HTTPException(status_code=500, detail=f"Failed to store raw file: {str(exc)}")

        # Generate and store pipeline config
        try:
            pipeline_conf = metadata_to_pipeline_config(meta)

            # Validate pipeline config
            if not isinstance(pipeline_conf, dict):
                raise ValueError("Pipeline config must be a dictionary")

            yml_bytes = yaml.dump(pipeline_conf, sort_keys=False, default_flow_style=False).encode("utf-8")

            # Use consistent naming: remove .csv extension and add .yml
            base_name = file.filename.rsplit('.', 1)[0]
            yml_name = f"pipelines/{base_name}.yml"

            upload_bytes(yml_name, yml_bytes)
            response["pipeline_yml"] = yml_name

            logger.info(f"Stored pipeline YAML to MinIO: {yml_name}")
            logger.debug(f"Pipeline config: {pipeline_conf}")

        except Exception as exc:
            logger.error(f"Failed to store pipeline YAML in MinIO: {exc}")
            # Clean up raw file if pipeline storage failed
            raise HTTPException(status_code=500, detail=f"Failed to store pipeline config: {str(exc)}")

    logger.info(f"Detection completed successfully for {file.filename}")
    return response
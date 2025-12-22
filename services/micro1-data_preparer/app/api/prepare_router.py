# app/api/prepare_router.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import pandas as pd
import io
import yaml

from app.messaging.nats_client import publish_step_done

from app.services.pipeline import run_pipeline
from app.storage.minio_client import upload_bytes, download_bytes
from app.core.logger import logger

router = APIRouter()


@router.post("")
async def prepare(
        pipeline_id: str = Form(...),          # ✅ ADD THIS
        file: UploadFile = File(None),
        minio_object: Optional[str] = Form(None),
        pipeline_yml: Optional[str] = Form(None),
        target_column: Optional[str] = Form(None)
):
    """
    Prepare the dataset. Provide either file OR minio_object.
    Optionally provide pipeline_yml (MinIO path), otherwise attempts to use
    'pipelines/<rawfilename>.yml' if minio_object is provided.

    Returns cleaned data preview and metadata.
    """

    # 1) Load dataframe
    df = None
    original_filename = None

    if file and minio_object:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'file' OR 'minio_object', not both"
        )

    if file:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        try:
            raw = await file.read()
            if len(raw) == 0:
                raise HTTPException(status_code=400, detail="Empty file provided")

            df = pd.read_csv(io.BytesIO(raw))
            if df.empty:
                raise HTTPException(status_code=400, detail="CSV contains no data")
            original_filename = file.filename
            logger.info(f"Loaded CSV from upload: {original_filename} ({len(df)} rows)")
        except Exception as exc:
            logger.error(f"Failed reading uploaded file: {exc}")
            raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(exc)}")

    elif minio_object:
        try:
            raw = download_bytes(minio_object)
            df = pd.read_csv(io.BytesIO(raw))
            if df.empty:
                raise HTTPException(status_code=400, detail="CSV from MinIO contains no data")
            original_filename = minio_object.split('/')[-1]
            logger.info(f"Loaded CSV from MinIO: {minio_object} ({len(df)} rows)")
        except Exception as exc:
            logger.error(f"Failed to download CSV from MinIO: {exc}")
            raise HTTPException(status_code=400, detail=f"Cannot download file from MinIO: {str(exc)}")
    else:
        raise HTTPException(status_code=400, detail="Must provide either 'file' or 'minio_object'")

    # 2) Load pipeline YAML if provided or infer
    pipeline_conf = None
    pipeline_source = "default (auto-generated)"
    if pipeline_yml:
        try:
            yml_bytes = download_bytes(pipeline_yml)
            pipeline_conf = yaml.safe_load(yml_bytes)
            pipeline_source = pipeline_yml
        except Exception as exc:
            logger.error(f"Failed to load pipeline YAML: {exc}")
            raise HTTPException(status_code=400, detail=f"Cannot load pipeline YAML: {str(exc)}")
    else:
        name_no_ext = original_filename.rsplit('.', 1)[0]
        guessed_path = f"pipelines/{name_no_ext}.yml"
        try:
            yml_bytes = download_bytes(guessed_path)
            pipeline_conf = yaml.safe_load(yml_bytes)
            pipeline_source = guessed_path
        except Exception:
            pipeline_conf = None  # fallback to automatic pipeline

    # 3) Run pipeline
    try:
        processed = run_pipeline(df, pipeline_conf, target_column=target_column)
        if processed.empty:
            raise ValueError("Pipeline produced empty dataset")
        logger.info(f"Pipeline completed: {len(processed)} rows, {len(processed.columns)} columns")
    except Exception as exc:
        logger.error(f"Pipeline error: {exc}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(exc)}")

    # 4) Store processed CSV to MinIO
    try:
        processed_bytes = processed.to_csv(index=False).encode("utf-8")
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        base_name = original_filename.rsplit('.', 1)[0]
        out_name = f"processed/{base_name}_processed_{timestamp}.csv"
        upload_bytes(out_name, processed_bytes)
        logger.info(f"Stored processed CSV: {out_name}")
    except Exception as exc:
        logger.error(f"Failed to store processed CSV: {exc}")
        raise HTTPException(status_code=500, detail=f"Failed to store processed CSV: {str(exc)}")

    # 5) Prepare preview data (first 10 rows) to send to frontend
    preview_data = processed.head(10).to_dict(orient="records")

    response = {
        "message": "Processing completed successfully",
        "minio_object": out_name,
        "rows": len(processed),
        "columns": len(processed.columns),
        "pipeline_used": pipeline_source,
        "cleaned_data": preview_data,  # frontend can preview first 10 rows
    }

    if target_column:
        response["target_column"] = target_column
        response["feature_columns"] = [c for c in processed.columns if c != target_column]



    # 6) Notify orchestrator that DataPreparer succeeded
    try:
        await publish_step_done(
            "DataPreparer",
            {
                "pipelineId": pipeline_id,   # MUST come from frontend
                "step": "DataPreparer",
                "status": "SUCCESS"
            }
        )
        logger.info("📤 Published DataPreparer SUCCESS to orchestrator")
    except Exception as exc:
        logger.error(f"Failed to notify orchestrator: {exc}")


    
    return response
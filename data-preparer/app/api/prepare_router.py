# app/api/prepare_router.py
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
async def prepare(
        file: UploadFile = File(None),
        minio_object: Optional[str] = Form(None),
        pipeline_yml: Optional[str] = Form(None)
):
    """
    Prepare the dataset. Provide either file OR minio_object.
    Optionally provide pipeline_yml (MinIO path), otherwise attempts to use
    'pipelines/<rawfilename>.yml' if minio_object is provided.
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
        # Validate file type
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

        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        except pd.errors.ParserError as exc:
            logger.error(f"Invalid CSV file uploaded: {exc}")
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(exc)}")
        except Exception as exc:
            logger.error(f"Failed reading uploaded file: {exc}")
            raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(exc)}")

    elif minio_object:
        try:
            raw = download_bytes(minio_object)
            df = pd.read_csv(io.BytesIO(raw))

            if df.empty:
                raise HTTPException(status_code=400, detail="CSV from MinIO contains no data")

            # Extract filename from path (e.g., "raw/myfile.csv" -> "myfile.csv")
            original_filename = minio_object.split('/')[-1]
            logger.info(f"Loaded CSV from MinIO: {minio_object} ({len(df)} rows)")

        except FileNotFoundError:
            logger.error(f"MinIO object not found: {minio_object}")
            raise HTTPException(status_code=404, detail=f"File not found in MinIO: {minio_object}")
        except pd.errors.ParserError as exc:
            logger.error(f"Invalid CSV from MinIO: {exc}")
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(exc)}")
        except Exception as exc:
            logger.error(f"Failed to download CSV from MinIO: {exc}")
            raise HTTPException(status_code=400, detail=f"Cannot download file from MinIO: {str(exc)}")
    else:
        raise HTTPException(status_code=400, detail="Must provide either 'file' or 'minio_object'")

    # 2) Determine pipeline YAML
    pipeline_conf = None
    pipeline_source = "default (auto-generated)"

    if pipeline_yml:
        # Explicit pipeline provided
        try:
            yml_bytes = download_bytes(pipeline_yml)
            pipeline_conf = yaml.safe_load(yml_bytes)

            if not isinstance(pipeline_conf, dict):
                raise ValueError("Pipeline YAML must contain a dictionary")

            pipeline_source = pipeline_yml
            logger.info(f"Loaded explicit pipeline config from: {pipeline_yml}")

        except FileNotFoundError:
            logger.error(f"Pipeline YAML not found: {pipeline_yml}")
            raise HTTPException(status_code=404, detail=f"Pipeline YAML not found: {pipeline_yml}")
        except yaml.YAMLError as exc:
            logger.error(f"Invalid YAML in {pipeline_yml}: {exc}")
            raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(exc)}")
        except Exception as exc:
            logger.error(f"Failed to load pipeline YAML from {pipeline_yml}: {exc}")
            raise HTTPException(status_code=400, detail=f"Cannot load pipeline YAML: {str(exc)}")
    else:
        # Attempt to infer pipeline from filename
        name_no_ext = original_filename.rsplit('.', 1)[0]
        guessed_path = f"pipelines/{name_no_ext}.yml"

        try:
            yml_bytes = download_bytes(guessed_path)
            pipeline_conf = yaml.safe_load(yml_bytes)

            if not isinstance(pipeline_conf, dict):
                raise ValueError("Pipeline YAML must contain a dictionary")

            pipeline_source = guessed_path
            logger.info(f"Auto-loaded pipeline config from: {guessed_path}")

        except FileNotFoundError:
            logger.info(f"No pipeline YAML found at {guessed_path}, will use automatic pipeline")
            pipeline_conf = None
        except yaml.YAMLError as exc:
            logger.warning(f"Invalid YAML in {guessed_path}, using automatic pipeline: {exc}")
            pipeline_conf = None
        except Exception as exc:
            logger.warning(f"Failed to load {guessed_path}, using automatic pipeline: {exc}")
            pipeline_conf = None

    # 3) Run pipeline
    try:
        logger.info(f"Running pipeline with config from: {pipeline_source}")
        logger.debug(f"Pipeline config: {pipeline_conf}")

        processed = run_pipeline(df, pipeline_conf)

        if processed.empty:
            raise ValueError("Pipeline produced empty dataset")

        logger.info(f"Pipeline completed: {len(processed)} rows, {len(processed.columns)} columns")

    except ValueError as exc:
        logger.error(f"Pipeline validation error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))
    except KeyError as exc:
        logger.error(f"Pipeline configuration error - missing key: {exc}")
        raise HTTPException(status_code=400, detail=f"Invalid pipeline config - missing: {str(exc)}")
    except Exception as exc:
        logger.exception("Unexpected pipeline failure")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(exc)}")

    # 4) Store processed CSV to MinIO
    try:
        processed_bytes = processed.to_csv(index=False).encode("utf-8")

        # Create timestamped output name
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        base_name = original_filename.rsplit('.', 1)[0]
        out_name = f"processed/{base_name}_processed_{timestamp}.csv"

        upload_bytes(out_name, processed_bytes)
        logger.info(f"Stored processed CSV: {out_name}")

    except Exception as exc:
        logger.error(f"Failed to store processed CSV: {exc}")
        raise HTTPException(status_code=500, detail=f"Failed to store processed CSV: {str(exc)}")

    return {
        "message": "Processing completed successfully",
        "minio_object": out_name,
        "rows": len(processed),
        "columns": len(processed.columns),
        "pipeline_used": pipeline_source
    }
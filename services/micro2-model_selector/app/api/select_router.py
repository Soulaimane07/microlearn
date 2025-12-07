# app/api/select_router.py
# --------------------------------------------------------------------
# Main API router for model selection functionality.
# Provides endpoints to select appropriate ML models based on dataset
# characteristics and user requirements.
# --------------------------------------------------------------------
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form
from typing import Optional, List
import pandas as pd
import io

from app.services.model_selector import ModelSelectorService
from app.services.dataset_analyzer import DatasetAnalyzer
from app.models.request_models import SelectionRequest
from app.models.response_models import SelectionResponse, ModelCandidate
from app.storage.minio_client import download_bytes
from app.core.logger import logger

router = APIRouter()
selector_service = ModelSelectorService()
analyzer = DatasetAnalyzer()


@router.get("")
async def select_models(
    minio_object: Optional[str] = Query(None, description="Path to prepared dataset in MinIO"),
    metric: str = Query("accuracy", description="Primary metric for model selection (accuracy, f1, rmse, mae, r2)"),
    task_type: Optional[str] = Query(None, description="Task type: classification, regression, clustering (auto-detected if not provided)"),
    max_models: int = Query(5, description="Maximum number of model candidates to return", ge=1, le=20),
    include_deep_learning: bool = Query(False, description="Include deep learning models (CNN, etc.)")
):
    """
    Select appropriate ML models based on dataset characteristics.
    
    Analyzes the dataset and returns a ranked list of model candidates
    suitable for the data type, size, and optimization objective.
    
    Args:
        minio_object: Path to the prepared dataset in MinIO storage
        metric: Evaluation metric to optimize (accuracy, f1, rmse, mae, r2)
        task_type: Override auto-detected task type
        max_models: Maximum number of candidates to return
        include_deep_learning: Whether to include neural network models
    
    Returns:
        SelectionResponse with list of model candidates and dataset analysis
    """
    if not minio_object:
        raise HTTPException(
            status_code=400,
            detail="minio_object parameter is required. Provide path to prepared dataset."
        )
    
    try:
        # Download and load dataset from MinIO
        logger.info(f"Loading dataset from MinIO: {minio_object}")
        raw_data = download_bytes(minio_object)
        df = pd.read_csv(io.BytesIO(raw_data))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Dataset is empty")
        
        logger.info(f"Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Dataset not found in MinIO: {minio_object}")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load dataset: {str(e)}")
    
    # Analyze dataset
    analysis = analyzer.analyze(df, task_type)
    logger.info(f"Dataset analysis complete: task_type={analysis['task_type']}, target={analysis.get('target_column')}")
    
    # Select models based on analysis
    candidates = selector_service.select_models(
        analysis=analysis,
        metric=metric,
        max_models=max_models,
        include_deep_learning=include_deep_learning
    )
    
    logger.info(f"Selected {len(candidates)} model candidates")
    
    return SelectionResponse(
        dataset_analysis=analysis,
        metric=metric,
        candidates=candidates,
        minio_object=minio_object
    )


@router.post("")
async def select_models_with_upload(
    file: UploadFile = File(..., description="CSV file to analyze"),
    metric: str = Form("accuracy", description="Primary metric for model selection"),
    task_type: Optional[str] = Form(None, description="Task type override"),
    target_column: Optional[str] = Form(None, description="Target column name for supervised learning"),
    max_models: int = Form(5, description="Maximum number of candidates"),
    include_deep_learning: bool = Form(False, description="Include deep learning models")
):
    """
    Select models by uploading a dataset directly.
    
    Alternative endpoint that accepts file upload instead of MinIO reference.
    Useful for testing and quick analysis without storing data first.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        raw = await file.read()
        df = pd.read_csv(io.BytesIO(raw))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV contains no data")
        
        logger.info(f"Loaded CSV from upload: {file.filename} ({len(df)} rows)")
        
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to read uploaded file: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")
    
    # Analyze dataset
    analysis = analyzer.analyze(df, task_type, target_column)
    
    # Select models
    candidates = selector_service.select_models(
        analysis=analysis,
        metric=metric,
        max_models=max_models,
        include_deep_learning=include_deep_learning
    )
    
    return SelectionResponse(
        dataset_analysis=analysis,
        metric=metric,
        candidates=candidates,
        minio_object=None
    )


@router.post("/analyze")
async def analyze_dataset(
    file: UploadFile = File(...),
    target_column: Optional[str] = Form(None)
):
    """
    Analyze a dataset without selecting models.
    
    Returns detailed information about the dataset structure,
    data types, statistics, and recommended task type.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        raw = await file.read()
        df = pd.read_csv(io.BytesIO(raw))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV contains no data")
        
        analysis = analyzer.analyze(df, target_column=target_column)
        return analysis
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

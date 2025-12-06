# app/api/models_router.py
# --------------------------------------------------------------------
# Trained models management endpoints.
# --------------------------------------------------------------------
from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional
from datetime import datetime

from app.models.response_models import TrainedModelInfo, ModelListResponse
from app.storage.postgres_client import get_postgres_client
from app.storage.minio_client import get_minio_client, download_model_bytes
from app.core.logger import logger

router = APIRouter()


@router.get("/", response_model=ModelListResponse)
async def list_trained_models(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Results per page")
):
    """
    List all trained models.
    
    Returns paginated list of successfully trained models with their metrics.
    
    Args:
        page: Page number (starting from 1)
        page_size: Number of results per page
        
    Returns:
        ModelListResponse with list of trained models
    """
    logger.debug(f"Listing trained models: page={page}, page_size={page_size}")
    
    postgres = get_postgres_client()
    
    # Get completed jobs only
    jobs = postgres.list_jobs(status="completed", limit=page_size)
    
    models = []
    for job in jobs:
        if job.get('final_model_path'):
            # Extract model name from path
            model_path = job['final_model_path']
            object_name = model_path.split('/')[-1] if '/' in model_path else model_path
            
            # Get file size
            minio = get_minio_client()
            file_size = minio.get_object_size(object_name.replace('trained-models/', ''))
            
            # Calculate training duration
            duration = None
            if job.get('started_at') and job.get('completed_at'):
                delta = job['completed_at'] - job['started_at']
                duration = str(delta)
            
            model_info = TrainedModelInfo(
                model_id=job['model_id'],
                job_id=job['job_id'],
                model_name=job['model_id'].replace('_', ' ').title(),
                task_type=job['task_type'],
                minio_path=model_path,
                file_size_mb=file_size,
                metrics=job.get('best_metrics') or {},
                hyperparameters=job.get('hyperparameters') or {},
                training_duration=duration,
                created_at=job['completed_at'] or job['created_at'],
                mlflow_run_id=job.get('mlflow_run_id')
            )
            
            models.append(model_info)
    
    return ModelListResponse(
        models=models,
        total=len(models),
        page=page,
        page_size=page_size
    )


@router.get("/{job_id}", response_model=TrainedModelInfo)
async def get_trained_model(job_id: str):
    """
    Get details of a specific trained model.
    
    Args:
        job_id: Training job identifier
        
    Returns:
        TrainedModelInfo with model details
    """
    logger.debug(f"Getting trained model: {job_id}")
    
    postgres = get_postgres_client()
    job = postgres.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    if job['status'] != 'completed' or not job.get('final_model_path'):
        raise HTTPException(
            status_code=400,
            detail=f"Job {job_id} has not completed successfully"
        )
    
    # Get file size
    model_path = job['final_model_path']
    object_name = model_path.split('/')[-1] if '/' in model_path else model_path
    
    minio = get_minio_client()
    file_size = minio.get_object_size(object_name.replace('trained-models/', ''))
    
    # Calculate duration
    duration = None
    if job.get('started_at') and job.get('completed_at'):
        delta = job['completed_at'] - job['started_at']
        duration = str(delta)
    
    return TrainedModelInfo(
        model_id=job['model_id'],
        job_id=job['job_id'],
        model_name=job['model_id'].replace('_', ' ').title(),
        task_type=job['task_type'],
        minio_path=model_path,
        file_size_mb=file_size,
        metrics=job.get('best_metrics') or {},
        hyperparameters=job.get('hyperparameters') or {},
        training_duration=duration,
        created_at=job['completed_at'] or job['created_at'],
        mlflow_run_id=job.get('mlflow_run_id')
    )


@router.get("/{job_id}/download")
async def download_trained_model(job_id: str):
    """
    Download trained model file.
    
    Returns the pickled model file as binary data.
    
    Args:
        job_id: Training job identifier
        
    Returns:
        Binary model file
    """
    logger.info(f"Downloading model: {job_id}")
    
    postgres = get_postgres_client()
    job = postgres.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    if job['status'] != 'completed' or not job.get('final_model_path'):
        raise HTTPException(
            status_code=400,
            detail=f"Job {job_id} has not completed successfully"
        )
    
    # Extract object name from path
    model_path = job['final_model_path']
    object_name = model_path.replace('trained-models/', '')
    
    try:
        # Download from MinIO
        model_bytes = download_model_bytes(object_name)
        
        # Return as binary response
        return Response(
            content=model_bytes,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={job_id}_model.pkl"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.delete("/{job_id}")
async def delete_trained_model(job_id: str):
    """
    Delete a trained model.
    
    Removes the model from MinIO and marks the job.
    
    Args:
        job_id: Training job identifier
        
    Returns:
        Success message
    """
    logger.info(f"Deleting model: {job_id}")
    
    postgres = get_postgres_client()
    job = postgres.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    if not job.get('final_model_path'):
        raise HTTPException(status_code=400, detail="No model to delete")
    
    # Extract object name
    model_path = job['final_model_path']
    object_name = model_path.replace('trained-models/', '')
    
    # Delete from MinIO
    minio = get_minio_client()
    success = minio.delete_model(object_name)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete model from storage")
    
    # Update job to clear model path
    postgres.update_job_status(job_id, job['status'], final_model_path=None)
    
    logger.info(f"Deleted model for job: {job_id}")
    
    return {"message": f"Model for job {job_id} deleted successfully"}

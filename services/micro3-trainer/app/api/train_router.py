# app/api/train_router.py
# --------------------------------------------------------------------
# Training job management endpoints.
# --------------------------------------------------------------------
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.request_models import TrainingRequest
from app.models.response_models import TrainingJobResponse, TrainingProgressResponse, JobStatus
from app.services.training_orchestrator import get_orchestrator
from app.core.logger import logger

router = APIRouter()


@router.post("", response_model=TrainingJobResponse)
async def start_training(request: TrainingRequest):
    """
    Start a new training job.
    
    Submits a model for training with the specified dataset and parameters.
    Training runs asynchronously in the background.
    
    Args:
        request: Training configuration
        
    Returns:
        TrainingJobResponse with job ID and initial status
    """
    logger.info(f"Received training request: model={request.model_id}, data={request.data_id}")
    
    try:
        orchestrator = get_orchestrator()
        response = await orchestrator.submit_training_job(request)
        
        logger.info(f"Training job submitted: {response.job_id}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to submit training job: {e}")
        raise HTTPException(status_code=500, detail=f"Training submission failed: {str(e)}")


@router.get("/{job_id}", response_model=TrainingJobResponse)
async def get_job_status(job_id: str):
    """
    Get training job status.
    
    Returns current status, progress, and metrics for a training job.
    
    Args:
        job_id: Training job identifier
        
    Returns:
        TrainingJobResponse with current status
    """
    logger.debug(f"Getting status for job: {job_id}")
    
    orchestrator = get_orchestrator()
    job = orchestrator.get_job_status(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    return job


@router.get("/{job_id}/progress", response_model=TrainingProgressResponse)
async def get_job_progress(job_id: str):
    """
    Get detailed training progress.
    
    Returns epoch-by-epoch metrics and checkpoints.
    
    Args:
        job_id: Training job identifier
        
    Returns:
        TrainingProgressResponse with detailed progress
    """
    from app.storage.postgres_client import get_postgres_client
    
    orchestrator = get_orchestrator()
    job = orchestrator.get_job_status(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    # Get recent metrics
    postgres = get_postgres_client()
    metrics_list = postgres.get_job_metrics(job_id, limit=10)
    
    # Get checkpoints
    checkpoints_list = postgres.get_job_checkpoints(job_id)
    
    from app.models.response_models import TrainingMetrics, CheckpointInfo
    
    # Convert to response models
    recent_metrics = [
        TrainingMetrics(
            epoch=m['epoch'],
            train_loss=m.get('train_loss') or 0.0,
            val_loss=m.get('val_loss'),
            train_accuracy=m.get('train_accuracy'),
            val_accuracy=m.get('val_accuracy'),
            learning_rate=m.get('learning_rate') or 0.001,
            additional_metrics=m.get('additional_metrics') or {}
        )
        for m in metrics_list
    ]
    
    checkpoints = [
        CheckpointInfo(
            checkpoint_id=c['checkpoint_id'],
            epoch=c['epoch'],
            minio_path=c['minio_path'],
            metrics=c.get('metrics') or {},
            created_at=c['created_at'],
            file_size_mb=c.get('file_size_mb')
        )
        for c in checkpoints_list
    ]
    
    return TrainingProgressResponse(
        job_id=job_id,
        status=job.status,
        current_epoch=job.current_epoch or 0,
        total_epochs=job.total_epochs,
        progress_percentage=job.progress_percentage or 0.0,
        recent_metrics=recent_metrics,
        checkpoints=checkpoints
    )


@router.get("", response_model=list[TrainingJobResponse])
async def list_training_jobs(
    status: Optional[str] = Query(None, description="Filter by job status"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results to return")
):
    """
    List training jobs.
    
    Returns a list of training jobs, optionally filtered by status.
    
    Args:
        status: Optional status filter (pending, running, completed, failed)
        limit: Maximum number of results
        
    Returns:
        List of TrainingJobResponse objects
    """
    logger.debug(f"Listing jobs: status={status}, limit={limit}")
    
    orchestrator = get_orchestrator()
    jobs = orchestrator.list_jobs(status=status, limit=limit)
    
    return jobs


@router.delete("/{job_id}")
async def cancel_training_job(job_id: str):
    """
    Cancel a running training job.
    
    Args:
        job_id: Training job identifier
        
    Returns:
        Success message
    """
    from app.storage.postgres_client import get_postgres_client
    
    orchestrator = get_orchestrator()
    job = orchestrator.get_job_status(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    if job.status not in [JobStatus.PENDING, JobStatus.RUNNING]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job in status: {job.status.value}"
        )
    
    # Update status to cancelled
    postgres = get_postgres_client()
    postgres.update_job_status(job_id, JobStatus.CANCELLED.value)
    
    logger.info(f"Cancelled training job: {job_id}")
    
    return {"message": f"Job {job_id} cancelled successfully"}

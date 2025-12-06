# app/models/response_models.py
# --------------------------------------------------------------------
# Pydantic response models for Trainer API.
# --------------------------------------------------------------------
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    """Training job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TrainingMetrics(BaseModel):
    """Training metrics for a specific epoch"""
    epoch: int
    train_loss: float
    val_loss: Optional[float] = None
    train_accuracy: Optional[float] = None
    val_accuracy: Optional[float] = None
    learning_rate: float
    additional_metrics: Dict[str, float] = Field(default_factory=dict)


class CheckpointInfo(BaseModel):
    """Checkpoint information"""
    checkpoint_id: str
    epoch: int
    minio_path: str
    metrics: Dict[str, float]
    created_at: datetime
    file_size_mb: Optional[float] = None


class TrainingJobResponse(BaseModel):
    """Response for training job submission"""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    model_id: str = Field(..., description="Model being trained")
    data_id: str = Field(..., description="Dataset ID")
    
    created_at: datetime = Field(..., description="Job creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Training start time")
    completed_at: Optional[datetime] = Field(None, description="Training completion time")
    
    # Progress tracking
    current_epoch: Optional[int] = Field(None, description="Current training epoch")
    total_epochs: int = Field(..., description="Total epochs")
    progress_percentage: Optional[float] = Field(None, ge=0, le=100, description="Progress %")
    
    # Resources
    gpu_allocated: Optional[str] = Field(None, description="GPU device ID")
    
    # MLflow
    mlflow_run_id: Optional[str] = Field(None, description="MLflow run ID")
    mlflow_experiment_id: Optional[str] = Field(None, description="MLflow experiment ID")
    
    # Results
    best_metrics: Optional[Dict[str, float]] = Field(None, description="Best metrics achieved")
    final_model_path: Optional[str] = Field(None, description="MinIO path to trained model")
    
    # Error tracking
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "train_123abc",
                "status": "running",
                "model_id": "xgboost_classifier",
                "data_id": "dataset_456",
                "created_at": "2025-12-02T10:00:00",
                "current_epoch": 45,
                "total_epochs": 100,
                "progress_percentage": 45.0,
                "gpu_allocated": "cuda:0"
            }
        }


class TrainingProgressResponse(BaseModel):
    """Detailed training progress"""
    job_id: str
    status: JobStatus
    current_epoch: int
    total_epochs: int
    progress_percentage: float
    
    recent_metrics: List[TrainingMetrics] = Field(default_factory=list, description="Last 10 epoch metrics")
    checkpoints: List[CheckpointInfo] = Field(default_factory=list, description="Saved checkpoints")
    
    estimated_time_remaining: Optional[str] = Field(None, description="ETA in human-readable format")
    elapsed_time: Optional[str] = Field(None, description="Time elapsed")


class TrainedModelInfo(BaseModel):
    """Information about a trained model"""
    model_id: str
    job_id: str
    model_name: str
    task_type: str
    
    minio_path: str
    file_size_mb: float
    
    metrics: Dict[str, float]
    hyperparameters: Dict[str, Any]
    
    training_duration: Optional[str] = None
    created_at: datetime
    
    mlflow_run_id: Optional[str] = None


class ModelListResponse(BaseModel):
    """List of trained models"""
    models: List[TrainedModelInfo]
    total: int
    page: int
    page_size: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "ok"
    service: str = "trainer"
    gpu_available: bool = False
    ray_initialized: bool = False
    mlflow_connected: bool = False
    postgres_connected: bool = False
    minio_connected: bool = False

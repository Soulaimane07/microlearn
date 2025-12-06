# app/models/request_models.py
# --------------------------------------------------------------------
# Pydantic request models for Trainer API.
# --------------------------------------------------------------------
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from enum import Enum


class TaskType(str, Enum):
    """ML task types"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"


class TrainingRequest(BaseModel):
    """Request to train a model"""
    model_id: str = Field(..., description="Model identifier from ModelSelector")
    data_id: str = Field(..., description="Dataset ID or MinIO path")
    task_type: TaskType = Field(..., description="ML task type")
    
    # Training parameters
    epochs: Optional[int] = Field(100, ge=1, le=1000, description="Number of training epochs")
    batch_size: Optional[int] = Field(32, ge=1, le=512, description="Batch size")
    learning_rate: Optional[float] = Field(0.001, gt=0, lt=1, description="Learning rate")
    
    # Hyperparameters (model-specific)
    hyperparameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Model hyperparameters")
    
    # Target column
    target_column: Optional[str] = Field(None, description="Target column name")
    
    # Resource allocation
    use_gpu: bool = Field(True, description="Use GPU if available")
    num_workers: int = Field(4, ge=0, le=32, description="DataLoader workers")
    
    # MLflow tracking
    experiment_name: Optional[str] = Field(None, description="MLflow experiment name")
    run_name: Optional[str] = Field(None, description="MLflow run name")
    tags: Optional[Dict[str, str]] = Field(default_factory=dict, description="MLflow tags")
    
    # Early stopping
    early_stopping: bool = Field(True, description="Enable early stopping")
    patience: Optional[int] = Field(10, ge=1, description="Early stopping patience")
    
    @field_validator('model_id')
    @classmethod
    def validate_model_id(cls, v):
        if not v or len(v) < 3:
            raise ValueError("model_id must be at least 3 characters")
        return v


class TrainingJobQuery(BaseModel):
    """Query parameters for job status"""
    job_id: Optional[str] = Field(None, description="Specific job ID")
    status: Optional[str] = Field(None, description="Filter by status")
    limit: int = Field(10, ge=1, le=100, description="Max results")


class ModelDeployRequest(BaseModel):
    """Request to deploy a trained model"""
    job_id: str = Field(..., description="Training job ID")
    deployment_name: str = Field(..., description="Deployment name")
    endpoint_url: Optional[str] = Field(None, description="Custom endpoint URL")

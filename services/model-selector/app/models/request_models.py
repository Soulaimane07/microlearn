# app/models/request_models.py
# --------------------------------------------------------------------
# Pydantic request models for ModelSelector API.
# --------------------------------------------------------------------
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SelectionRequest(BaseModel):
    """Request model for model selection"""
    minio_object: Optional[str] = Field(None, description="Path to dataset in MinIO")
    metric: str = Field("accuracy", description="Optimization metric")
    task_type: Optional[str] = Field(None, description="Task type override")
    target_column: Optional[str] = Field(None, description="Target column name")
    max_models: int = Field(5, ge=1, le=20, description="Max candidates to return")
    include_deep_learning: bool = Field(False, description="Include DL models")
    
    # Optional constraints
    max_training_time: Optional[int] = Field(None, description="Max training time in seconds")
    require_interpretability: bool = Field(False, description="Prefer interpretable models")
    exclude_models: Optional[List[str]] = Field(None, description="Models to exclude")


class DatasetConfig(BaseModel):
    """Configuration for dataset analysis"""
    target_column: Optional[str] = None
    id_columns: Optional[List[str]] = None
    date_columns: Optional[List[str]] = None
    categorical_columns: Optional[List[str]] = None
    numeric_columns: Optional[List[str]] = None


class ModelFilterRequest(BaseModel):
    """Request model for filtering available models"""
    task_types: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    min_interpretability: Optional[str] = None
    max_complexity: Optional[str] = None
    supports_gpu: Optional[bool] = None

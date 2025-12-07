# app/models/response_models.py
# --------------------------------------------------------------------
# Pydantic response models for ModelSelector API.
# --------------------------------------------------------------------
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ModelCandidate(BaseModel):
    """A candidate model for selection"""
    model_id: str = Field(..., description="Unique model identifier")
    model_name: str = Field(..., description="Human-readable model name")
    model_class: str = Field(..., description="Full class path (e.g., sklearn.ensemble.RandomForestClassifier)")
    category: str = Field(..., description="Model category (tree, ensemble, linear, svm, neural_network)")
    
    # Scoring
    compatibility_score: float = Field(..., ge=0, le=1, description="How well suited for this dataset (0-1)")
    expected_performance: Optional[str] = Field(None, description="Expected performance level")
    ranking: int = Field(..., description="Rank among candidates")
    
    # Characteristics
    interpretability: str = Field(..., description="Interpretability level: high, medium, low")
    training_complexity: str = Field(..., description="Training complexity: low, medium, high")
    supports_gpu: bool = Field(False, description="Whether model supports GPU acceleration")
    
    # Parameters
    default_params: Dict[str, Any] = Field(default_factory=dict, description="Default hyperparameters")
    tunable_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for hyperopt")
    
    # Recommendations
    recommended_for: List[str] = Field(default_factory=list, description="Scenarios where model excels")
    limitations: List[str] = Field(default_factory=list, description="Known limitations")


class DatasetAnalysis(BaseModel):
    """Analysis results for a dataset"""
    n_rows: int
    n_columns: int
    n_features: int
    
    task_type: str = Field(..., description="Detected task type")
    target_column: Optional[str] = None
    target_type: Optional[str] = None
    n_classes: Optional[int] = None
    
    numeric_columns: List[str] = Field(default_factory=list)
    categorical_columns: List[str] = Field(default_factory=list)
    datetime_columns: List[str] = Field(default_factory=list)
    
    has_missing_values: bool = False
    missing_percentage: float = 0.0
    
    data_size_category: str = Field("medium", description="small, medium, large, very_large")
    feature_target_ratio: Optional[float] = None
    
    warnings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class SelectionResponse(BaseModel):
    """Response from model selection endpoint"""
    dataset_analysis: Dict[str, Any] = Field(..., description="Dataset analysis results")
    metric: str = Field(..., description="Selected optimization metric")
    candidates: List[ModelCandidate] = Field(..., description="Ranked list of model candidates")
    minio_object: Optional[str] = Field(None, description="Source dataset path")
    
    # Summary
    top_recommendation: Optional[str] = Field(None, description="Top recommended model")
    selection_rationale: Optional[str] = Field(None, description="Explanation for selection")


class ModelInfo(BaseModel):
    """Detailed information about a model"""
    model_id: str
    model_name: str
    model_class: str
    category: str
    
    description: str
    task_types: List[str]
    
    interpretability: str
    training_complexity: str
    prediction_speed: str
    memory_usage: str
    supports_gpu: bool
    
    default_params: Dict[str, Any]
    tunable_params: Dict[str, Any]
    
    suitable_for: List[str]
    not_suitable_for: List[str]
    
    sklearn_compatible: bool = True
    requires_scaling: bool = False
    handles_missing: bool = False
    handles_categorical: bool = False


class CategoryInfo(BaseModel):
    """Information about a model category"""
    category_id: str
    category_name: str
    description: str
    model_count: int
    models: List[str]

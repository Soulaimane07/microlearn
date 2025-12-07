# app/api/models_router.py
# --------------------------------------------------------------------
# API router for model catalog management.
# Provides endpoints to browse, add, and manage available ML models.
# --------------------------------------------------------------------
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from app.services.model_catalog import ModelCatalog
from app.models.response_models import ModelInfo
from app.core.logger import logger

router = APIRouter()
catalog = ModelCatalog()


@router.get("/")
async def list_models(
    task_type: Optional[str] = Query(None, description="Filter by task type: classification, regression, clustering"),
    category: Optional[str] = Query(None, description="Filter by category: tree, linear, ensemble, svm, neural_network")
):
    """
    List all available models in the catalog.
    
    Returns a list of all supported ML models with their metadata,
    optionally filtered by task type or category.
    """
    models = catalog.list_models(task_type=task_type, category=category)
    logger.info(f"Listed {len(models)} models (task_type={task_type}, category={category})")
    return {"models": models, "count": len(models)}


@router.get("/{model_id}")
async def get_model(model_id: str):
    """
    Get detailed information about a specific model.
    
    Returns comprehensive metadata including parameters,
    suitable data types, complexity, and usage recommendations.
    """
    model = catalog.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail=f"Model not found: {model_id}")
    return model


@router.get("/categories/")
async def list_categories():
    """
    List all model categories.
    
    Returns available model categories (tree-based, linear, ensemble, etc.)
    with counts of models in each category.
    """
    return catalog.list_categories()


@router.get("/metrics/")
async def list_metrics():
    """
    List supported evaluation metrics.
    
    Returns all metrics that can be used for model selection
    along with their descriptions and applicable task types.
    """
    return {
        "classification": [
            {"name": "accuracy", "description": "Overall correctness of predictions"},
            {"name": "f1", "description": "Harmonic mean of precision and recall"},
            {"name": "precision", "description": "Ratio of true positives to predicted positives"},
            {"name": "recall", "description": "Ratio of true positives to actual positives"},
            {"name": "roc_auc", "description": "Area under ROC curve"},
            {"name": "log_loss", "description": "Negative log-likelihood of predictions"}
        ],
        "regression": [
            {"name": "rmse", "description": "Root Mean Squared Error"},
            {"name": "mae", "description": "Mean Absolute Error"},
            {"name": "r2", "description": "Coefficient of determination"},
            {"name": "mape", "description": "Mean Absolute Percentage Error"}
        ],
        "clustering": [
            {"name": "silhouette", "description": "Silhouette coefficient"},
            {"name": "calinski_harabasz", "description": "Calinski-Harabasz Index"},
            {"name": "davies_bouldin", "description": "Davies-Bouldin Index"}
        ]
    }


@router.get("/recommendations/{task_type}")
async def get_recommendations(
    task_type: str,
    data_size: Optional[str] = Query("medium", description="Dataset size: small, medium, large"),
    interpretability: Optional[str] = Query("medium", description="Required interpretability: low, medium, high")
):
    """
    Get model recommendations for a specific task type.
    
    Provides tailored recommendations based on task type,
    data size, and interpretability requirements.
    """
    if task_type not in ["classification", "regression", "clustering"]:
        raise HTTPException(
            status_code=400,
            detail="task_type must be one of: classification, regression, clustering"
        )
    
    recommendations = catalog.get_recommendations(
        task_type=task_type,
        data_size=data_size,
        interpretability=interpretability
    )
    
    return {
        "task_type": task_type,
        "data_size": data_size,
        "interpretability": interpretability,
        "recommendations": recommendations
    }

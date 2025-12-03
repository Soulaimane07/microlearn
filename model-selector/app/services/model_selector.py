# app/services/model_selector.py
# --------------------------------------------------------------------
# Core model selection service.
# Evaluates dataset characteristics and selects appropriate ML models.
# --------------------------------------------------------------------
from typing import Dict, Any, List, Optional

from app.services.model_catalog import ModelCatalog
from app.models.response_models import ModelCandidate
from app.core.logger import logger


class ModelSelectorService:
    """Service for selecting appropriate ML models based on dataset analysis"""
    
    def __init__(self):
        self.catalog = ModelCatalog()
    
    def select_models(
        self,
        analysis: Dict[str, Any],
        metric: str = "accuracy",
        max_models: int = 5,
        include_deep_learning: bool = False
    ) -> List[ModelCandidate]:
        """
        Select appropriate models based on dataset analysis.
        
        Args:
            analysis: Dataset analysis from DatasetAnalyzer
            metric: Primary metric to optimize
            max_models: Maximum number of candidates to return
            include_deep_learning: Whether to include neural network models
            
        Returns:
            List of ModelCandidate objects ranked by compatibility
        """
        task_type = analysis.get("task_type", "classification")
        logger.info(f"Selecting models for task_type={task_type}, metric={metric}")
        
        # Get all models for this task type
        available_models = self.catalog.list_models(task_type=task_type)
        
        # Filter out deep learning if not requested
        if not include_deep_learning:
            available_models = [m for m in available_models if m["category"] != "neural_network"]
        
        # Score each model based on dataset characteristics
        scored_models = []
        for model in available_models:
            score = self._calculate_compatibility_score(model, analysis, metric)
            scored_models.append((model, score))
        
        # Sort by score descending
        scored_models.sort(key=lambda x: x[1], reverse=True)
        
        # Convert to ModelCandidate objects
        candidates = []
        for rank, (model, score) in enumerate(scored_models[:max_models], 1):
            candidate = self._create_candidate(model, score, rank, analysis)
            candidates.append(candidate)
        
        logger.info(f"Selected {len(candidates)} model candidates")
        return candidates
    
    def _calculate_compatibility_score(
        self,
        model: Dict[str, Any],
        analysis: Dict[str, Any],
        metric: str
    ) -> float:
        """
        Calculate compatibility score for a model given dataset characteristics.
        
        Score is based on:
        - Data size compatibility
        - Feature types compatibility  
        - Missing value handling
        - Performance characteristics
        - Metric optimization suitability
        """
        score = 0.5  # Base score
        
        data_size = analysis.get("data_size_category", "medium")
        n_features = analysis.get("n_features", 0)
        n_rows = analysis.get("n_rows", 0)
        has_missing = analysis.get("has_missing_values", False)
        has_categorical = len(analysis.get("categorical_columns", [])) > 0
        is_imbalanced = analysis.get("is_imbalanced", False)
        
        # 1. Data size compatibility (0-0.2)
        if data_size == "small":
            # Prefer simpler models for small datasets
            if model["training_complexity"] in ["very_low", "low"]:
                score += 0.15
            elif model["training_complexity"] == "medium":
                score += 0.1
            # Penalize complex models
            if model["training_complexity"] == "high":
                score -= 0.1
        
        elif data_size == "medium":
            # Most models work well
            score += 0.1
        
        elif data_size in ["large", "very_large"]:
            # Prefer scalable models
            if model["prediction_speed"] in ["fast", "very_fast"]:
                score += 0.15
            if model["memory_usage"] in ["low", "very_low"]:
                score += 0.05
            # Penalize slow models
            if model["prediction_speed"] == "slow":
                score -= 0.15
        
        # 2. Missing value handling (0-0.1)
        if has_missing:
            if model.get("handles_missing", False):
                score += 0.1
            else:
                score -= 0.05
        
        # 3. Categorical feature handling (0-0.05)
        if has_categorical:
            if model.get("handles_categorical", False):
                score += 0.05
        
        # 4. Imbalanced data handling (0-0.1)
        if is_imbalanced:
            # Tree-based models handle imbalance better
            if model["category"] in ["tree", "ensemble"]:
                score += 0.1
            # Linear models struggle more
            if model["category"] == "linear":
                score -= 0.05
        
        # 5. Feature count considerations (0-0.1)
        if n_features > 100:
            # High dimensionality - prefer models that handle it well
            if model["model_id"] in ["random_forest_classifier", "random_forest_regressor",
                                      "xgboost_classifier", "xgboost_regressor",
                                      "lightgbm_classifier", "lightgbm_regressor"]:
                score += 0.1
            # Penalize SVM and KNN for high dimensionality
            if model["category"] in ["svm", "instance_based"]:
                score -= 0.1
        
        # 6. Model-specific bonuses
        # XGBoost/LightGBM are generally top performers
        if model["model_id"] in ["xgboost_classifier", "xgboost_regressor",
                                  "lightgbm_classifier", "lightgbm_regressor"]:
            score += 0.1
        
        # Random Forest is a great default choice
        if model["model_id"] in ["random_forest_classifier", "random_forest_regressor"]:
            score += 0.08
        
        # 7. Metric-specific adjustments
        if metric in ["accuracy", "f1", "precision", "recall"]:
            # Classification metrics
            if model["category"] == "ensemble":
                score += 0.05
        
        elif metric in ["rmse", "mae", "r2"]:
            # Regression metrics
            if model["category"] == "ensemble":
                score += 0.05
        
        # Ensure score stays in valid range
        return max(0.0, min(1.0, score))
    
    def _create_candidate(
        self,
        model: Dict[str, Any],
        score: float,
        rank: int,
        analysis: Dict[str, Any]
    ) -> ModelCandidate:
        """Create a ModelCandidate from model info and score"""
        
        # Determine expected performance based on score
        if score >= 0.8:
            expected_performance = "excellent"
        elif score >= 0.6:
            expected_performance = "good"
        elif score >= 0.4:
            expected_performance = "moderate"
        else:
            expected_performance = "fair"
        
        return ModelCandidate(
            model_id=model["model_id"],
            model_name=model["model_name"],
            model_class=model["model_class"],
            category=model["category"],
            compatibility_score=round(score, 3),
            expected_performance=expected_performance,
            ranking=rank,
            interpretability=model["interpretability"],
            training_complexity=model["training_complexity"],
            supports_gpu=model.get("supports_gpu", False),
            default_params=model.get("default_params", {}),
            tunable_params=model.get("tunable_params", {}),
            recommended_for=model.get("suitable_for", []),
            limitations=model.get("not_suitable_for", [])
        )
    
    def get_model_details(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model"""
        return self.catalog.get_model(model_id)
    
    def explain_selection(
        self,
        candidates: List[ModelCandidate],
        analysis: Dict[str, Any]
    ) -> str:
        """Generate human-readable explanation of model selection"""
        if not candidates:
            return "No suitable models found for this dataset."
        
        top = candidates[0]
        task_type = analysis.get("task_type", "unknown")
        size = analysis.get("data_size_category", "unknown")
        
        explanation = f"For this {size} {task_type} dataset, "
        explanation += f"the top recommendation is **{top.model_name}** "
        explanation += f"(compatibility score: {top.compatibility_score:.2f}). "
        
        if top.model_id in ["xgboost_classifier", "xgboost_regressor",
                            "lightgbm_classifier", "lightgbm_regressor"]:
            explanation += "Gradient boosting models typically achieve state-of-the-art results on tabular data. "
        elif top.model_id in ["random_forest_classifier", "random_forest_regressor"]:
            explanation += "Random Forest provides a good balance of accuracy and interpretability. "
        elif top.model_id in ["logistic_regression", "linear_regression"]:
            explanation += "Linear models offer high interpretability and fast training. "
        
        if analysis.get("has_missing_values"):
            explanation += "The dataset contains missing values. "
        
        if analysis.get("is_imbalanced"):
            explanation += "Class imbalance was detected - consider using class weights. "
        
        return explanation

# tests/test_catalog.py
# --------------------------------------------------------------------
# Tests for the model catalog service.
# --------------------------------------------------------------------
import pytest

from app.services.model_catalog import ModelCatalog


class TestModelCatalogService:
    """Unit tests for ModelCatalog service"""
    
    @pytest.fixture
    def catalog(self):
        return ModelCatalog()
    
    def test_catalog_initialization(self, catalog):
        """Test that catalog initializes with models"""
        models = catalog.list_models()
        assert len(models) > 0
    
    def test_classification_models_exist(self, catalog):
        """Test that classification models are available"""
        models = catalog.list_models(task_type="classification")
        assert len(models) > 0
        
        # Check for essential models
        model_ids = [m["model_id"] for m in models]
        assert "random_forest_classifier" in model_ids
        assert "logistic_regression" in model_ids
        assert "xgboost_classifier" in model_ids
    
    def test_regression_models_exist(self, catalog):
        """Test that regression models are available"""
        models = catalog.list_models(task_type="regression")
        assert len(models) > 0
        
        model_ids = [m["model_id"] for m in models]
        assert "random_forest_regressor" in model_ids
        assert "linear_regression" in model_ids
    
    def test_clustering_models_exist(self, catalog):
        """Test that clustering models are available"""
        models = catalog.list_models(task_type="clustering")
        assert len(models) > 0
        
        model_ids = [m["model_id"] for m in models]
        assert "kmeans" in model_ids
        assert "dbscan" in model_ids
    
    def test_filter_by_category(self, catalog):
        """Test filtering models by category"""
        ensemble_models = catalog.list_models(category="ensemble")
        assert len(ensemble_models) > 0
        assert all(m["category"] == "ensemble" for m in ensemble_models)
        
        linear_models = catalog.list_models(category="linear")
        assert len(linear_models) > 0
        assert all(m["category"] == "linear" for m in linear_models)
    
    def test_combined_filter(self, catalog):
        """Test filtering by both task type and category"""
        models = catalog.list_models(task_type="classification", category="ensemble")
        assert len(models) > 0
        assert all(
            m["category"] == "ensemble" and "classification" in m["task_types"]
            for m in models
        )
    
    def test_get_model_by_id(self, catalog):
        """Test getting a specific model by ID"""
        model = catalog.get_model("random_forest_classifier")
        assert model is not None
        assert model["model_id"] == "random_forest_classifier"
        assert model["model_name"] == "Random Forest Classifier"
        assert "sklearn.ensemble.RandomForestClassifier" == model["model_class"]
    
    def test_get_nonexistent_model(self, catalog):
        """Test getting a model that doesn't exist"""
        model = catalog.get_model("nonexistent_model_xyz")
        assert model is None
    
    def test_model_has_required_fields(self, catalog):
        """Test that models have all required fields"""
        required_fields = [
            "model_id", "model_name", "model_class", "category",
            "task_types", "interpretability", "training_complexity",
            "default_params", "tunable_params"
        ]
        
        models = catalog.list_models()
        for model in models:
            for field in required_fields:
                assert field in model, f"Model {model['model_id']} missing field {field}"
    
    def test_list_categories(self, catalog):
        """Test listing model categories"""
        categories = catalog.list_categories()
        assert len(categories) > 0
        assert "ensemble" in categories
        assert "linear" in categories
        assert "svm" in categories
        
        # Check category structure
        for cat_id, cat_info in categories.items():
            assert "category_id" in cat_info
            assert "category_name" in cat_info
            assert "model_count" in cat_info
            assert "models" in cat_info
    
    def test_recommendations(self, catalog):
        """Test model recommendations"""
        recommendations = catalog.get_recommendations(
            task_type="classification",
            data_size="medium",
            interpretability="medium"
        )
        
        assert len(recommendations) > 0
        assert len(recommendations) <= 5  # Should return top 5
        
        # Check that recommendations have scores
        for rec in recommendations:
            assert "recommendation_score" in rec
    
    def test_recommendations_for_large_data(self, catalog):
        """Test recommendations favor scalable models for large data"""
        recommendations = catalog.get_recommendations(
            task_type="classification",
            data_size="large",
            interpretability="low"
        )
        
        # Should prefer fast models for large data
        top_model = recommendations[0]
        assert top_model["prediction_speed"] in ["fast", "very_fast"]
    
    def test_recommendations_for_high_interpretability(self, catalog):
        """Test recommendations favor interpretable models when needed"""
        recommendations = catalog.get_recommendations(
            task_type="classification",
            data_size="small",
            interpretability="high"
        )
        
        # Top recommendations should include interpretable models
        top_interpretabilities = [r["interpretability"] for r in recommendations[:3]]
        assert "high" in top_interpretabilities or "medium" in top_interpretabilities


class TestModelMetadata:
    """Tests for model metadata completeness"""
    
    @pytest.fixture
    def catalog(self):
        return ModelCatalog()
    
    def test_xgboost_metadata(self, catalog):
        """Test XGBoost model metadata"""
        model = catalog.get_model("xgboost_classifier")
        assert model is not None
        assert model["supports_gpu"] == True
        assert model["handles_missing"] == True
        assert "n_estimators" in model["default_params"]
        assert "n_estimators" in model["tunable_params"]
    
    def test_logistic_regression_metadata(self, catalog):
        """Test Logistic Regression metadata"""
        model = catalog.get_model("logistic_regression")
        assert model is not None
        assert model["interpretability"] == "high"
        assert model["requires_scaling"] == True
        assert model["training_complexity"] == "low"
    
    def test_svm_metadata(self, catalog):
        """Test SVM model metadata"""
        model = catalog.get_model("svm_classifier")
        assert model is not None
        assert model["requires_scaling"] == True
        assert "kernel" in model["default_params"]
    
    def test_kmeans_metadata(self, catalog):
        """Test K-Means clustering metadata"""
        model = catalog.get_model("kmeans")
        assert model is not None
        assert "clustering" in model["task_types"]
        assert model["requires_scaling"] == True
        assert "n_clusters" in model["default_params"]

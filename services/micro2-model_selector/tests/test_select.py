# tests/test_select.py
# --------------------------------------------------------------------
# Tests for model selection endpoints and services.
# These tests are designed to work in CI without external infrastructure.
# --------------------------------------------------------------------
import pytest
import pandas as pd
import io

# Import services that don't require infrastructure
from app.services.model_selector import ModelSelectorService
from app.services.dataset_analyzer import DatasetAnalyzer
from app.services.model_catalog import ModelCatalog


# Skip all endpoint tests that require infrastructure (postgres)
SKIP_INFRA_TESTS = True  # Set to False when running with docker-compose


@pytest.fixture
def get_client():
    """Get TestClient, skip test if infrastructure unavailable"""
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)
    except Exception as e:
        pytest.skip(f"Cannot create client - infrastructure unavailable: {e}")


class TestDatasetAnalyzer:
    """Tests for dataset analysis service - no infrastructure needed"""
    
    @pytest.fixture
    def analyzer(self):
        return DatasetAnalyzer()
    
    @pytest.fixture
    def classification_df(self):
        """Sample classification dataset"""
        return pd.DataFrame({
            "feature1": [1.0, 2.0, 3.0, 4.0, 5.0] * 20,
            "feature2": [0.1, 0.2, 0.3, 0.4, 0.5] * 20,
            "category": ["A", "B", "A", "B", "A"] * 20,
            "target": [0, 1, 0, 1, 0] * 20
        })
    
    @pytest.fixture
    def regression_df(self):
        """Sample regression dataset"""
        return pd.DataFrame({
            "feature1": range(100),
            "feature2": [x * 0.5 for x in range(100)],
            "target": [x * 2.0 + 1.0 for x in range(100)]
        })
    
    def test_detect_classification_task(self, analyzer, classification_df):
        analysis = analyzer.analyze(classification_df)
        assert analysis["task_type"] == "classification"
        assert analysis["target_column"] == "target"
        assert analysis["n_classes"] == 2
    
    def test_detect_regression_task(self, analyzer, regression_df):
        analysis = analyzer.analyze(regression_df)
        assert analysis["task_type"] == "regression"
        assert analysis["target_column"] == "target"
    
    def test_detect_column_types(self, analyzer, classification_df):
        analysis = analyzer.analyze(classification_df)
        assert "feature1" in analysis["numeric_columns"]
        assert "feature2" in analysis["numeric_columns"]
        assert "category" in analysis["categorical_columns"]
    
    def test_missing_value_detection(self, analyzer):
        df = pd.DataFrame({
            "feature1": [1.0, None, 3.0, None, 5.0],
            "feature2": [1, 2, 3, 4, 5],
            "target": [0, 1, 0, 1, 0]
        })
        analysis = analyzer.analyze(df)
        assert analysis["has_missing_values"] == True
        assert "feature1" in analysis["columns_with_missing"]
    
    def test_data_size_categorization(self, analyzer):
        # Small dataset
        small_df = pd.DataFrame({"x": range(100), "y": range(100)})
        analysis = analyzer.analyze(small_df)
        assert analysis["data_size_category"] == "small"
        
        # Medium dataset
        medium_df = pd.DataFrame({"x": range(5000), "y": range(5000)})
        analysis = analyzer.analyze(medium_df)
        assert analysis["data_size_category"] == "medium"


class TestModelCatalogService:
    """Tests for model catalog service - no infrastructure needed"""
    
    @pytest.fixture
    def catalog(self):
        return ModelCatalog()
    
    def test_list_all_models(self, catalog):
        models = catalog.list_models()
        assert len(models) > 0
    
    def test_list_classification_models(self, catalog):
        models = catalog.list_models(task_type="classification")
        assert len(models) > 0
        assert all("classification" in m["task_types"] for m in models)
    
    def test_get_model_by_id(self, catalog):
        model = catalog.get_model("random_forest_classifier")
        assert model is not None
        assert model["model_id"] == "random_forest_classifier"


class TestModelSelector:
    """Tests for model selection service - no infrastructure needed"""
    
    @pytest.fixture
    def selector(self):
        return ModelSelectorService()
    
    @pytest.fixture
    def classification_analysis(self):
        return {
            "task_type": "classification",
            "n_rows": 1000,
            "n_features": 10,
            "n_classes": 2,
            "data_size_category": "medium",
            "has_missing_values": False,
            "is_imbalanced": False,
            "numeric_columns": ["f1", "f2", "f3"],
            "categorical_columns": ["cat1"]
        }
    
    @pytest.fixture
    def regression_analysis(self):
        return {
            "task_type": "regression",
            "n_rows": 1000,
            "n_features": 10,
            "data_size_category": "medium",
            "has_missing_values": False,
            "numeric_columns": ["f1", "f2", "f3"],
            "categorical_columns": []
        }
    
    def test_select_classification_models(self, selector, classification_analysis):
        candidates = selector.select_models(classification_analysis)
        assert len(candidates) > 0
        assert all(c.ranking > 0 for c in candidates)
        assert candidates[0].ranking == 1  # Top model is rank 1
    
    def test_select_regression_models(self, selector, regression_analysis):
        candidates = selector.select_models(regression_analysis, metric="rmse")
        assert len(candidates) > 0
    
    def test_max_models_limit(self, selector, classification_analysis):
        candidates = selector.select_models(classification_analysis, max_models=3)
        assert len(candidates) <= 3


@pytest.mark.skipif(SKIP_INFRA_TESTS, reason="Requires Postgres infrastructure")
class TestEndpoints:
    """Tests for API endpoints - requires infrastructure"""
    
    def test_health_check(self, get_client):
        response = get_client.get("/health/")
        assert response.status_code == 200
    
    def test_list_models(self, get_client):
        response = get_client.get("/models/")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

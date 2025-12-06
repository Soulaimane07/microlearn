# tests/test_select.py
# --------------------------------------------------------------------
# Tests for model selection endpoints and services.
# --------------------------------------------------------------------
import pytest
from fastapi.testclient import TestClient
import pandas as pd
import io

from app.main import app
from app.services.model_selector import ModelSelectorService
from app.services.dataset_analyzer import DatasetAnalyzer
from app.services.model_catalog import ModelCatalog


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "model-selector"
    
    def test_ready_check(self):
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"


class TestModelCatalog:
    """Tests for model catalog"""
    
    def test_list_all_models(self):
        response = client.get("/models/")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "count" in data
        assert data["count"] > 0
    
    def test_list_classification_models(self):
        response = client.get("/models/?task_type=classification")
        assert response.status_code == 200
        data = response.json()
        assert all("classification" in m["task_types"] for m in data["models"])
    
    def test_list_regression_models(self):
        response = client.get("/models/?task_type=regression")
        assert response.status_code == 200
        data = response.json()
        assert all("regression" in m["task_types"] for m in data["models"])
    
    def test_list_by_category(self):
        response = client.get("/models/?category=ensemble")
        assert response.status_code == 200
        data = response.json()
        assert all(m["category"] == "ensemble" for m in data["models"])
    
    def test_get_specific_model(self):
        response = client.get("/models/random_forest_classifier")
        assert response.status_code == 200
        data = response.json()
        assert data["model_id"] == "random_forest_classifier"
        assert data["model_name"] == "Random Forest Classifier"
    
    def test_get_nonexistent_model(self):
        response = client.get("/models/nonexistent_model")
        assert response.status_code == 404
    
    def test_list_categories(self):
        response = client.get("/models/categories/")
        assert response.status_code == 200
        data = response.json()
        assert "ensemble" in data
        assert "linear" in data
    
    def test_list_metrics(self):
        response = client.get("/models/metrics/")
        assert response.status_code == 200
        data = response.json()
        assert "classification" in data
        assert "regression" in data
        assert "clustering" in data


class TestDatasetAnalyzer:
    """Tests for dataset analysis service"""
    
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


class TestModelSelector:
    """Tests for model selection service"""
    
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
        # Should not include classification-only models
        assert all("regression" in selector.catalog.get_model(c.model_id)["task_types"]
                   for c in candidates)
    
    def test_max_models_limit(self, selector, classification_analysis):
        candidates = selector.select_models(classification_analysis, max_models=3)
        assert len(candidates) <= 3
    
    def test_exclude_deep_learning(self, selector, classification_analysis):
        candidates = selector.select_models(
            classification_analysis,
            include_deep_learning=False
        )
        assert all(c.category != "neural_network" for c in candidates)
    
    def test_include_deep_learning(self, selector, classification_analysis):
        candidates = selector.select_models(
            classification_analysis,
            include_deep_learning=True,
            max_models=20
        )
        # Should include at least one neural network model
        categories = [c.category for c in candidates]
        assert "neural_network" in categories
    
    def test_compatibility_scores(self, selector, classification_analysis):
        candidates = selector.select_models(classification_analysis)
        # Scores should be between 0 and 1
        assert all(0 <= c.compatibility_score <= 1 for c in candidates)
        # Scores should be in descending order
        scores = [c.compatibility_score for c in candidates]
        assert scores == sorted(scores, reverse=True)


class TestSelectEndpoint:
    """Tests for /select endpoint"""
    
    def test_select_with_upload(self):
        # Create a simple CSV
        csv_content = "feature1,feature2,target\n1,0.1,0\n2,0.2,1\n3,0.3,0\n4,0.4,1\n5,0.5,0"
        
        response = client.post(
            "/select",
            files={"file": ("test.csv", csv_content, "text/csv")},
            data={"metric": "accuracy", "max_models": "3"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "candidates" in data
        assert "dataset_analysis" in data
        assert len(data["candidates"]) <= 3
    
    def test_select_invalid_file(self):
        response = client.post(
            "/select",
            files={"file": ("test.txt", "not a csv", "text/plain")}
        )
        assert response.status_code == 400
    
    def test_analyze_endpoint(self):
        csv_content = "a,b,c,target\n1,2,3,0\n4,5,6,1\n7,8,9,0"
        
        response = client.post(
            "/select/analyze",
            files={"file": ("test.csv", csv_content, "text/csv")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "task_type" in data
        assert "n_rows" in data
        assert "n_columns" in data


class TestRecommendations:
    """Tests for model recommendations"""
    
    def test_get_recommendations_classification(self):
        response = client.get("/models/recommendations/classification")
        assert response.status_code == 200
        data = response.json()
        assert data["task_type"] == "classification"
        assert "recommendations" in data
    
    def test_get_recommendations_regression(self):
        response = client.get("/models/recommendations/regression")
        assert response.status_code == 200
        data = response.json()
        assert data["task_type"] == "regression"
    
    def test_get_recommendations_with_params(self):
        response = client.get(
            "/models/recommendations/classification",
            params={"data_size": "large", "interpretability": "high"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data_size"] == "large"
        assert data["interpretability"] == "high"
    
    def test_get_recommendations_invalid_task(self):
        response = client.get("/models/recommendations/invalid_task")
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

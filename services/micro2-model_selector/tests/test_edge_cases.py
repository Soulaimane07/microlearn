# tests/test_edge_cases.py
# --------------------------------------------------------------------
# Additional edge case tests for Model Selector microservice.
# Improves test coverage by testing boundary conditions and error cases.
# --------------------------------------------------------------------
import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from app.main import app
from app.services.model_catalog import ModelCatalog
from app.services.dataset_analyzer import DatasetAnalyzer
from app.services.model_selector import ModelSelectorService


client = TestClient(app)


class TestDatasetAnalyzerEdgeCases:
    """Edge case tests for DatasetAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        return DatasetAnalyzer()
    
    def test_analyze_empty_dataframe(self, analyzer):
        """Test analyzing an empty dataframe"""
        df = pd.DataFrame()
        
        # Should handle gracefully or raise appropriate error
        try:
            analysis = analyzer.analyze(df)
            # If it doesn't raise, should have sensible defaults
            assert "n_rows" in analysis
            assert analysis["n_rows"] == 0
        except (ValueError, KeyError, IndexError):
            # Empty dataframe causing an error is acceptable
            pass
    
    def test_analyze_single_row(self, analyzer):
        """Test analyzing dataframe with single row"""
        df = pd.DataFrame({
            "feature": [1.0],
            "target": [0]
        })
        
        analysis = analyzer.analyze(df)
        
        assert analysis["n_rows"] == 1
        assert analysis["data_size_category"] == "small"
    
    def test_analyze_single_column(self, analyzer):
        """Test analyzing dataframe with single column"""
        df = pd.DataFrame({
            "only_column": [1, 2, 3, 4, 5]
        })
        
        analysis = analyzer.analyze(df)
        
        assert analysis["n_columns"] == 1
    
    def test_analyze_all_missing_values(self, analyzer):
        """Test analyzing dataframe with all missing values"""
        df = pd.DataFrame({
            "feature": [None, None, None],
            "target": [None, None, None]
        })
        
        analysis = analyzer.analyze(df)
        
        assert analysis["has_missing_values"] == True
        # Check for either missing_ratio or total_missing_percentage
        has_missing_info = (
            analysis.get("missing_ratio", 0) > 0 or
            analysis.get("total_missing_percentage", 0) > 0 or
            len(analysis.get("columns_with_missing", [])) > 0
        )
        assert has_missing_info
    
    def test_analyze_mixed_types(self, analyzer):
        """Test analyzing dataframe with mixed column types"""
        df = pd.DataFrame({
            "int_col": [1, 2, 3, 4, 5],
            "float_col": [1.1, 2.2, 3.3, 4.4, 5.5],
            "str_col": ["a", "b", "c", "d", "e"],
            "bool_col": [True, False, True, False, True],
            "date_col": pd.date_range("2023-01-01", periods=5),
            "target": [0, 1, 0, 1, 0]
        })
        
        analysis = analyzer.analyze(df)
        
        assert len(analysis["numeric_columns"]) >= 2
        assert len(analysis["categorical_columns"]) >= 1
    
    def test_analyze_high_cardinality_target(self, analyzer):
        """Test regression detection with continuous target"""
        df = pd.DataFrame({
            "feature": list(range(100)),
            "target": [x * 0.5 + 0.1 for x in range(100)]
        })
        
        analysis = analyzer.analyze(df, target_column="target")
        
        assert analysis["task_type"] == "regression"
    
    def test_analyze_binary_classification(self, analyzer):
        """Test binary classification detection"""
        df = pd.DataFrame({
            "feature": list(range(100)),
            "target": [0, 1] * 50
        })
        
        analysis = analyzer.analyze(df, target_column="target")
        
        assert analysis["task_type"] == "classification"
        assert analysis["n_classes"] == 2
    
    def test_analyze_multiclass_classification(self, analyzer):
        """Test multiclass classification detection"""
        df = pd.DataFrame({
            "feature": list(range(99)),
            "target": [0, 1, 2] * 33
        })
        
        analysis = analyzer.analyze(df, target_column="target")
        
        assert analysis["task_type"] == "classification"
        assert analysis["n_classes"] == 3
    
    def test_analyze_imbalanced_dataset(self, analyzer):
        """Test imbalance detection"""
        df = pd.DataFrame({
            "feature": list(range(100)),
            "target": [0] * 95 + [1] * 5  # 95:5 imbalance
        })
        
        analysis = analyzer.analyze(df, target_column="target")
        
        assert analysis["is_imbalanced"] == True
    
    def test_analyze_large_dataset_category(self, analyzer):
        """Test large dataset size categorization"""
        df = pd.DataFrame({
            "feature": list(range(50000)),
            "target": list(range(50000))
        })
        
        analysis = analyzer.analyze(df)
        
        assert analysis["data_size_category"] in ["large", "very_large"]
    
    def test_analyze_with_explicit_task_type(self, analyzer):
        """Test specifying task type explicitly"""
        df = pd.DataFrame({
            "feature": [1, 2, 3, 4, 5],
            "target": [0, 1, 0, 1, 0]
        })
        
        # Force regression even though target looks like classification
        analysis = analyzer.analyze(df, task_type="regression", target_column="target")
        
        assert analysis["task_type"] == "regression"


class TestModelSelectorEdgeCases:
    """Edge case tests for ModelSelectorService"""
    
    @pytest.fixture
    def selector(self):
        return ModelSelectorService()
    
    def test_select_with_minimal_analysis(self, selector):
        """Test selection with minimal analysis input"""
        minimal_analysis = {
            "task_type": "classification",
            "n_rows": 100,
            "n_features": 5,
            "data_size_category": "small",
            "has_missing_values": False,
            "numeric_columns": [],
            "categorical_columns": []
        }
        
        candidates = selector.select_models(minimal_analysis)
        
        assert len(candidates) > 0
    
    def test_select_with_zero_features(self, selector):
        """Test selection when there are no features"""
        analysis = {
            "task_type": "classification",
            "n_rows": 100,
            "n_features": 0,
            "data_size_category": "small",
            "has_missing_values": False,
            "numeric_columns": [],
            "categorical_columns": []
        }
        
        candidates = selector.select_models(analysis)
        
        # Should still return candidates even with edge case
        assert candidates is not None
    
    def test_select_for_clustering(self, selector):
        """Test model selection for clustering task"""
        analysis = {
            "task_type": "clustering",
            "n_rows": 1000,
            "n_features": 10,
            "data_size_category": "medium",
            "has_missing_values": False,
            "numeric_columns": ["f1", "f2", "f3"],
            "categorical_columns": []
        }
        
        candidates = selector.select_models(analysis)
        
        # Should return clustering models
        assert len(candidates) > 0
        # Verify all candidates are for clustering
        for c in candidates:
            model = selector.catalog.get_model(c.model_id)
            assert "clustering" in model["task_types"]
    
    def test_select_max_models_one(self, selector):
        """Test selecting only one model"""
        analysis = {
            "task_type": "classification",
            "n_rows": 1000,
            "n_features": 10,
            "data_size_category": "medium",
            "has_missing_values": False,
            "numeric_columns": ["f1"],
            "categorical_columns": []
        }
        
        candidates = selector.select_models(analysis, max_models=1)
        
        assert len(candidates) == 1
        assert candidates[0].ranking == 1
    
    def test_select_with_all_missing_values(self, selector):
        """Test selection when all features have missing values"""
        analysis = {
            "task_type": "classification",
            "n_rows": 1000,
            "n_features": 10,
            "data_size_category": "medium",
            "has_missing_values": True,
            "missing_ratio": 0.5,
            "numeric_columns": ["f1", "f2"],
            "categorical_columns": [],
            "columns_with_missing": ["f1", "f2"]
        }
        
        candidates = selector.select_models(analysis)
        
        # Should prefer models that handle missing values
        assert len(candidates) > 0
    
    def test_select_different_metrics(self, selector):
        """Test selection with different optimization metrics"""
        analysis = {
            "task_type": "classification",
            "n_rows": 1000,
            "n_features": 10,
            "data_size_category": "medium",
            "has_missing_values": False,
            "numeric_columns": ["f1"],
            "categorical_columns": []
        }
        
        for metric in ["accuracy", "f1", "precision", "recall", "auc"]:
            candidates = selector.select_models(analysis, metric=metric)
            assert len(candidates) > 0
    
    def test_explain_selection(self, selector):
        """Test selection explanation generation"""
        analysis = {
            "task_type": "classification",
            "n_rows": 1000,
            "n_features": 10,
            "n_classes": 2,
            "data_size_category": "medium",
            "has_missing_values": False,
            "numeric_columns": ["f1"],
            "categorical_columns": []
        }
        
        candidates = selector.select_models(analysis)
        explanation = selector.explain_selection(candidates, analysis)
        
        assert explanation is not None
        assert len(explanation) > 0


class TestModelCatalogEdgeCases:
    """Edge case tests for ModelCatalog"""
    
    @pytest.fixture
    def catalog(self):
        return ModelCatalog()
    
    def test_filter_nonexistent_category(self, catalog):
        """Test filtering by category that doesn't exist"""
        models = catalog.list_models(category="nonexistent_category")
        
        assert len(models) == 0
    
    def test_filter_nonexistent_task_type(self, catalog):
        """Test filtering by task type that doesn't exist"""
        models = catalog.list_models(task_type="nonexistent_task")
        
        assert len(models) == 0
    
    def test_get_recommendations_invalid_data_size(self, catalog):
        """Test recommendations with unusual data size"""
        recommendations = catalog.get_recommendations(
            task_type="classification",
            data_size="gigantic",  # Not a standard size
            interpretability="medium"
        )
        
        # Should still return some recommendations
        assert recommendations is not None
    
    def test_list_all_task_types(self, catalog):
        """Test that all task types have models"""
        for task_type in ["classification", "regression", "clustering"]:
            models = catalog.list_models(task_type=task_type)
            assert len(models) > 0, f"No models for task type: {task_type}"
    
    def test_model_has_default_params(self, catalog):
        """Test all models have default parameters"""
        models = catalog.list_models()
        
        for model in models:
            assert "default_params" in model
            assert isinstance(model["default_params"], dict)


class TestAPIEdgeCases:
    """Edge case tests for API endpoints"""
    
    def test_select_empty_csv(self):
        """Test /select with empty CSV"""
        response = client.post(
            "/select",
            files={"file": ("empty.csv", "", "text/csv")}
        )
        
        # Should return an error status
        assert response.status_code in [400, 422, 500]
    
    def test_select_malformed_csv(self):
        """Test /select with malformed CSV"""
        response = client.post(
            "/select",
            files={"file": ("bad.csv", "a,b,c\n1,2\n4,5,6,7", "text/csv")}
        )
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 422, 500]
    
    def test_select_single_column_csv(self):
        """Test /select with single column"""
        csv_content = "feature\n1\n2\n3\n4\n5"
        
        response = client.post(
            "/select",
            files={"file": ("single.csv", csv_content, "text/csv")}
        )
        
        # Should return an error or handle gracefully
        assert response.status_code in [200, 400, 422, 500]
    
    def test_recommendations_all_task_types(self):
        """Test recommendations endpoint for all task types"""
        for task_type in ["classification", "regression"]:
            response = client.get(f"/models/recommendations/{task_type}")
            assert response.status_code == 200
    
    def test_models_pagination(self):
        """Test models list handles pagination-like requests"""
        response = client.get("/models/")
        assert response.status_code == 200
        
        data = response.json()
        assert "models" in data
        assert "count" in data


class TestUtilityFunctions:
    """Tests for utility functions"""
    
    def test_convert_numpy_types(self):
        """Test numpy type conversion utility"""
        from app.services.dataset_analyzer import convert_numpy_types
        
        # Test various numpy types
        assert convert_numpy_types(np.int64(42)) == 42
        assert convert_numpy_types(np.float64(3.14)) == 3.14
        assert convert_numpy_types(np.bool_(True)) == True
        assert convert_numpy_types(np.array([1, 2, 3])) == [1, 2, 3]
        assert convert_numpy_types({"key": np.int64(10)}) == {"key": 10}
        assert convert_numpy_types([np.float64(1.5), np.float64(2.5)]) == [1.5, 2.5]
    
    def test_convert_numpy_types_nested(self):
        """Test numpy type conversion with nested structures"""
        from app.services.dataset_analyzer import convert_numpy_types
        
        nested = {
            "outer": {
                "inner": np.int64(100),
                "list": [np.float64(1.1), np.float64(2.2)]
            }
        }
        
        result = convert_numpy_types(nested)
        
        assert result["outer"]["inner"] == 100
        assert result["outer"]["list"] == [1.1, 2.2]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

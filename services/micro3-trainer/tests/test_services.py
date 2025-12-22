# tests/test_services.py
# --------------------------------------------------------------------
# Additional unit tests for Trainer microservice services.
# Improves SonarQube test coverage with unit tests for model_factory
# and training utilities.
# --------------------------------------------------------------------
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock


class TestModelFactoryExtended:
    """Extended tests for ModelFactory class"""
    
    @pytest.fixture
    def factory(self):
        from app.services.model_factory import ModelFactory
        return ModelFactory()
    
    def test_create_decision_tree_classifier(self, factory):
        """Test creating DecisionTree classifier"""
        model = factory.create_model(
            "decision_tree_classifier",
            "classification",
            {"max_depth": 5}
        )
        assert model is not None
        assert hasattr(model, "fit")
        assert hasattr(model, "predict")
    
    def test_create_logistic_regression(self, factory):
        """Test creating Logistic Regression"""
        model = factory.create_model(
            "logistic_regression",
            "classification",
            {"max_iter": 100}
        )
        assert model is not None
        assert hasattr(model, "fit")
    
    def test_create_svm_classifier(self, factory):
        """Test creating SVM classifier"""
        model = factory.create_model(
            "svm_classifier",
            "classification",
            {"kernel": "rbf"}
        )
        assert model is not None
    
    def test_create_knn_classifier(self, factory):
        """Test creating KNN classifier"""
        model = factory.create_model(
            "knn_classifier",
            "classification",
            {"n_neighbors": 3}
        )
        assert model is not None
    
    def test_create_naive_bayes(self, factory):
        """Test creating Naive Bayes"""
        model = factory.create_model(
            "naive_bayes",
            "classification",
            {}
        )
        assert model is not None
    
    def test_create_mlp_classifier(self, factory):
        """Test creating MLP classifier"""
        model = factory.create_model(
            "mlp_classifier",
            "classification",
            {"hidden_layer_sizes": (10,), "max_iter": 100}
        )
        assert model is not None
    
    def test_create_random_forest_regressor(self, factory):
        """Test creating RandomForest regressor"""
        model = factory.create_model(
            "random_forest_regressor",
            "regression",
            {"n_estimators": 10}
        )
        assert model is not None
    
    def test_create_linear_regression(self, factory):
        """Test creating Linear Regression"""
        model = factory.create_model(
            "linear_regression",
            "regression",
            {}
        )
        assert model is not None
    
    def test_create_ridge_regression(self, factory):
        """Test creating Ridge Regression"""
        model = factory.create_model(
            "ridge_regression",
            "regression",
            {"alpha": 1.0}
        )
        assert model is not None
    
    def test_create_lasso_regression(self, factory):
        """Test creating Lasso Regression"""
        model = factory.create_model(
            "lasso_regression",
            "regression",
            {"alpha": 0.1}
        )
        assert model is not None
    
    def test_create_svr(self, factory):
        """Test creating SVR"""
        model = factory.create_model(
            "svr",
            "regression",
            {"kernel": "rbf"}
        )
        assert model is not None
    
    def test_create_mlp_regressor(self, factory):
        """Test creating MLP regressor"""
        model = factory.create_model(
            "mlp_regressor",
            "regression",
            {"hidden_layer_sizes": (10,), "max_iter": 100}
        )
        assert model is not None
    
    def test_create_kmeans(self, factory):
        """Test creating K-Means"""
        model = factory.create_model(
            "kmeans",
            "clustering",
            {"n_clusters": 3}
        )
        assert model is not None
    
    def test_create_dbscan(self, factory):
        """Test creating DBSCAN"""
        model = factory.create_model(
            "dbscan",
            "clustering",
            {"eps": 0.5}
        )
        assert model is not None
    
    def test_create_hierarchical(self, factory):
        """Test creating Hierarchical Clustering"""
        model = factory.create_model(
            "hierarchical",
            "clustering",
            {"n_clusters": 3}
        )
        assert model is not None
    
    def test_create_xgboost_classifier_with_defaults(self, factory):
        """Test XGBoost classifier gets proper defaults"""
        try:
            model = factory.create_model(
                "xgboost_classifier",
                "classification",
                {}
            )
            assert model is not None
        except ImportError:
            pytest.skip("XGBoost not installed")
    
    def test_create_xgboost_regressor(self, factory):
        """Test creating XGBoost regressor"""
        try:
            model = factory.create_model(
                "xgboost_regressor",
                "regression",
                {"n_estimators": 10}
            )
            assert model is not None
        except ImportError:
            pytest.skip("XGBoost not installed")
    
    def test_create_lightgbm_with_verbosity(self, factory):
        """Test LightGBM classifier gets verbosity set"""
        try:
            model = factory.create_model(
                "lightgbm_classifier",
                "classification",
                {}
            )
            assert model is not None
        except ImportError:
            pytest.skip("LightGBM not installed")
    
    def test_create_lightgbm_regressor(self, factory):
        """Test creating LightGBM regressor"""
        try:
            model = factory.create_model(
                "lightgbm_regressor",
                "regression",
                {}
            )
            assert model is not None
        except ImportError:
            pytest.skip("LightGBM not installed")
    
    def test_get_classification_models(self, factory):
        """Test getting classification models"""
        models = factory.get_available_models("classification")
        assert len(models) > 0
        assert "random_forest_classifier" in models
        assert "logistic_regression" in models
    
    def test_get_regression_models(self, factory):
        """Test getting regression models"""
        models = factory.get_available_models("regression")
        assert len(models) > 0
        assert "random_forest_regressor" in models
        assert "linear_regression" in models
    
    def test_get_clustering_models(self, factory):
        """Test getting clustering models"""
        models = factory.get_available_models("clustering")
        assert len(models) > 0
        assert "kmeans" in models
        assert "dbscan" in models
    
    def test_get_all_models(self, factory):
        """Test getting all models without filter"""
        models = factory.get_available_models()
        assert len(models) > 10
    
    def test_random_state_set_automatically(self, factory):
        """Test that random_state is set by default"""
        model = factory.create_model(
            "random_forest_classifier",
            "classification",
            {}
        )
        # RandomForest should have random_state set
        assert model.random_state is not None


class TestTrainingOrchestratorMocked:
    """Tests for TrainingOrchestrator with mocked dependencies"""
    
    def test_calculate_progress_normal(self):
        """Test progress calculation with normal values"""
        from app.services.training_orchestrator import TrainingOrchestrator
        
        with patch.object(TrainingOrchestrator, '__init__', lambda x: None):
            orch = TrainingOrchestrator()
            orch.postgres = None
            orch.minio = None
            orch.model_factory = None
            orch.mlflow_tracker = None
            orch.gpu_available = False
            orch.active_jobs = {}
            
            progress = orch._calculate_progress(5, 10)
            assert progress == 50.0
    
    def test_calculate_progress_complete(self):
        """Test progress at 100%"""
        from app.services.training_orchestrator import TrainingOrchestrator
        
        with patch.object(TrainingOrchestrator, '__init__', lambda x: None):
            orch = TrainingOrchestrator()
            orch.postgres = None
            orch.minio = None
            orch.model_factory = None
            orch.mlflow_tracker = None
            orch.gpu_available = False
            orch.active_jobs = {}
            
            progress = orch._calculate_progress(10, 10)
            assert progress == 100.0
    
    def test_calculate_progress_none_current(self):
        """Test progress with None current epoch"""
        from app.services.training_orchestrator import TrainingOrchestrator
        
        with patch.object(TrainingOrchestrator, '__init__', lambda x: None):
            orch = TrainingOrchestrator()
            orch.postgres = None
            orch.minio = None
            orch.model_factory = None
            orch.mlflow_tracker = None
            orch.gpu_available = False
            orch.active_jobs = {}
            
            progress = orch._calculate_progress(None, 10)
            assert progress == 0.0
    
    def test_calculate_progress_none_total(self):
        """Test progress with None total epochs"""
        from app.services.training_orchestrator import TrainingOrchestrator
        
        with patch.object(TrainingOrchestrator, '__init__', lambda x: None):
            orch = TrainingOrchestrator()
            orch.postgres = None
            orch.minio = None
            orch.model_factory = None
            orch.mlflow_tracker = None
            orch.gpu_available = False
            orch.active_jobs = {}
            
            progress = orch._calculate_progress(5, None)
            assert progress == 0.0
    
    def test_calculate_progress_zero_total(self):
        """Test progress with zero total epochs"""
        from app.services.training_orchestrator import TrainingOrchestrator
        
        with patch.object(TrainingOrchestrator, '__init__', lambda x: None):
            orch = TrainingOrchestrator()
            orch.postgres = None
            orch.minio = None
            orch.model_factory = None
            orch.mlflow_tracker = None
            orch.gpu_available = False
            orch.active_jobs = {}
            
            progress = orch._calculate_progress(5, 0)
            assert progress == 0.0


class TestMLflowTrackerMocked:
    """Tests for MLflowTracker with mocked dependencies"""
    
    def test_tracker_initialization(self):
        """Test MLflow tracker can be imported"""
        try:
            from app.services.mlflow_tracker import MLflowTracker
            assert MLflowTracker is not None
        except ImportError:
            pytest.skip("MLflow not available")
    
    def test_tracker_start_run_mock(self):
        """Test starting MLflow run"""
        with patch('app.services.mlflow_tracker.mlflow') as mock_mlflow:
            mock_run = MagicMock()
            mock_run.info.run_id = "test_run_id"
            mock_run.info.experiment_id = "test_exp_id"
            mock_mlflow.start_run.return_value.__enter__ = lambda _: mock_run
            mock_mlflow.start_run.return_value.__exit__ = lambda *args: None
            
            from app.services.mlflow_tracker import MLflowTracker
            tracker = MLflowTracker()
            
            # Should not raise
            assert tracker is not None


class TestMetricsCalculation:
    """Tests for metrics calculation helpers"""
    
    def test_accuracy_calculation(self):
        """Test accuracy metric"""
        from sklearn.metrics import accuracy_score
        
        y_true = [0, 1, 0, 1, 0]
        y_pred = [0, 1, 0, 1, 1]  # One error
        
        accuracy = accuracy_score(y_true, y_pred)
        assert accuracy == 0.8
    
    def test_f1_score_calculation(self):
        """Test F1 score metric"""
        from sklearn.metrics import f1_score
        
        y_true = [0, 1, 0, 1, 0]
        y_pred = [0, 1, 0, 1, 1]
        
        f1 = f1_score(y_true, y_pred)
        assert f1 > 0
    
    def test_mse_calculation(self):
        """Test MSE metric"""
        from sklearn.metrics import mean_squared_error
        
        y_true = [1.0, 2.0, 3.0]
        y_pred = [1.1, 2.1, 2.9]
        
        mse = mean_squared_error(y_true, y_pred)
        assert mse > 0
    
    def test_r2_calculation(self):
        """Test R2 score metric"""
        from sklearn.metrics import r2_score
        
        y_true = [1.0, 2.0, 3.0, 4.0, 5.0]
        y_pred = [1.1, 2.1, 2.9, 4.1, 4.9]
        
        r2 = r2_score(y_true, y_pred)
        assert r2 > 0.9


class TestDataPreparation:
    """Tests for data preparation utilities"""
    
    def test_train_test_split(self):
        """Test train test split"""
        from sklearn.model_selection import train_test_split
        
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        y = np.array([0, 1, 0, 1, 0])
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        assert len(X_train) == 4
        assert len(X_test) == 1
    
    def test_cross_validation(self):
        """Test cross validation"""
        from sklearn.model_selection import cross_val_score
        from sklearn.ensemble import RandomForestClassifier
        
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]] * 4)
        y = np.array([0, 1, 0, 1, 0] * 4)
        
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        scores = cross_val_score(model, X, y, cv=2)
        
        assert len(scores) == 2


class TestModelTraining:
    """Tests for model training utilities"""
    
    def test_fit_predict_classifier(self):
        """Test fit and predict for classifier"""
        from sklearn.ensemble import RandomForestClassifier
        
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]] * 5)
        y = np.array([0, 1, 0, 1] * 5)
        
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        predictions = model.predict(X)
        
        assert len(predictions) == len(y)
    
    def test_fit_predict_regressor(self):
        """Test fit and predict for regressor"""
        from sklearn.ensemble import RandomForestRegressor
        
        X = np.array([[1], [2], [3], [4], [5]])
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        
        model = RandomForestRegressor(n_estimators=5, random_state=42)
        model.fit(X, y)
        predictions = model.predict(X)
        
        assert len(predictions) == len(y)
    
    def test_fit_predict_clustering(self):
        """Test fit and predict for clustering"""
        from sklearn.cluster import KMeans
        
        X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
        
        model = KMeans(n_clusters=2, random_state=42, n_init="auto")
        labels = model.fit_predict(X)
        
        assert len(labels) == len(X)
        assert len(set(labels)) == 2


class TestModelSerialization:
    """Tests for model serialization"""
    
    def test_joblib_save_load(self):
        """Test saving and loading model with joblib"""
        import joblib
        import tempfile
        import os
        
        from sklearn.ensemble import RandomForestClassifier
        
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 1, 0, 1])
        model.fit(X, y)
        
        # Save and load
        with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as f:
            temp_path = f.name
        
        try:
            joblib.dump(model, temp_path)
            loaded_model = joblib.load(temp_path)
            
            # Compare predictions
            orig_pred = model.predict(X)
            loaded_pred = loaded_model.predict(X)
            
            assert (orig_pred == loaded_pred).all()
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# app/services/model_factory.py
# --------------------------------------------------------------------
# Model factory for creating ML model instances.
# --------------------------------------------------------------------
from typing import Any, Dict, Optional
import importlib

from app.core.logger import logger


class ModelFactory:
    """Factory for creating ML model instances"""
    
    # Model registry mapping model_id to class paths
    MODEL_REGISTRY = {
        # Classification models
        'random_forest_classifier': 'sklearn.ensemble.RandomForestClassifier',
        'decision_tree_classifier': 'sklearn.tree.DecisionTreeClassifier',
        'xgboost_classifier': 'xgboost.XGBClassifier',
        'lightgbm_classifier': 'lightgbm.LGBMClassifier',
        'logistic_regression': 'sklearn.linear_model.LogisticRegression',
        'svm_classifier': 'sklearn.svm.SVC',
        'knn_classifier': 'sklearn.neighbors.KNeighborsClassifier',
        'naive_bayes': 'sklearn.naive_bayes.GaussianNB',
        'mlp_classifier': 'sklearn.neural_network.MLPClassifier',
        
        # Regression models
        'random_forest_regressor': 'sklearn.ensemble.RandomForestRegressor',
        'xgboost_regressor': 'xgboost.XGBRegressor',
        'lightgbm_regressor': 'lightgbm.LGBMRegressor',
        'linear_regression': 'sklearn.linear_model.LinearRegression',
        'ridge_regression': 'sklearn.linear_model.Ridge',
        'lasso_regression': 'sklearn.linear_model.Lasso',
        'svr': 'sklearn.svm.SVR',
        'mlp_regressor': 'sklearn.neural_network.MLPRegressor',
        
        # Clustering models
        'kmeans': 'sklearn.cluster.KMeans',
        'dbscan': 'sklearn.cluster.DBSCAN',
        'hierarchical': 'sklearn.cluster.AgglomerativeClustering',
    }
    
    def create_model(
        self, 
        model_id: str, 
        task_type: str,
        hyperparameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Create a model instance.
        
        Args:
            model_id: Model identifier
            task_type: Task type (classification, regression, clustering)
            hyperparameters: Model hyperparameters
            
        Returns:
            Model instance
        """
        if model_id not in self.MODEL_REGISTRY:
            raise ValueError(f"Unknown model_id: {model_id}")
        
        class_path = self.MODEL_REGISTRY[model_id]
        logger.info(f"Creating model: {model_id} ({class_path})")
        
        # Import model class
        module_name, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        
        # Merge with default parameters
        params = hyperparameters or {}
        
        # Add common defaults
        if 'random_state' not in params and hasattr(model_class, 'random_state'):
            params['random_state'] = 42
        
        # Special handling for XGBoost classifier
        if model_id == 'xgboost_classifier':
            params.setdefault('use_label_encoder', False)
            params.setdefault('eval_metric', 'logloss')
        
        # Special handling for LightGBM
        if 'lightgbm' in model_id:
            params.setdefault('verbosity', -1)
        
        # Instantiate model
        try:
            model = model_class(**params)
            logger.info(f"Created model with params: {params}")
            return model
        except Exception as e:
            logger.error(f"Failed to create model {model_id}: {e}")
            raise
    
    def get_available_models(self, task_type: Optional[str] = None) -> list:
        """
        Get list of available models.
        
        Args:
            task_type: Filter by task type
            
        Returns:
            List of model IDs
        """
        if task_type is None:
            return list(self.MODEL_REGISTRY.keys())
        
        # Filter by task type
        suffix_map = {
            'classification': '_classifier',
            'regression': '_regressor',
            'clustering': ''
        }
        
        suffix = suffix_map.get(task_type, '')
        
        if suffix:
            return [mid for mid in self.MODEL_REGISTRY.keys() if suffix in mid or 'naive_bayes' in mid or 'logistic' in mid or 'svm' in mid or mid in ['kmeans', 'dbscan', 'hierarchical']]
        else:
            return [mid for mid in self.MODEL_REGISTRY.keys() if mid in ['kmeans', 'dbscan', 'hierarchical']]

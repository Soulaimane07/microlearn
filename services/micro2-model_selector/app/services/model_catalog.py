# app/services/model_catalog.py
# --------------------------------------------------------------------
# Catalog of available ML models with metadata.
# Contains all supported models and their characteristics.
# --------------------------------------------------------------------
from typing import Dict, Any, List, Optional

from app.core.logger import logger


class ModelCatalog:
    """Catalog of available ML models with comprehensive metadata"""
    
    def __init__(self):
        self._models = self._initialize_models()
        self._categories = self._initialize_categories()
    
    def _initialize_models(self) -> Dict[str, Dict[str, Any]]:
        """Initialize the model catalog with all supported models"""
        return {
            # ============== CLASSIFICATION MODELS ==============
            
            # Tree-based
            "random_forest_classifier": {
                "model_id": "random_forest_classifier",
                "model_name": "Random Forest Classifier",
                "model_class": "sklearn.ensemble.RandomForestClassifier",
                "category": "ensemble",
                "description": "Ensemble of decision trees using bagging. Robust and versatile.",
                "task_types": ["classification"],
                "interpretability": "medium",
                "training_complexity": "medium",
                "prediction_speed": "fast",
                "memory_usage": "medium",
                "supports_gpu": False,
                "default_params": {
                    "n_estimators": 100,
                    "max_depth": None,
                    "min_samples_split": 2,
                    "min_samples_leaf": 1,
                    "random_state": 42
                },
                "tunable_params": {
                    "n_estimators": {"type": "int", "low": 50, "high": 500},
                    "max_depth": {"type": "int", "low": 3, "high": 30},
                    "min_samples_split": {"type": "int", "low": 2, "high": 20},
                    "min_samples_leaf": {"type": "int", "low": 1, "high": 10}
                },
                "suitable_for": ["tabular data", "mixed features", "imbalanced data"],
                "not_suitable_for": ["very high dimensional data", "streaming data"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "decision_tree_classifier": {
                "model_id": "decision_tree_classifier",
                "model_name": "Decision Tree Classifier",
                "model_class": "sklearn.tree.DecisionTreeClassifier",
                "category": "tree",
                "description": "Simple, interpretable tree-based classifier.",
                "task_types": ["classification"],
                "interpretability": "high",
                "training_complexity": "low",
                "prediction_speed": "very_fast",
                "memory_usage": "low",
                "supports_gpu": False,
                "default_params": {
                    "max_depth": None,
                    "min_samples_split": 2,
                    "min_samples_leaf": 1,
                    "random_state": 42
                },
                "tunable_params": {
                    "max_depth": {"type": "int", "low": 2, "high": 30},
                    "min_samples_split": {"type": "int", "low": 2, "high": 20},
                    "min_samples_leaf": {"type": "int", "low": 1, "high": 10},
                    "criterion": {"type": "categorical", "choices": ["gini", "entropy"]}
                },
                "suitable_for": ["interpretability required", "small datasets", "quick prototyping"],
                "not_suitable_for": ["complex patterns", "high accuracy needs"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "xgboost_classifier": {
                "model_id": "xgboost_classifier",
                "model_name": "XGBoost Classifier",
                "model_class": "xgboost.XGBClassifier",
                "category": "ensemble",
                "description": "Gradient boosting with regularization. State-of-the-art for tabular data.",
                "task_types": ["classification"],
                "interpretability": "low",
                "training_complexity": "high",
                "prediction_speed": "fast",
                "memory_usage": "medium",
                "supports_gpu": True,
                "default_params": {
                    "n_estimators": 100,
                    "max_depth": 6,
                    "learning_rate": 0.1,
                    "subsample": 0.8,
                    "colsample_bytree": 0.8,
                    "random_state": 42,
                    "use_label_encoder": False,
                    "eval_metric": "logloss"
                },
                "tunable_params": {
                    "n_estimators": {"type": "int", "low": 50, "high": 500},
                    "max_depth": {"type": "int", "low": 3, "high": 15},
                    "learning_rate": {"type": "float", "low": 0.01, "high": 0.3},
                    "subsample": {"type": "float", "low": 0.6, "high": 1.0},
                    "colsample_bytree": {"type": "float", "low": 0.6, "high": 1.0},
                    "reg_alpha": {"type": "float", "low": 0, "high": 10},
                    "reg_lambda": {"type": "float", "low": 0, "high": 10}
                },
                "suitable_for": ["tabular data", "competitions", "large datasets"],
                "not_suitable_for": ["small datasets", "interpretability required"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": True,
                "handles_categorical": False
            },
            
            "lightgbm_classifier": {
                "model_id": "lightgbm_classifier",
                "model_name": "LightGBM Classifier",
                "model_class": "lightgbm.LGBMClassifier",
                "category": "ensemble",
                "description": "Fast gradient boosting framework. Excellent for large datasets.",
                "task_types": ["classification"],
                "interpretability": "low",
                "training_complexity": "medium",
                "prediction_speed": "very_fast",
                "memory_usage": "low",
                "supports_gpu": True,
                "default_params": {
                    "n_estimators": 100,
                    "max_depth": -1,
                    "learning_rate": 0.1,
                    "num_leaves": 31,
                    "random_state": 42,
                    "verbosity": -1
                },
                "tunable_params": {
                    "n_estimators": {"type": "int", "low": 50, "high": 500},
                    "max_depth": {"type": "int", "low": 3, "high": 15},
                    "learning_rate": {"type": "float", "low": 0.01, "high": 0.3},
                    "num_leaves": {"type": "int", "low": 20, "high": 100},
                    "min_child_samples": {"type": "int", "low": 5, "high": 100}
                },
                "suitable_for": ["large datasets", "high cardinality features", "speed critical"],
                "not_suitable_for": ["very small datasets"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": True,
                "handles_categorical": True
            },
            
            # Linear models
            "logistic_regression": {
                "model_id": "logistic_regression",
                "model_name": "Logistic Regression",
                "model_class": "sklearn.linear_model.LogisticRegression",
                "category": "linear",
                "description": "Linear model for classification. Simple, fast, interpretable.",
                "task_types": ["classification"],
                "interpretability": "high",
                "training_complexity": "low",
                "prediction_speed": "very_fast",
                "memory_usage": "very_low",
                "supports_gpu": False,
                "default_params": {
                    "C": 1.0,
                    "max_iter": 1000,
                    "random_state": 42,
                    "solver": "lbfgs"
                },
                "tunable_params": {
                    "C": {"type": "float", "low": 0.001, "high": 100, "log": True},
                    "penalty": {"type": "categorical", "choices": ["l1", "l2", "elasticnet", None]},
                    "solver": {"type": "categorical", "choices": ["lbfgs", "liblinear", "saga"]}
                },
                "suitable_for": ["linearly separable data", "interpretability", "baseline model"],
                "not_suitable_for": ["complex non-linear patterns"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            # SVM
            "svm_classifier": {
                "model_id": "svm_classifier",
                "model_name": "Support Vector Classifier",
                "model_class": "sklearn.svm.SVC",
                "category": "svm",
                "description": "Powerful classifier using kernel trick. Good for complex boundaries.",
                "task_types": ["classification"],
                "interpretability": "low",
                "training_complexity": "high",
                "prediction_speed": "medium",
                "memory_usage": "high",
                "supports_gpu": False,
                "default_params": {
                    "C": 1.0,
                    "kernel": "rbf",
                    "gamma": "scale",
                    "random_state": 42,
                    "probability": True
                },
                "tunable_params": {
                    "C": {"type": "float", "low": 0.1, "high": 100, "log": True},
                    "kernel": {"type": "categorical", "choices": ["linear", "rbf", "poly"]},
                    "gamma": {"type": "categorical", "choices": ["scale", "auto"]}
                },
                "suitable_for": ["small-medium datasets", "complex decision boundaries"],
                "not_suitable_for": ["large datasets", "high dimensionality"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            # KNN
            "knn_classifier": {
                "model_id": "knn_classifier",
                "model_name": "K-Nearest Neighbors Classifier",
                "model_class": "sklearn.neighbors.KNeighborsClassifier",
                "category": "instance_based",
                "description": "Instance-based learning. Simple and effective for small datasets.",
                "task_types": ["classification"],
                "interpretability": "medium",
                "training_complexity": "very_low",
                "prediction_speed": "slow",
                "memory_usage": "high",
                "supports_gpu": False,
                "default_params": {
                    "n_neighbors": 5,
                    "weights": "uniform",
                    "algorithm": "auto"
                },
                "tunable_params": {
                    "n_neighbors": {"type": "int", "low": 1, "high": 50},
                    "weights": {"type": "categorical", "choices": ["uniform", "distance"]},
                    "metric": {"type": "categorical", "choices": ["euclidean", "manhattan", "minkowski"]}
                },
                "suitable_for": ["small datasets", "low dimensionality"],
                "not_suitable_for": ["large datasets", "high dimensionality"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            # Naive Bayes
            "naive_bayes": {
                "model_id": "naive_bayes",
                "model_name": "Gaussian Naive Bayes",
                "model_class": "sklearn.naive_bayes.GaussianNB",
                "category": "probabilistic",
                "description": "Probabilistic classifier assuming feature independence.",
                "task_types": ["classification"],
                "interpretability": "high",
                "training_complexity": "very_low",
                "prediction_speed": "very_fast",
                "memory_usage": "very_low",
                "supports_gpu": False,
                "default_params": {},
                "tunable_params": {
                    "var_smoothing": {"type": "float", "low": 1e-12, "high": 1e-6, "log": True}
                },
                "suitable_for": ["text classification", "quick baseline", "high dimensionality"],
                "not_suitable_for": ["correlated features"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            # ============== REGRESSION MODELS ==============
            
            "random_forest_regressor": {
                "model_id": "random_forest_regressor",
                "model_name": "Random Forest Regressor",
                "model_class": "sklearn.ensemble.RandomForestRegressor",
                "category": "ensemble",
                "description": "Ensemble of decision trees for regression.",
                "task_types": ["regression"],
                "interpretability": "medium",
                "training_complexity": "medium",
                "prediction_speed": "fast",
                "memory_usage": "medium",
                "supports_gpu": False,
                "default_params": {
                    "n_estimators": 100,
                    "max_depth": None,
                    "random_state": 42
                },
                "tunable_params": {
                    "n_estimators": {"type": "int", "low": 50, "high": 500},
                    "max_depth": {"type": "int", "low": 3, "high": 30},
                    "min_samples_split": {"type": "int", "low": 2, "high": 20}
                },
                "suitable_for": ["tabular data", "non-linear relationships"],
                "not_suitable_for": ["extrapolation tasks"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "xgboost_regressor": {
                "model_id": "xgboost_regressor",
                "model_name": "XGBoost Regressor",
                "model_class": "xgboost.XGBRegressor",
                "category": "ensemble",
                "description": "Gradient boosting for regression tasks.",
                "task_types": ["regression"],
                "interpretability": "low",
                "training_complexity": "high",
                "prediction_speed": "fast",
                "memory_usage": "medium",
                "supports_gpu": True,
                "default_params": {
                    "n_estimators": 100,
                    "max_depth": 6,
                    "learning_rate": 0.1,
                    "random_state": 42
                },
                "tunable_params": {
                    "n_estimators": {"type": "int", "low": 50, "high": 500},
                    "max_depth": {"type": "int", "low": 3, "high": 15},
                    "learning_rate": {"type": "float", "low": 0.01, "high": 0.3}
                },
                "suitable_for": ["tabular data", "competitions"],
                "not_suitable_for": ["small datasets"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": True,
                "handles_categorical": False
            },
            
            "lightgbm_regressor": {
                "model_id": "lightgbm_regressor",
                "model_name": "LightGBM Regressor",
                "model_class": "lightgbm.LGBMRegressor",
                "category": "ensemble",
                "description": "Fast gradient boosting for regression.",
                "task_types": ["regression"],
                "interpretability": "low",
                "training_complexity": "medium",
                "prediction_speed": "very_fast",
                "memory_usage": "low",
                "supports_gpu": True,
                "default_params": {
                    "n_estimators": 100,
                    "learning_rate": 0.1,
                    "random_state": 42,
                    "verbosity": -1
                },
                "tunable_params": {
                    "n_estimators": {"type": "int", "low": 50, "high": 500},
                    "learning_rate": {"type": "float", "low": 0.01, "high": 0.3},
                    "num_leaves": {"type": "int", "low": 20, "high": 100}
                },
                "suitable_for": ["large datasets", "speed critical"],
                "not_suitable_for": ["very small datasets"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": True,
                "handles_categorical": True
            },
            
            "linear_regression": {
                "model_id": "linear_regression",
                "model_name": "Linear Regression",
                "model_class": "sklearn.linear_model.LinearRegression",
                "category": "linear",
                "description": "Simple linear regression model.",
                "task_types": ["regression"],
                "interpretability": "high",
                "training_complexity": "very_low",
                "prediction_speed": "very_fast",
                "memory_usage": "very_low",
                "supports_gpu": False,
                "default_params": {},
                "tunable_params": {},
                "suitable_for": ["linear relationships", "baseline model", "interpretability"],
                "not_suitable_for": ["non-linear relationships"],
                "sklearn_compatible": True,
                "requires_scaling": False,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "ridge_regression": {
                "model_id": "ridge_regression",
                "model_name": "Ridge Regression",
                "model_class": "sklearn.linear_model.Ridge",
                "category": "linear",
                "description": "Linear regression with L2 regularization.",
                "task_types": ["regression"],
                "interpretability": "high",
                "training_complexity": "low",
                "prediction_speed": "very_fast",
                "memory_usage": "very_low",
                "supports_gpu": False,
                "default_params": {"alpha": 1.0, "random_state": 42},
                "tunable_params": {
                    "alpha": {"type": "float", "low": 0.001, "high": 100, "log": True}
                },
                "suitable_for": ["multicollinearity", "regularization needed"],
                "not_suitable_for": ["feature selection"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "lasso_regression": {
                "model_id": "lasso_regression",
                "model_name": "Lasso Regression",
                "model_class": "sklearn.linear_model.Lasso",
                "category": "linear",
                "description": "Linear regression with L1 regularization (sparse).",
                "task_types": ["regression"],
                "interpretability": "high",
                "training_complexity": "low",
                "prediction_speed": "very_fast",
                "memory_usage": "very_low",
                "supports_gpu": False,
                "default_params": {"alpha": 1.0, "random_state": 42},
                "tunable_params": {
                    "alpha": {"type": "float", "low": 0.001, "high": 100, "log": True}
                },
                "suitable_for": ["feature selection", "sparse solutions"],
                "not_suitable_for": ["highly correlated features"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "svr": {
                "model_id": "svr",
                "model_name": "Support Vector Regressor",
                "model_class": "sklearn.svm.SVR",
                "category": "svm",
                "description": "SVM for regression tasks.",
                "task_types": ["regression"],
                "interpretability": "low",
                "training_complexity": "high",
                "prediction_speed": "medium",
                "memory_usage": "high",
                "supports_gpu": False,
                "default_params": {"C": 1.0, "kernel": "rbf"},
                "tunable_params": {
                    "C": {"type": "float", "low": 0.1, "high": 100, "log": True},
                    "kernel": {"type": "categorical", "choices": ["linear", "rbf", "poly"]}
                },
                "suitable_for": ["small-medium datasets", "complex patterns"],
                "not_suitable_for": ["large datasets"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            # ============== CLUSTERING MODELS ==============
            
            "kmeans": {
                "model_id": "kmeans",
                "model_name": "K-Means Clustering",
                "model_class": "sklearn.cluster.KMeans",
                "category": "clustering",
                "description": "Partition-based clustering algorithm.",
                "task_types": ["clustering"],
                "interpretability": "high",
                "training_complexity": "low",
                "prediction_speed": "fast",
                "memory_usage": "low",
                "supports_gpu": False,
                "default_params": {"n_clusters": 8, "random_state": 42, "n_init": 10},
                "tunable_params": {
                    "n_clusters": {"type": "int", "low": 2, "high": 20},
                    "init": {"type": "categorical", "choices": ["k-means++", "random"]}
                },
                "suitable_for": ["spherical clusters", "large datasets"],
                "not_suitable_for": ["non-convex clusters", "varying density"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "dbscan": {
                "model_id": "dbscan",
                "model_name": "DBSCAN",
                "model_class": "sklearn.cluster.DBSCAN",
                "category": "clustering",
                "description": "Density-based clustering. Finds arbitrarily shaped clusters.",
                "task_types": ["clustering"],
                "interpretability": "medium",
                "training_complexity": "medium",
                "prediction_speed": "medium",
                "memory_usage": "medium",
                "supports_gpu": False,
                "default_params": {"eps": 0.5, "min_samples": 5},
                "tunable_params": {
                    "eps": {"type": "float", "low": 0.1, "high": 2.0},
                    "min_samples": {"type": "int", "low": 2, "high": 20}
                },
                "suitable_for": ["arbitrary shapes", "outlier detection"],
                "not_suitable_for": ["varying density", "high dimensionality"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "hierarchical": {
                "model_id": "hierarchical",
                "model_name": "Hierarchical Clustering",
                "model_class": "sklearn.cluster.AgglomerativeClustering",
                "category": "clustering",
                "description": "Agglomerative hierarchical clustering.",
                "task_types": ["clustering"],
                "interpretability": "high",
                "training_complexity": "high",
                "prediction_speed": "slow",
                "memory_usage": "high",
                "supports_gpu": False,
                "default_params": {"n_clusters": 2, "linkage": "ward"},
                "tunable_params": {
                    "n_clusters": {"type": "int", "low": 2, "high": 20},
                    "linkage": {"type": "categorical", "choices": ["ward", "complete", "average", "single"]}
                },
                "suitable_for": ["hierarchical structure", "dendrogram visualization"],
                "not_suitable_for": ["large datasets"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            # ============== NEURAL NETWORKS ==============
            
            "mlp_classifier": {
                "model_id": "mlp_classifier",
                "model_name": "Multi-Layer Perceptron Classifier",
                "model_class": "sklearn.neural_network.MLPClassifier",
                "category": "neural_network",
                "description": "Feedforward neural network for classification.",
                "task_types": ["classification"],
                "interpretability": "low",
                "training_complexity": "high",
                "prediction_speed": "fast",
                "memory_usage": "medium",
                "supports_gpu": False,
                "default_params": {
                    "hidden_layer_sizes": (100,),
                    "max_iter": 500,
                    "random_state": 42
                },
                "tunable_params": {
                    "hidden_layer_sizes": {"type": "categorical", "choices": [(50,), (100,), (100, 50), (100, 100)]},
                    "learning_rate_init": {"type": "float", "low": 0.0001, "high": 0.1, "log": True},
                    "alpha": {"type": "float", "low": 0.0001, "high": 0.1, "log": True}
                },
                "suitable_for": ["complex patterns", "large datasets"],
                "not_suitable_for": ["interpretability required", "small datasets"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            },
            
            "mlp_regressor": {
                "model_id": "mlp_regressor",
                "model_name": "Multi-Layer Perceptron Regressor",
                "model_class": "sklearn.neural_network.MLPRegressor",
                "category": "neural_network",
                "description": "Feedforward neural network for regression.",
                "task_types": ["regression"],
                "interpretability": "low",
                "training_complexity": "high",
                "prediction_speed": "fast",
                "memory_usage": "medium",
                "supports_gpu": False,
                "default_params": {
                    "hidden_layer_sizes": (100,),
                    "max_iter": 500,
                    "random_state": 42
                },
                "tunable_params": {
                    "hidden_layer_sizes": {"type": "categorical", "choices": [(50,), (100,), (100, 50)]},
                    "learning_rate_init": {"type": "float", "low": 0.0001, "high": 0.1, "log": True}
                },
                "suitable_for": ["complex patterns", "large datasets"],
                "not_suitable_for": ["small datasets", "interpretability required"],
                "sklearn_compatible": True,
                "requires_scaling": True,
                "handles_missing": False,
                "handles_categorical": False
            }
        }
    
    def _initialize_categories(self) -> Dict[str, Dict[str, Any]]:
        """Initialize model categories"""
        return {
            "tree": {
                "category_id": "tree",
                "category_name": "Decision Trees",
                "description": "Tree-based models that make decisions based on feature splits"
            },
            "ensemble": {
                "category_id": "ensemble",
                "category_name": "Ensemble Methods",
                "description": "Methods that combine multiple models (bagging, boosting)"
            },
            "linear": {
                "category_id": "linear",
                "category_name": "Linear Models",
                "description": "Models based on linear combinations of features"
            },
            "svm": {
                "category_id": "svm",
                "category_name": "Support Vector Machines",
                "description": "Models based on finding optimal hyperplanes"
            },
            "instance_based": {
                "category_id": "instance_based",
                "category_name": "Instance-Based Learning",
                "description": "Methods that store and compare instances"
            },
            "probabilistic": {
                "category_id": "probabilistic",
                "category_name": "Probabilistic Models",
                "description": "Models based on probability theory"
            },
            "clustering": {
                "category_id": "clustering",
                "category_name": "Clustering Algorithms",
                "description": "Unsupervised methods for grouping similar instances"
            },
            "neural_network": {
                "category_id": "neural_network",
                "category_name": "Neural Networks",
                "description": "Deep learning models with multiple layers"
            }
        }
    
    def list_models(
        self,
        task_type: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all models, optionally filtered by task type or category"""
        models = list(self._models.values())
        
        if task_type:
            models = [m for m in models if task_type in m["task_types"]]
        
        if category:
            models = [m for m in models if m["category"] == category]
        
        return models
    
    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific model by ID"""
        return self._models.get(model_id)
    
    def list_categories(self) -> Dict[str, Any]:
        """List all categories with model counts"""
        result = {}
        for cat_id, cat_info in self._categories.items():
            models_in_cat = [m["model_id"] for m in self._models.values() if m["category"] == cat_id]
            result[cat_id] = {
                **cat_info,
                "model_count": len(models_in_cat),
                "models": models_in_cat
            }
        return result
    
    def get_recommendations(
        self,
        task_type: str,
        data_size: str = "medium",
        interpretability: str = "medium"
    ) -> List[Dict[str, Any]]:
        """Get model recommendations based on requirements"""
        candidates = self.list_models(task_type=task_type)
        
        # Score and sort candidates
        scored = []
        for model in candidates:
            score = 0
            
            # Size compatibility
            if data_size == "small":
                if model["training_complexity"] in ["very_low", "low"]:
                    score += 2
            elif data_size == "large" or data_size == "very_large":
                if model["prediction_speed"] in ["fast", "very_fast"]:
                    score += 2
                if model["handles_missing"]:
                    score += 1
            
            # Interpretability
            interp_levels = {"low": 1, "medium": 2, "high": 3}
            model_interp = interp_levels.get(model["interpretability"], 2)
            required_interp = interp_levels.get(interpretability, 2)
            if model_interp >= required_interp:
                score += 2
            
            scored.append({**model, "recommendation_score": score})
        
        # Sort by score descending
        scored.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        return scored[:5]  # Top 5 recommendations

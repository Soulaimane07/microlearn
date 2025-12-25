from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression

def create_model(model_id: str, params: dict, task_type: str):
    if model_id == "lightgbm_classifier":
        return LGBMClassifier(**params)

    if model_id == "lightgbm_regressor":
        return LGBMRegressor(**params)

    if model_id == "logistic_regression":
        return LogisticRegression(**params)

    if model_id == "linear_regression":
        return LinearRegression(**params)

    raise ValueError(f"Unknown model_id: {model_id}")
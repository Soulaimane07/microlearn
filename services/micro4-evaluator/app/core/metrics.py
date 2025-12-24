import pandas as pd
from sklearn.metrics import roc_auc_score, f1_score, mean_squared_error, roc_curve
import plotly.graph_objects as go
import numpy as np

def evaluate(df: pd.DataFrame):
    y_true = df["y_true"]
    y_pred = df["y_pred"]

    result = {}

    # Classification
    if set(y_true.unique()).issubset({0, 1}):
        result["auc"] = roc_auc_score(y_true, y_pred)
        result["f1"] = f1_score(y_true, y_pred.round())
        result["rmse"] = None

        fpr, tpr, _ = roc_curve(y_true, y_pred)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="ROC"))
        result["roc_curve"] = fig.to_dict()

    # Regression
    else:
        result["auc"] = None
        result["f1"] = None
        result["rmse"] = mean_squared_error(y_true, y_pred, squared=False)
        result["roc_curve"] = None

    return result
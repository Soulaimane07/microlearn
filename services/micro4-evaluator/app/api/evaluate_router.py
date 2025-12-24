from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.metrics import (
    roc_curve, precision_recall_curve,
    confusion_matrix, roc_auc_score,
    f1_score, precision_score,
    recall_score, accuracy_score
)

router = APIRouter()





@router.get("/models")
def list_models():
    # Later: load from Postgres or MinIO
    return [
        {
            "id": "model-1",
            "name": "RandomForest v1",
            "algorithm": "RandomForest"
        },
        {
            "id": "model-2",
            "name": "XGBoost v2",
            "algorithm": "XGBoost"
        }
    ]





@router.get("/datasets")
def list_datasets():
    return [
        { "id": "dataset-1", "name": "Credit Test Set" },
        { "id": "dataset-2", "name": "Fraud Validation Set" }
    ]






class EvaluateRequest(BaseModel):
    model_id: str
    dataset_id: str

@router.post("/evaluate")
def evaluate(req: EvaluateRequest):
    # 🔹 TEMP: simulate predictions
    np.random.seed(42)
    y_true = np.random.randint(0, 2, 200)
    y_pred = np.random.rand(200)

    # Metrics
    auc = roc_auc_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred > 0.5)
    precision = precision_score(y_true, y_pred > 0.5)
    recall = recall_score(y_true, y_pred > 0.5)
    accuracy = accuracy_score(y_true, y_pred > 0.5)

    # ROC
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc = [{"fpr": float(f), "tpr": float(t)} for f, t in zip(fpr, tpr)]

    # PR
    p, r, _ = precision_recall_curve(y_true, y_pred)
    pr = [{"precision": float(pv), "recall": float(rv)} for pv, rv in zip(p, r)]

    # Confusion Matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred > 0.5).ravel()

    # Feature importance (mock)
    feature_importance = [
        {"feature": "age", "importance": 0.32},
        {"feature": "income", "importance": 0.21},
        {"feature": "credit_score", "importance": 0.18}
    ]

    return {
        "metrics": {
            "auc": auc,
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy
        },
        "roc": roc,
        "pr": pr,
        "confusion": {
            "tp": int(tp),
            "fp": int(fp),
            "fn": int(fn),
            "tn": int(tn)
        },
        "feature_importance": feature_importance
    }

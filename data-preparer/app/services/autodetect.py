# app/services/autodetect.py
# --------------------------------------------------------------------
# Compose lower-level detectors into a single metadata detection
# and provide a helper to convert detection result into a pipeline config.
# --------------------------------------------------------------------
import pandas as pd
from app.services.id_detector import detect_id_columns
from app.services.date_detector import detect_date_columns
from app.services.type_detector import detect_column_types
from typing import Dict

def detect_metadata(df: pd.DataFrame) -> Dict[str, list]:
    """
    Return dict with id_columns, date_columns, numeric_columns, categorical_columns.
    """
    id_cols = detect_id_columns(df)
    date_cols = detect_date_columns(df)
    types = detect_column_types(df)
    numeric = types["numeric"]
    categorical = [c for c in types["categorical"] if c not in id_cols + date_cols]
    categorical = [c for c in categorical if c not in numeric]
    return {
        "id_columns": id_cols,
        "date_columns": date_cols,
        "numeric_columns": numeric,
        "categorical_columns": categorical
    }

def metadata_to_pipeline_config(meta: Dict[str, list]) -> Dict:
    """
    Convert detection metadata to an automatic pipeline configuration.
    The pipeline config is deliberately simple:
      - drop id columns
      - treat detected date columns as dates (kept)
      - impute numeric with mean
      - impute categorical with most_frequent
      - apply standard scaling to numeric
      - one-hot encode categorical
    """
    return {
        "drop_columns": meta.get("id_columns", []),
        "date_columns": meta.get("date_columns", []),
        "numeric_columns": meta.get("numeric_columns", []),
        "categorical_columns": meta.get("categorical_columns", []),
        "impute": True,
        "scaling": "standard",
        "onehot": True
    }

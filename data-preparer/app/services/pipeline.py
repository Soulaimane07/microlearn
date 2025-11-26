# app/services/pipeline.py
# --------------------------------------------------------------------
# Deterministic pipeline runner.
# - If config is None, runs an auto pipeline based on heuristics.
# - Returns a pandas DataFrame ready for ML (no id-columns, numeric scaled,
#   categorical one-hot encoded).
# --------------------------------------------------------------------
from typing import Optional, Dict, List
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from app.services.autodetect import detect_metadata, metadata_to_pipeline_config

def _safe_list(cols: Optional[List[str]]) -> List[str]:
    return cols or []

def run_pipeline(df: pd.DataFrame, config: Optional[Dict] = None) -> pd.DataFrame:
    """
    Run pipeline on df.
    If config is None -> auto-detect metadata and build pipeline config.
    Config keys:
      - drop_columns: list[str]
      - date_columns: list[str]
      - numeric_columns: list[str]
      - categorical_columns: list[str]
      - impute: bool
      - scaling: 'standard' or None
      - onehot: bool
    """
    working = df.copy()

    # if no config provided, auto-generate
    if config is None:
        meta = detect_metadata(working)
        config = metadata_to_pipeline_config(meta)

    drop_cols = _safe_list(config.get("drop_columns"))
    date_cols = _safe_list(config.get("date_columns"))
    numeric_cols = _safe_list(config.get("numeric_columns"))
    categorical_cols = _safe_list(config.get("categorical_columns"))
    impute = config.get("impute", False)
    scaling = config.get("scaling", None)
    onehot = config.get("onehot", False)

    # ensure columns exist in DF (defensive)
    drop_cols = [c for c in drop_cols if c in working.columns]
    date_cols = [c for c in date_cols if c in working.columns]
    numeric_cols = [c for c in numeric_cols if c in working.columns]
    categorical_cols = [c for c in categorical_cols if c in working.columns]

    # drop columns (ids)
    if drop_cols:
        working = working.drop(columns=drop_cols)

    # parse dates
    for c in date_cols:
        try:
            working[c] = pd.to_datetime(working[c], errors="coerce")
        except Exception:
            # if parse fails, just leave original values
            pass

    # numeric imputation
    if impute and numeric_cols:
        # use mean for numeric
        imp = SimpleImputer(strategy="mean")
        for col in numeric_cols:
            try:
                arr = working[[col]].values  # 2D
                transformed = imp.fit_transform(arr)
                # transformed shape (n,1) -> assign flattened
                working[col] = transformed.ravel()
            except Exception:
                # coerce to numeric if possible
                working[col] = pd.to_numeric(working[col], errors="coerce")

    # categorical imputation
    if impute and categorical_cols:
        imp = SimpleImputer(strategy="most_frequent")
        for col in categorical_cols:
            try:
                arr = working[[col]].astype(object).values
                transformed = imp.fit_transform(arr)
                working[col] = transformed.ravel()
            except Exception:
                # fallback: fillna with placeholder
                working[col] = working[col].fillna("NA")

    # scaling
    if scaling == "standard" and numeric_cols:
        scaler = StandardScaler()
        # build subset of numeric cols that still exist
        num = [c for c in numeric_cols if c in working.columns]
        try:
            working[num] = scaler.fit_transform(working[num].astype(float))
        except Exception:
            # if conversion fails, try per-column
            for col in num:
                try:
                    working[col] = scaler.fit_transform(working[[col]].astype(float))
                except Exception:
                    pass

    # one-hot encoding
    if onehot and categorical_cols:
        cat_cols = [c for c in categorical_cols if c in working.columns]
        if cat_cols:
            try:
                working = pd.get_dummies(working, columns=cat_cols, drop_first=False)
            except Exception:
                # fallback: encode each categorical col manually
                for c in cat_cols:
                    try:
                        dummies = pd.get_dummies(working[c], prefix=c)
                        working = pd.concat([working.drop(columns=[c]), dummies], axis=1)
                    except Exception:
                        continue

    # final: drop any columns with all-NaN
    working = working.dropna(axis=1, how="all")

    return working

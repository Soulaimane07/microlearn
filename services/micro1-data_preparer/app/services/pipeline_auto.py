# app/services/pipeline_auto.py
# --------------------------------------------------------------------
# Automatic cleaning pipeline for arbitrary tabular datasets.
#
# Logic:
#  - Drop identifier-like columns (UUIDs / very high uniqueness).
#  - Convert detected date columns into numeric features (year, month, weekday).
#  - Impute numerical columns with median, categorical with most frequent.
#  - Scale numeric columns (StandardScaler) when requested or by default if numeric present.
#  - One-hot encode categorical columns with limited cardinality (<= 50 unique values).
#
# Returns: cleaned pd.DataFrame
# --------------------------------------------------------------------

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from typing import Dict, List
from app.core.logger import logger

def _safe_get(cols_list, df):
    return [c for c in (cols_list or []) if c in df.columns]

def run_pipeline_auto(df: pd.DataFrame, pipeline_cfg: Dict) -> pd.DataFrame:
    """
    df: raw dataframe
    pipeline_cfg: dictionary with keys:
        - id_columns: list[str]
        - date_columns: list[str]
        - numeric_columns: list[str]
        - categorical_columns: list[str]
        - impute (bool) optional
        - scaling (str) optional: 'standard' or None
        - onehot (bool) optional
    """
    df = df.copy()

    # 0. Normalize config lists from detection
    id_cols = _safe_get(pipeline_cfg.get("id_columns", []), df)
    date_cols = _safe_get(pipeline_cfg.get("date_columns", []), df)
    numeric_cols = _safe_get(pipeline_cfg.get("numeric_columns", []), df)
    categorical_cols = _safe_get(pipeline_cfg.get("categorical_columns", []), df)
    target_column = pipeline_cfg.get("target_column")

    logger.info(f"PipelineAuto: drop ids {id_cols}")
    df = df.drop(columns=id_cols, errors="ignore")

    # 1. Date extraction
    for col in date_cols:
        if col not in df.columns:
            continue
        try:
            parsed = pd.to_datetime(df[col], errors="coerce", utc=False)
            df[f"{col}_year"] = parsed.dt.year
            df[f"{col}_month"] = parsed.dt.month
            df[f"{col}_day"] = parsed.dt.day
            df[f"{col}_weekday"] = parsed.dt.weekday
            # After extracting features we drop original column
            df = df.drop(columns=[col])
        except Exception as exc:
            logger.warning(f"Date parse failed for {col}: {exc}")

    # Refresh numeric/categorical columns after date extraction/drop
    numeric_cols = [c for c in numeric_cols if c in df.columns]
    categorical_cols = [c for c in categorical_cols if c in df.columns]

    # 2. Imputation
    if pipeline_cfg.get("impute", True):
        # Numeric imputation: median
        if numeric_cols:
            try:
                num_imputer = SimpleImputer(strategy="median")
                df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
            except Exception as exc:
                logger.warning(f"Numeric imputation warning: {exc}")

        # Categorical imputation: most frequent (mode)
        for c in categorical_cols:
            try:
                imp = SimpleImputer(strategy="most_frequent")
                df[[c]] = imp.fit_transform(df[[c]])
            except Exception as exc:
                # If column can't be imputed (all NaN), fill with empty string
                logger.warning(f"Categorical impute failed for {c}: {exc}")
                df[c] = df[c].fillna("")

    # 3. Scaling (default to standard if numeric exists and scaling not provided)
    scaling = pipeline_cfg.get("scaling")
    if not scaling and numeric_cols:
        scaling = "standard"
    if scaling and numeric_cols:
        try:
            # Exclude target column from scaling
            cols_to_scale = [c for c in numeric_cols if c != target_column]
            if cols_to_scale:
                if scaling == "standard":
                    scaler = StandardScaler()
                    df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
                else:
                    logger.info(f"Unknown scaling '{scaling}' - skipping")
        except Exception as exc:
            logger.warning(f"Scaling failed: {exc}")

    # 4. One-hot encoding for low-cardinality categorical columns
    if pipeline_cfg.get("onehot", True) and categorical_cols:
        low_card = [c for c in categorical_cols if df[c].nunique(dropna=True) <= 50]
        if low_card:
            try:
                df = pd.get_dummies(df, columns=low_card, drop_first=False)
            except Exception as exc:
                logger.warning(f"One-hot encoding failed: {exc}")

    # Final clean-up: reset index
    df = df.reset_index(drop=True)
    return df

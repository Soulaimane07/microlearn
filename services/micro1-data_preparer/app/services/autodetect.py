# app/services/autodetect.py
import pandas as pd
from typing import Dict, List, Optional


def detect_metadata(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Detect column types in a DataFrame

    Returns dict with keys:
    - id_columns: Columns that look like IDs
    - date_columns: Columns with date/datetime types
    - numeric_columns: Numeric columns
    - categorical_columns: Categorical/string columns
    """

    metadata = {
        "id_columns": [],
        "date_columns": [],
        "numeric_columns": [],
        "categorical_columns": []
    }

    for col in df.columns:
        col_lower = col.lower()

        # Check for ID columns (by name pattern)
        if any(pattern in col_lower for pattern in ['id', '_id', 'key', '_key']):
            metadata["id_columns"].append(col)
            continue  # Don't classify as other types

        # Check for date columns
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            metadata["date_columns"].append(col)
        elif any(pattern in col_lower for pattern in ['date', 'time', 'datetime', 'timestamp']):
            metadata["date_columns"].append(col)
        # Check for numeric columns
        elif pd.api.types.is_numeric_dtype(df[col]):
            metadata["numeric_columns"].append(col)
        # Check for categorical columns
        elif pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
            metadata["categorical_columns"].append(col)

    # Additional heuristic: treat very high-uniqueness columns as identifiers
    # (e.g., columns where >90% of values are unique and there are enough
    # distinct values to be meaningful). This helps drop accidental ID-like
    # numeric columns that would otherwise be scaled or treated as features.
    try:
        n_rows = len(df)
        for col in df.columns:
            if col in metadata["id_columns"]:
                continue
            try:
                unique_count = df[col].nunique(dropna=True)
            except Exception:
                unique_count = 0

            # Avoid marking tiny datasets' columns as IDs
            if n_rows > 0 and unique_count >= 20:
                unique_ratio = unique_count / float(n_rows)
                if unique_ratio >= 0.90:
                    metadata["id_columns"].append(col)
    except Exception:
        # If anything goes wrong in heuristics, ignore and return current metadata
        pass

    return metadata


def metadata_to_pipeline_config(meta: Dict[str, List[str]], target_column: Optional[str] = None) -> Dict:
    """
    Convert detected metadata into a pipeline configuration

    Strategy:
    1. Drop ID columns (not useful for ML)
    2. Parse date columns
    3. Handle missing values
    4. Encode categorical columns (EXCEPT target)
    5. Scale numeric columns (EXCEPT target)
    
    Args:
        target_column: Column to exclude from transformations
    """

    steps = []

    # Step 1: Drop ID columns
    if meta.get("id_columns"):
        steps.append({
            "type": "drop_columns",
            "columns": meta["id_columns"]
        })

    # Step 2: Parse date columns (but don't do anything with them yet)
    # In a real scenario, you might extract features like day, month, year
    if meta.get("date_columns"):
        steps.append({
            "type": "parse_dates",
            "columns": meta["date_columns"]
        })

    # Step 3: Handle missing values
    # Prefer imputation over dropping rows to avoid empty datasets.
    # Impute numeric columns with median and categorical with mode.
    numeric_for_imputation = [
        col for col in meta.get("numeric_columns", [])
        if col != target_column  # Exclude target
    ]
    if numeric_for_imputation:
        steps.append({
            "type": "handle_missing",
            "method": "fill_median",
            "columns": numeric_for_imputation
        })

    categorical_for_imputation = [
        col for col in meta.get("categorical_columns", [])
        if col != target_column  # Exclude target
    ]
    if categorical_for_imputation:
        steps.append({
            "type": "handle_missing",
            "method": "fill_mode",
            "columns": categorical_for_imputation
        })

    # Step 4: Encode categorical columns (EXCEPT target)
    categorical_to_encode = [
        col for col in meta.get("categorical_columns", [])
        if col != target_column  # Exclude target from encoding
    ]
    if categorical_to_encode:
        steps.append({
            "type": "encode_categorical",
            "method": "label",
            "columns": categorical_to_encode
        })

    # Step 5: Scale numeric columns (EXCEPT target)
    # Only scale columns that aren't IDs (already dropped), aren't dates, and aren't target
    numeric_to_scale = [
        col for col in meta.get("numeric_columns", [])
        if col not in meta.get("id_columns", []) and col != target_column
    ]

    if numeric_to_scale:
        steps.append({
            "type": "scale_numeric",
            "method": "standard",
            "columns": numeric_to_scale
        })

    return {"steps": steps}
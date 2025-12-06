# app/services/pipeline.py
import pandas as pd
from typing import Dict, List, Optional
from app.core.logger import logger


def run_pipeline(df: pd.DataFrame, pipeline_conf: Optional[Dict] = None) -> pd.DataFrame:
    """
    Execute data preparation pipeline on DataFrame

    Args:
        df: Input DataFrame
        pipeline_conf: Pipeline configuration dict with 'steps' key.
                      If None, auto-generates a basic pipeline.

    Returns:
        Processed DataFrame
    """

    if df.empty:
        raise ValueError("Input DataFrame is empty")

    logger.info(f"Starting pipeline with {len(df)} rows, {len(df.columns)} columns")
    logger.debug(f"Input columns: {list(df.columns)}")

    # Auto-generate pipeline if not provided
    if pipeline_conf is None:
        logger.info("No pipeline config provided, using automatic pipeline")
        pipeline_conf = _auto_generate_pipeline(df)

    if not isinstance(pipeline_conf, dict) or 'steps' not in pipeline_conf:
        raise ValueError("Pipeline config must be a dict with 'steps' key")

    # Execute each step
    processed = df.copy()

    for i, step in enumerate(pipeline_conf.get('steps', [])):
        step_type = step.get('type')
        logger.info(f"Executing step {i + 1}: {step_type}")

        try:
            if step_type == 'drop_columns':
                processed = _drop_columns(processed, step)
            elif step_type == 'handle_missing':
                processed = _handle_missing(processed, step)
            elif step_type == 'encode_categorical':
                processed = _encode_categorical(processed, step)
            elif step_type == 'scale_numeric':
                processed = _scale_numeric(processed, step)
            elif step_type == 'parse_dates':
                processed = _parse_dates(processed, step)
            else:
                logger.warning(f"Unknown step type: {step_type}, skipping")

            logger.info(f"After step {i + 1}: {len(processed)} rows, {len(processed.columns)} columns")

        except KeyError as e:
            # Column not found - check if it was already dropped
            missing_col = str(e).strip("'")
            if missing_col not in processed.columns:
                logger.warning(f"Column '{missing_col}' not found (may have been dropped in previous step), skipping")
                continue
            else:
                raise ValueError(f"Column '{missing_col}' not found in DataFrame") from e
        except Exception as e:
            logger.error(f"Error in step {i + 1} ({step_type}): {e}")
            raise ValueError(f"Pipeline step {i + 1} failed: {str(e)}") from e

    logger.info(f"Pipeline complete: {len(processed)} rows, {len(processed.columns)} columns")
    return processed


def _auto_generate_pipeline(df: pd.DataFrame) -> Dict:
    """Generate a basic automatic pipeline"""
    from app.services.autodetect import detect_metadata, metadata_to_pipeline_config

    meta = detect_metadata(df)
    return metadata_to_pipeline_config(meta)


def _drop_columns(df: pd.DataFrame, step: Dict) -> pd.DataFrame:
    """Drop specified columns"""
    columns = step.get('columns', [])

    if not columns:
        logger.info("No columns to drop")
        return df

    # Only drop columns that actually exist
    existing_cols = [col for col in columns if col in df.columns]
    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        logger.warning(f"Columns not found (skipping): {missing_cols}")

    if existing_cols:
        logger.info(f"Dropping {len(existing_cols)} columns: {existing_cols}")
        df = df.drop(columns=existing_cols)

    return df


def _handle_missing(df: pd.DataFrame, step: Dict) -> pd.DataFrame:
    """Handle missing values"""
    method = step.get('method', 'drop')
    columns = step.get('columns')

    if columns is None:
        # Apply to all columns
        target_cols = df.columns.tolist()
    else:
        # Only use columns that exist
        target_cols = [col for col in columns if col in df.columns]

    if not target_cols:
        logger.info("No columns to process for missing values")
        return df

    if method == 'drop':
        logger.info(f"Dropping rows with missing values in {len(target_cols)} columns")
        df = df.dropna(subset=target_cols)
    elif method == 'fill_mean':
        logger.info(f"Filling missing values with mean")
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
    elif method == 'fill_median':
        logger.info(f"Filling missing values with median")
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
    elif method == 'fill_mode':
        logger.info(f"Filling missing values with mode")
        for col in target_cols:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])
    else:
        logger.warning(f"Unknown missing value method: {method}")

    return df


def _encode_categorical(df: pd.DataFrame, step: Dict) -> pd.DataFrame:
    """Encode categorical columns"""
    method = step.get('method', 'label')
    columns = step.get('columns', [])

    # Only use columns that exist
    existing_cols = [col for col in columns if col in df.columns]
    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        logger.warning(f"Categorical columns not found (skipping): {missing_cols}")

    if not existing_cols:
        logger.info("No categorical columns to encode")
        return df

    if method == 'label':
        logger.info(f"Label encoding {len(existing_cols)} columns")
        for col in existing_cols:
            df[col] = pd.Categorical(df[col]).codes
    elif method == 'onehot':
        logger.info(f"One-hot encoding {len(existing_cols)} columns")
        df = pd.get_dummies(df, columns=existing_cols, prefix=existing_cols)
    else:
        logger.warning(f"Unknown encoding method: {method}")

    return df


def _scale_numeric(df: pd.DataFrame, step: Dict) -> pd.DataFrame:
    """Scale numeric columns"""
    method = step.get('method', 'standard')
    columns = step.get('columns', [])

    # Only use columns that exist
    existing_cols = [col for col in columns if col in df.columns]
    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        logger.warning(f"Numeric columns not found (skipping): {missing_cols}")

    if not existing_cols:
        logger.info("No numeric columns to scale")
        return df

    if method == 'standard':
        logger.info(f"Standard scaling {len(existing_cols)} columns")
        for col in existing_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    df[col] = (df[col] - mean) / std
    elif method == 'minmax':
        logger.info(f"MinMax scaling {len(existing_cols)} columns")
        for col in existing_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    df[col] = (df[col] - min_val) / (max_val - min_val)
    elif method == 'robust':
        logger.info(f"Robust scaling {len(existing_cols)} columns")
        for col in existing_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                median = df[col].median()
                q75 = df[col].quantile(0.75)
                q25 = df[col].quantile(0.25)
                iqr = q75 - q25
                if iqr > 0:
                    df[col] = (df[col] - median) / iqr
    else:
        logger.warning(f"Unknown scaling method: {method}")

    return df


def _parse_dates(df: pd.DataFrame, step: Dict) -> pd.DataFrame:
    """Parse date columns"""
    columns = step.get('columns', [])

    # Only use columns that exist
    existing_cols = [col for col in columns if col in df.columns]
    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        logger.warning(f"Date columns not found (skipping): {missing_cols}")

    if not existing_cols:
        logger.info("No date columns to parse")
        return df

    logger.info(f"Parsing {len(existing_cols)} date columns")
    for col in existing_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except Exception as e:
            logger.warning(f"Failed to parse date column {col}: {e}")

    return df
# app/services/type_detector.py
# --------------------------------------------------------------------
# Detect numeric and categorical columns using pandas dtypes and unique counts.
# --------------------------------------------------------------------
import pandas as pd
from typing import Dict, List

def detect_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    numeric = []
    categorical = []
    for col in df.columns:
        ser = df[col]
        # treat booleans as categorical
        if pd.api.types.is_numeric_dtype(ser):
            numeric.append(col)
        else:
            # if small number of unique values -> categorical
            try:
                nunique = ser.nunique(dropna=True)
                if nunique <= 0.1 * max(1, len(ser)) and nunique <= 50:
                    categorical.append(col)
                else:
                    # strings with mostly numeric characters might still be categorical
                    if pd.api.types.is_string_dtype(ser):
                        categorical.append(col)
            except Exception:
                categorical.append(col)
    # remove overlap
    categorical = [c for c in categorical if c not in numeric]
    return {"numeric": numeric, "categorical": categorical}

# app/services/date_detector.py
# --------------------------------------------------------------------
# Detect candidate date columns by attempting to parse samples with pandas.
# --------------------------------------------------------------------
import pandas as pd
from typing import List

def detect_date_columns(df: pd.DataFrame, sample_n: int = 50) -> List[str]:
    cand = []
    for col in df.columns:
        series = df[col].dropna().astype(str).head(sample_n)
        if series.empty:
            continue
        # try to parse; coerce errors gives NaT for non-dates
        try:
            parsed = pd.to_datetime(series, errors="coerce")
            frac_parsed = parsed.notna().sum() / len(parsed)
            if frac_parsed >= 0.8:  # 80% parseable -> consider date
                cand.append(col)
        except Exception:
            continue
    return cand

# app/services/id_detector.py
# --------------------------------------------------------------------
# Heuristic ID column detector for generic datasets.
# - Checks column name patterns (id, _id, ID, patient, provider, appointment, etc.)
# - Also checks if values look like UUIDs.
# --------------------------------------------------------------------
import re
import pandas as pd

NAME_PATTERNS = [
    r"id$", r"^id", r"_id", r"patient", r"provider", r"insurance",
    r"appointment", r"referring", r"supervising", r"claim", r"order"
]

_uuid_re = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)

def looks_like_uuid_series(s: pd.Series, sample_n: int = 20) -> bool:
    sample = s.dropna().astype(str).head(sample_n)
    if sample.empty:
        return False
    matches = [bool(_uuid_re.match(x.strip())) for x in sample]
    return sum(matches)/len(matches) > 0.8

def detect_id_columns(df: pd.DataFrame) -> list:
    detected = []
    cols = list(df.columns)
    lower_cols = {c: c.lower() for c in cols}
    for c in cols:
        name = c.lower()
        if any(re.search(pat, name) for pat in NAME_PATTERNS):
            detected.append(c)
            continue
        # check UUID-like content
        try:
            if looks_like_uuid_series(df[c]):
                detected.append(c)
        except Exception:
            pass
    # deduplicate and keep original order
    seen = set()
    out = []
    for c in detected:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out

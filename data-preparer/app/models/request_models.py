# app/models/request_models.py
# --------------------------------------------------------------------
# Optional request DTOs (Pydantic) - kept small because we use
# PipelineSchema in validation.
# --------------------------------------------------------------------

from pydantic import BaseModel
from typing import List, Optional

class PipelineConfig(BaseModel):
    drop_columns: Optional[List[str]] = []
    date_columns: Optional[List[str]] = []
    numeric_columns: Optional[List[str]] = []
    categorical_columns: Optional[List[str]] = []
    impute: bool = False
    scaling: Optional[str] = None
    onehot: bool = False

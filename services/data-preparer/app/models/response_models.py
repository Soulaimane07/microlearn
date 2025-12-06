# app/models/response_models.py
# --------------------------------------------------------------------
# Response models for the detect endpoint.
# --------------------------------------------------------------------
from pydantic import BaseModel
from typing import List, Optional

class DetectResponse(BaseModel):
    id_columns: List[str]
    date_columns: List[str]
    numeric_columns: List[str]
    categorical_columns: List[str]
    minio_object: Optional[str] = None
    pipeline_yml: Optional[str] = None

# app/models/pipeline_schema.py
# --------------------------------------------------------------------
# Pydantic models used to document expected pipeline config shape.
# (Optional - not strictly required because service accepts YAML)
# --------------------------------------------------------------------
from pydantic import BaseModel
from typing import List, Optional

class PipelineSchema(BaseModel):
    drop_columns: Optional[List[str]] = []
    date_columns: Optional[List[str]] = []
    numeric_columns: Optional[List[str]] = []
    categorical_columns: Optional[List[str]] = []
    impute: Optional[bool] = True
    scaling: Optional[str] = None
    onehot: Optional[bool] = True

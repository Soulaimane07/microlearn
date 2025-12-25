from pydantic import BaseModel
from typing import Dict, Optional

class TrainRequest(BaseModel):
    model_id: str
    data_id: str
    task_type: str
    target_column: str
    hyperparameters: Dict = {}
    pipeline_id: Optional[str] = None


class TrainResponse(BaseModel):
    job_id: str
    status: str


class FinalResult(BaseModel):
    status: str
    pipeline_id: str
    job_id: str
    model_id: str
    task_type: str
    artifacts: Dict
    training_metrics: Dict
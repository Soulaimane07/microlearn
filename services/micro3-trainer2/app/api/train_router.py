from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.train_schema import TrainRequest, TrainResponse
from app.services.training_orchestrator import TrainingOrchestrator
import asyncio

router = APIRouter(prefix="/train", tags=["Training"])
orchestrator = TrainingOrchestrator()

@router.post("/")
async def start_training(req: TrainRequest):
    job_id = orchestrator.create_job(req)

    # run training in background
    asyncio.create_task(orchestrator.safe_run_training(job_id))

    return {"job_id": job_id}


@router.get("/{job_id}")
def get_status(job_id: str):
    job = orchestrator.get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@router.get("/{job_id}/final_result")
def get_final_result(job_id: str):
    result = orchestrator.get_final_result(job_id)
    if not result:
        raise HTTPException(404, "Result not ready")
    return result
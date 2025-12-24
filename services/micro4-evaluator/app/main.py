from fastapi import FastAPI
from app.api.evaluate_router import router as eval_router

app = FastAPI(title="Evaluator Service")

app.include_router(eval_router)
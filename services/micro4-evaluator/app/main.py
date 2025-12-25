from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.evaluate_router import router as eval_router

app = FastAPI(title="Evaluator Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eval_router)
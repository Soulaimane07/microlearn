from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.train_router import router as train_router

app = FastAPI(
    title="Trainer Microservice",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(train_router)

@app.get("/")
def root():
    return {"service": "trainer", "status": "running"}

@app.get("/health/")
def health():
    return {"status": "ok"}

@app.get("/health/ready")
def ready():
    return {"ready": True}
import uuid
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from app.services.model_factory import create_model
from app.storage.minio_client import load_dataset
import numpy as np
import traceback
from app.storage.minio_client import upload_model
from app.messaging.nats_client import publish_step_done
from app.core.logger import logger

BASE_DIR = "models"
os.makedirs(BASE_DIR, exist_ok=True)

class TrainingOrchestrator:

    def __init__(self):
        self.jobs = {}
        self.results = {}

    async def safe_run_training(self, job_id: str):
        req = self.jobs[job_id]["request"]

        try:
            self.run_training(job_id)

            # 📤 Notify orchestrator — SUCCESS
            await publish_step_done(
                "Trainer",
                {
                    "pipelineId": req.pipeline_id,
                    "step": "Trainer",
                    "status": "SUCCESS"
                }
            )
            logger.info("📤 Published Trainer SUCCESS to orchestrator")

        except Exception as e:
            traceback.print_exc()

            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["error"] = str(e)

            # 📤 Notify orchestrator — FAILED
            try:
                await publish_step_done(
                    "Trainer",
                    {
                        "pipelineId": req.pipeline_id,
                        "step": "Trainer",
                        "status": "FAILED"
                    }
                )
                logger.info("📤 Published Trainer FAILED to orchestrator")
            except Exception as exc:
                logger.error(f"Failed to notify orchestrator: {exc}")


    def create_job(self, req):
        job_id = f"train_{uuid.uuid4().hex[:12]}"
        self.jobs[job_id] = {
            "job_id": job_id,
            "status": "running",
            "model_id": req.model_id
        }
        self.jobs[job_id]["request"] = req
        return job_id

    def run_training(self, job_id: str):
        req = self.jobs[job_id]["request"]

        # Load dataset
        df = load_dataset(req.data_id)
        print(f"Dataset loaded with shape: {df.shape}")
        X = df.drop(columns=[req.target_column])
        y = df[req.target_column]

        if req.task_type == "classification" and not np.issubdtype(y.dtype, np.integer):
            y = y.astype(int)


        # Encode categorical columns
        for col in X.select_dtypes(include=["object"]).columns:
            X[col] = X[col].astype("category").cat.codes


        # 🔒 VALIDATION (your missing protection)
        if req.task_type == "classification":
            if not np.issubdtype(y.dtype, np.integer):
                raise ValueError(
                    f"Classification requires discrete integer labels, got {y.dtype}"
                )

        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3)

        model = create_model(req.model_id, req.hyperparameters, req.task_type)
        model.fit(X_train, y_train)
       
        # Metrics
        if req.task_type == "classification":
            preds = model.predict(X_val)
            metric = accuracy_score(y_val, preds)
            metrics = {"accuracy": metric}
        else:
            preds = model.predict(X_val)
            metric = mean_squared_error(y_val, preds)
            metrics = {"rmse": metric}

        # ============================
        # SAVE MODEL LOCALLY
        # ============================
        model_dir = f"{BASE_DIR}/{job_id}"
        os.makedirs(model_dir, exist_ok=True)

        model_path = f"{model_dir}/model.pkl"
        joblib.dump(model, model_path)

        # ============================
        # UPLOAD TO MINIO
        # ============================
        minio_object_name = f"models/{job_id}/model.pkl"
        upload_model(model_path, minio_object_name)

        # ============================
        # FINAL PIPELINE RESULT
        # ============================
        self.results[job_id] = {
            "status": "completed",
            "pipeline_id": req.pipeline_id,
            "job_id": job_id,
            "model_id": req.model_id,
            "task_type": req.task_type,
            "artifacts": {
                "model_path": minio_object_name  # ✅ MinIO reference ONLY
            },
            "training_metrics": metrics
        }

        self.jobs[job_id]["status"] = "completed"

    def get_job(self, job_id: str):
        return self.jobs.get(job_id)

    def get_final_result(self, job_id: str):
        return self.results.get(job_id)
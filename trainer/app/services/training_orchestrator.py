# app/services/training_orchestrator.py
# --------------------------------------------------------------------
# Main training orchestrator service.
# Manages GPU allocation, parallel training with Ray, and MLflow tracking.
# --------------------------------------------------------------------
import uuid
import pickle
import pandas as pd
import io
from datetime import datetime
from typing import Dict, Any, Optional
import torch

from app.core.config import settings
from app.core.logger import logger
from app.models.request_models import TrainingRequest
from app.models.response_models import JobStatus, TrainingJobResponse
from app.storage.postgres_client import get_postgres_client
from app.storage.minio_client import get_minio_client, download_dataset_bytes
from app.services.model_factory import ModelFactory
from app.services.mlflow_tracker import MLflowTracker


class TrainingOrchestrator:
    """Orchestrates model training with GPU allocation and tracking"""
    
    def __init__(self):
        """Initialize training orchestrator"""
        self.postgres = get_postgres_client()
        self.minio = get_minio_client()
        self.model_factory = ModelFactory()
        self.mlflow_tracker = MLflowTracker()
        
        # Check GPU availability
        self.gpu_available = torch.cuda.is_available()
        self.num_gpus = torch.cuda.device_count() if self.gpu_available else 0
        
        logger.info(f"Training Orchestrator initialized")
        logger.info(f"GPU Available: {self.gpu_available}, Count: {self.num_gpus}")
        
        # Track active jobs
        self.active_jobs: Dict[str, Any] = {}
    
    async def submit_training_job(self, request: TrainingRequest) -> TrainingJobResponse:
        """
        Submit a new training job.
        
        Args:
            request: Training request with model and data info
            
        Returns:
            TrainingJobResponse with job details
        """
        # Generate unique job ID
        job_id = f"train_{uuid.uuid4().hex[:12]}"
        
        logger.info(f"Submitting training job: {job_id}")
        logger.info(f"Model: {request.model_id}, Data: {request.data_id}")
        
        # Create MLflow run
        mlflow_run = self.mlflow_tracker.start_run(
            experiment_name=request.experiment_name or settings.MLFLOW_EXPERIMENT_NAME,
            run_name=request.run_name or f"{request.model_id}_{job_id}",
            tags=request.tags or {}
        )
        
        # Create job in database
        job_data = {
            'job_id': job_id,
            'model_id': request.model_id,
            'data_id': request.data_id,
            'task_type': request.task_type.value,
            'status': JobStatus.PENDING.value,
            'total_epochs': request.epochs,
            'hyperparameters': request.hyperparameters,
            'mlflow_run_id': mlflow_run.info.run_id if mlflow_run else None,
            'mlflow_experiment_id': mlflow_run.info.experiment_id if mlflow_run else None
        }
        
        self.postgres.create_training_job(job_data)
        
        # Start training asynchronously (in background)
        # In production, this would use Ray or Celery
        import asyncio
        asyncio.create_task(self._train_model(job_id, request, mlflow_run))
        
        # Return immediate response
        return TrainingJobResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            model_id=request.model_id,
            data_id=request.data_id,
            created_at=datetime.now(),
            total_epochs=request.epochs,
            mlflow_run_id=mlflow_run.info.run_id if mlflow_run else None,
            mlflow_experiment_id=mlflow_run.info.experiment_id if mlflow_run else None
        )
    
    async def _train_model(self, job_id: str, request: TrainingRequest, mlflow_run: Any):
        """
        Internal method to perform actual training.
        
        Args:
            job_id: Training job ID
            request: Training request
            mlflow_run: MLflow run object
        """
        try:
            # Update status to RUNNING
            self.postgres.update_job_status(
                job_id, 
                JobStatus.RUNNING.value, 
                started_at=datetime.now()
            )
            
            logger.info(f"Starting training for job: {job_id}")
            
            # Allocate GPU if requested and available
            device = self._allocate_gpu(job_id, request.use_gpu)
            
            # Load dataset
            logger.info(f"Loading dataset: {request.data_id}")
            df = self._load_dataset(request.data_id)
            
            # Prepare data
            X, y = self._prepare_data(df, request.target_column, request.task_type.value)
            
            # Get model instance
            logger.info(f"Creating model: {request.model_id}")
            model = self.model_factory.create_model(
                request.model_id,
                request.task_type.value,
                request.hyperparameters
            )
            
            # Log parameters to MLflow
            if mlflow_run:
                self.mlflow_tracker.log_params({
                    'model_id': request.model_id,
                    'task_type': request.task_type.value,
                    'epochs': request.epochs,
                    'batch_size': request.batch_size,
                    'learning_rate': request.learning_rate,
                    **request.hyperparameters
                })
            
            # Train model with progress tracking
            trained_model, metrics = await self._train_with_progress(
                job_id=job_id,
                model=model,
                X=X,
                y=y,
                request=request,
                device=device,
                mlflow_run=mlflow_run
            )
            
            # Save trained model
            logger.info(f"Saving trained model for job: {job_id}")
            model_path = await self._save_trained_model(
                job_id=job_id,
                model=trained_model,
                model_id=request.model_id
            )
            
            # Update job as completed
            self.postgres.update_job_status(
                job_id,
                JobStatus.COMPLETED.value,
                completed_at=datetime.now(),
                best_metrics=metrics,
                final_model_path=model_path
            )
            
            # Log final metrics to MLflow
            if mlflow_run:
                self.mlflow_tracker.log_metrics(metrics)
                self.mlflow_tracker.end_run()
            
            logger.info(f"Training completed for job: {job_id}")
            
        except Exception as e:
            logger.error(f"Training failed for job {job_id}: {e}")
            
            # Update job as failed
            self.postgres.update_job_status(
                job_id,
                JobStatus.FAILED.value,
                completed_at=datetime.now(),
                error_message=str(e)
            )
            
            # End MLflow run with failure
            if mlflow_run:
                self.mlflow_tracker.end_run(status="FAILED")
            
            raise
        finally:
            # Release GPU
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
    
    def _allocate_gpu(self, job_id: str, use_gpu: bool) -> str:
        """Allocate GPU device for training"""
        if use_gpu and self.gpu_available:
            # Simple round-robin GPU allocation
            gpu_id = len(self.active_jobs) % self.num_gpus
            device = f"cuda:{gpu_id}"
            
            self.postgres.update_job_status(job_id, JobStatus.RUNNING.value, gpu_allocated=device)
            logger.info(f"Allocated GPU {device} for job {job_id}")
            
            return device
        else:
            device = "cpu"
            logger.info(f"Using CPU for job {job_id}")
            return device
    
    def _load_dataset(self, data_id: str) -> pd.DataFrame:
        """Load dataset from MinIO"""
        try:
            # Download dataset
            data_bytes = download_dataset_bytes(data_id)
            
            # Parse as CSV
            df = pd.read_csv(io.BytesIO(data_bytes))
            
            logger.info(f"Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load dataset {data_id}: {e}")
            raise
    
    def _prepare_data(self, df: pd.DataFrame, target_column: Optional[str], task_type: str):
        """Prepare features and target"""
        # Auto-detect target if not provided
        if target_column is None:
            target_column = df.columns[-1]
            logger.info(f"Auto-detected target column: {target_column}")
        
        # Split features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        logger.info(f"Prepared data: X shape {X.shape}, y shape {y.shape}")
        return X, y
    
    async def _train_with_progress(
        self, 
        job_id: str, 
        model: Any, 
        X, 
        y, 
        request: TrainingRequest,
        device: str,
        mlflow_run: Any
    ):
        """
        Train model with progress tracking.
        This is a simplified version - in production would use PyTorch Lightning.
        """
        from sklearn.model_selection import train_test_split
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        logger.info(f"Training set: {len(X_train)}, Validation set: {len(X_val)}")
        
        # For sklearn models, training is single-step
        if hasattr(model, 'fit'):
            logger.info("Training sklearn model...")
            model.fit(X_train, y_train)
            
            # Calculate metrics
            from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
            
            if request.task_type.value == 'classification':
                train_pred = model.predict(X_train)
                val_pred = model.predict(X_val)
                
                train_acc = accuracy_score(y_train, train_pred)
                val_acc = accuracy_score(y_val, val_pred)
                
                metrics = {
                    'train_accuracy': float(train_acc),
                    'val_accuracy': float(val_acc)
                }
                
                logger.info(f"Training accuracy: {train_acc:.4f}, Validation accuracy: {val_acc:.4f}")
            
            else:  # regression
                train_pred = model.predict(X_train)
                val_pred = model.predict(X_val)
                
                train_rmse = mean_squared_error(y_train, train_pred, squared=False)
                val_rmse = mean_squared_error(y_val, val_pred, squared=False)
                val_r2 = r2_score(y_val, val_pred)
                
                metrics = {
                    'train_rmse': float(train_rmse),
                    'val_rmse': float(val_rmse),
                    'val_r2': float(val_r2)
                }
                
                logger.info(f"Validation RMSE: {val_rmse:.4f}, R2: {val_r2:.4f}")
            
            # Save metrics to database
            self.postgres.save_training_metrics(job_id, epoch=1, metrics=metrics)
            
            # Update progress to 100%
            self.postgres.update_job_status(job_id, JobStatus.RUNNING.value, current_epoch=request.epochs)
            
            return model, metrics
        
        else:
            raise ValueError(f"Model {request.model_id} does not have fit() method")
    
    async def _save_trained_model(self, job_id: str, model: Any, model_id: str) -> str:
        """Save trained model to MinIO"""
        # Serialize model
        model_bytes = pickle.dumps(model)
        
        # Generate object name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"{model_id}/{job_id}_{timestamp}.pkl"
        
        # Upload to MinIO
        minio_path = self.minio.upload_model(model_bytes, object_name)
        
        # Get file size
        file_size = self.minio.get_object_size(object_name)
        
        logger.info(f"Saved model to {minio_path} ({file_size} MB)")
        
        return minio_path
    
    def get_job_status(self, job_id: str) -> Optional[TrainingJobResponse]:
        """Get status of a training job"""
        job = self.postgres.get_job(job_id)
        
        if not job:
            return None
        
        # Calculate progress percentage
        progress = 0.0
        if job['total_epochs'] > 0 and job['current_epoch']:
            progress = (job['current_epoch'] / job['total_epochs']) * 100
        
        return TrainingJobResponse(
            job_id=job['job_id'],
            status=JobStatus(job['status']),
            model_id=job['model_id'],
            data_id=job['data_id'],
            created_at=job['created_at'],
            started_at=job.get('started_at'),
            completed_at=job.get('completed_at'),
            current_epoch=job.get('current_epoch'),
            total_epochs=job['total_epochs'],
            progress_percentage=progress,
            gpu_allocated=job.get('gpu_allocated'),
            mlflow_run_id=job.get('mlflow_run_id'),
            mlflow_experiment_id=job.get('mlflow_experiment_id'),
            best_metrics=job.get('best_metrics'),
            final_model_path=job.get('final_model_path'),
            error_message=job.get('error_message')
        )
    
    def list_jobs(self, status: Optional[str] = None, limit: int = 10) -> list:
        """List training jobs"""
        jobs = self.postgres.list_jobs(status=status, limit=limit)
        
        return [
            TrainingJobResponse(
                job_id=job['job_id'],
                status=JobStatus(job['status']),
                model_id=job['model_id'],
                data_id=job['data_id'],
                created_at=job['created_at'],
                started_at=job.get('started_at'),
                completed_at=job.get('completed_at'),
                current_epoch=job.get('current_epoch'),
                total_epochs=job['total_epochs'],
                progress_percentage=(job.get('current_epoch', 0) / job['total_epochs'] * 100) if job['total_epochs'] > 0 else 0,
                gpu_allocated=job.get('gpu_allocated'),
                mlflow_run_id=job.get('mlflow_run_id'),
                best_metrics=job.get('best_metrics'),
                final_model_path=job.get('final_model_path')
            )
            for job in jobs
        ]


# Global instance
_orchestrator: Optional[TrainingOrchestrator] = None


def get_orchestrator() -> TrainingOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = TrainingOrchestrator()
    return _orchestrator

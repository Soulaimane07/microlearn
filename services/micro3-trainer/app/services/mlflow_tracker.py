# app/services/mlflow_tracker.py
# --------------------------------------------------------------------
# MLflow integration for experiment tracking.
# --------------------------------------------------------------------
from typing import Dict, Any, Optional
import mlflow
from mlflow.tracking import MlflowClient

from app.core.config import settings
from app.core.logger import logger


class MLflowTracker:
    """MLflow experiment tracking wrapper"""
    
    def __init__(self):
        """Initialize MLflow tracker"""
        try:
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            self.client = MlflowClient()
            self.connected = True
            logger.info(f"MLflow connected: {settings.MLFLOW_TRACKING_URI}")
        except Exception as e:
            logger.warning(f"MLflow connection failed: {e}. Tracking disabled.")
            self.connected = False
    
    def start_run(
        self, 
        experiment_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ):
        """
        Start a new MLflow run.
        
        Args:
            experiment_name: Experiment name
            run_name: Optional run name
            tags: Optional tags
            
        Returns:
            MLflow run object or None
        """
        if not self.connected:
            return None
        
        try:
            # Set or create experiment
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment is None:
                experiment_id = mlflow.create_experiment(experiment_name)
            else:
                experiment_id = experiment.experiment_id
            
            # Start run
            run = mlflow.start_run(
                experiment_id=experiment_id,
                run_name=run_name,
                tags=tags
            )
            
            logger.info(f"Started MLflow run: {run.info.run_id}")
            return run
            
        except Exception as e:
            logger.error(f"Failed to start MLflow run: {e}")
            return None
    
    def log_params(self, params: Dict[str, Any]):
        """Log parameters to MLflow"""
        if not self.connected:
            return
        
        try:
            mlflow.log_params(params)
            logger.debug(f"Logged {len(params)} parameters to MLflow")
        except Exception as e:
            logger.error(f"Failed to log params: {e}")
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics to MLflow"""
        if not self.connected:
            return
        
        try:
            mlflow.log_metrics(metrics, step=step)
            logger.debug(f"Logged {len(metrics)} metrics to MLflow")
        except Exception as e:
            logger.error(f"Failed to log metrics: {e}")
    
    def log_artifact(self, local_path: str):
        """Log artifact to MLflow"""
        if not self.connected:
            return
        
        try:
            mlflow.log_artifact(local_path)
            logger.debug(f"Logged artifact: {local_path}")
        except Exception as e:
            logger.error(f"Failed to log artifact: {e}")
    
    def log_model(self, model: Any, artifact_path: str):
        """Log model to MLflow"""
        if not self.connected:
            return
        
        try:
            mlflow.sklearn.log_model(model, artifact_path)
            logger.info(f"Logged model to MLflow: {artifact_path}")
        except Exception as e:
            logger.error(f"Failed to log model: {e}")
    
    def end_run(self, status: str = "FINISHED"):
        """End the current MLflow run"""
        if not self.connected:
            return
        
        try:
            mlflow.end_run(status=status)
            logger.info(f"Ended MLflow run with status: {status}")
        except Exception as e:
            logger.error(f"Failed to end run: {e}")
    
    def get_run(self, run_id: str):
        """Get MLflow run by ID"""
        if not self.connected:
            return None
        
        try:
            return self.client.get_run(run_id)
        except Exception as e:
            logger.error(f"Failed to get run {run_id}: {e}")
            return None
    
    def search_runs(
        self, 
        experiment_name: str,
        filter_string: Optional[str] = None,
        max_results: int = 10
    ):
        """Search MLflow runs"""
        if not self.connected:
            return []
        
        try:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment is None:
                return []
            
            runs = self.client.search_runs(
                experiment_ids=[experiment.experiment_id],
                filter_string=filter_string,
                max_results=max_results
            )
            
            return runs
        except Exception as e:
            logger.error(f"Failed to search runs: {e}")
            return []

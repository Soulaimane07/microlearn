# app/storage/postgres_client.py
# --------------------------------------------------------------------
# PostgreSQL client for storing training job metadata and metrics.
# --------------------------------------------------------------------
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from app.core.config import settings
from app.core.logger import logger


class PostgresClient:
    """PostgreSQL client for training metadata"""
    
    def __init__(self):
        """Initialize PostgreSQL client"""
        self.conn_params = {
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT,
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "database": settings.POSTGRES_DB
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.conn_params)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_db(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Training jobs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_jobs (
                    job_id VARCHAR(255) PRIMARY KEY,
                    model_id VARCHAR(255) NOT NULL,
                    data_id VARCHAR(255) NOT NULL,
                    task_type VARCHAR(50) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    
                    current_epoch INTEGER DEFAULT 0,
                    total_epochs INTEGER NOT NULL,
                    
                    gpu_allocated VARCHAR(50),
                    
                    mlflow_run_id VARCHAR(255),
                    mlflow_experiment_id VARCHAR(255),
                    
                    hyperparameters JSONB,
                    best_metrics JSONB,
                    
                    final_model_path TEXT,
                    error_message TEXT
                )
            """)
            
            # Training metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_metrics (
                    id SERIAL PRIMARY KEY,
                    job_id VARCHAR(255) REFERENCES training_jobs(job_id) ON DELETE CASCADE,
                    epoch INTEGER NOT NULL,
                    train_loss FLOAT,
                    val_loss FLOAT,
                    train_accuracy FLOAT,
                    val_accuracy FLOAT,
                    learning_rate FLOAT,
                    additional_metrics JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    UNIQUE(job_id, epoch)
                )
            """)
            
            # Checkpoints table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id VARCHAR(255) PRIMARY KEY,
                    job_id VARCHAR(255) REFERENCES training_jobs(job_id) ON DELETE CASCADE,
                    epoch INTEGER NOT NULL,
                    minio_path TEXT NOT NULL,
                    metrics JSONB,
                    file_size_mb FLOAT,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON training_jobs(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_created ON training_jobs(created_at DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_job ON training_metrics(job_id, epoch)")
            
            logger.info("Database tables initialized successfully")
    
    def create_training_job(self, job_data: Dict[str, Any]) -> str:
        """Create a new training job"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO training_jobs (
                    job_id, model_id, data_id, task_type, status,
                    total_epochs, hyperparameters, mlflow_run_id, mlflow_experiment_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING job_id
            """, (
                job_data['job_id'],
                job_data['model_id'],
                job_data['data_id'],
                job_data['task_type'],
                job_data.get('status', 'pending'),
                job_data['total_epochs'],
                json.dumps(job_data.get('hyperparameters', {})),
                job_data.get('mlflow_run_id'),
                job_data.get('mlflow_experiment_id')
            ))
            
            result = cursor.fetchone()
            logger.info(f"Created training job: {result[0]}")
            return result[0]
    
    def update_job_status(self, job_id: str, status: str, **kwargs):
        """Update job status and other fields"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic UPDATE query
            update_fields = ["status = %s"]
            values = [status]
            
            if 'started_at' in kwargs:
                update_fields.append("started_at = %s")
                values.append(kwargs['started_at'])
            
            if 'completed_at' in kwargs:
                update_fields.append("completed_at = %s")
                values.append(kwargs['completed_at'])
            
            if 'current_epoch' in kwargs:
                update_fields.append("current_epoch = %s")
                values.append(kwargs['current_epoch'])
            
            if 'gpu_allocated' in kwargs:
                update_fields.append("gpu_allocated = %s")
                values.append(kwargs['gpu_allocated'])
            
            if 'best_metrics' in kwargs:
                update_fields.append("best_metrics = %s")
                values.append(json.dumps(kwargs['best_metrics']))
            
            if 'final_model_path' in kwargs:
                update_fields.append("final_model_path = %s")
                values.append(kwargs['final_model_path'])
            
            if 'error_message' in kwargs:
                update_fields.append("error_message = %s")
                values.append(kwargs['error_message'])
            
            values.append(job_id)
            
            query = f"UPDATE training_jobs SET {', '.join(update_fields)} WHERE job_id = %s"
            cursor.execute(query, values)
            
            logger.debug(f"Updated job {job_id}: status={status}")
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get training job by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM training_jobs WHERE job_id = %s", (job_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def list_jobs(self, status: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """List training jobs with optional filtering"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            if status:
                cursor.execute(
                    "SELECT * FROM training_jobs WHERE status = %s ORDER BY created_at DESC LIMIT %s",
                    (status, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM training_jobs ORDER BY created_at DESC LIMIT %s",
                    (limit,)
                )
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def save_training_metrics(self, job_id: str, epoch: int, metrics: Dict[str, float]):
        """Save training metrics for an epoch"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            additional = {k: v for k, v in metrics.items() 
                         if k not in ['train_loss', 'val_loss', 'train_accuracy', 'val_accuracy', 'learning_rate']}
            
            cursor.execute("""
                INSERT INTO training_metrics (
                    job_id, epoch, train_loss, val_loss, train_accuracy, 
                    val_accuracy, learning_rate, additional_metrics
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_id, epoch) DO UPDATE SET
                    train_loss = EXCLUDED.train_loss,
                    val_loss = EXCLUDED.val_loss,
                    train_accuracy = EXCLUDED.train_accuracy,
                    val_accuracy = EXCLUDED.val_accuracy,
                    learning_rate = EXCLUDED.learning_rate,
                    additional_metrics = EXCLUDED.additional_metrics
            """, (
                job_id, epoch,
                metrics.get('train_loss'),
                metrics.get('val_loss'),
                metrics.get('train_accuracy'),
                metrics.get('val_accuracy'),
                metrics.get('learning_rate'),
                json.dumps(additional) if additional else None
            ))
    
    def get_job_metrics(self, job_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent metrics for a job"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM training_metrics 
                WHERE job_id = %s 
                ORDER BY epoch DESC 
                LIMIT %s
            """, (job_id, limit))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    def save_checkpoint(self, checkpoint_data: Dict[str, Any]):
        """Save checkpoint information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO checkpoints (
                    checkpoint_id, job_id, epoch, minio_path, metrics, file_size_mb
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                checkpoint_data['checkpoint_id'],
                checkpoint_data['job_id'],
                checkpoint_data['epoch'],
                checkpoint_data['minio_path'],
                json.dumps(checkpoint_data.get('metrics', {})),
                checkpoint_data.get('file_size_mb')
            ))
            
            logger.info(f"Saved checkpoint: {checkpoint_data['checkpoint_id']}")
    
    def get_job_checkpoints(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all checkpoints for a job"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT * FROM checkpoints 
                WHERE job_id = %s 
                ORDER BY epoch DESC
            """, (job_id,))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]


# Global instance
_postgres_client: Optional[PostgresClient] = None


def get_postgres_client() -> PostgresClient:
    """Get or create PostgreSQL client instance"""
    global _postgres_client
    if _postgres_client is None:
        _postgres_client = PostgresClient()
    return _postgres_client


def init_db():
    """Initialize database tables"""
    try:
        get_postgres_client().init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

# app/storage/postgres_client.py
# --------------------------------------------------------------------
# PostgreSQL client for model catalog persistence.
# Stores model selection history and catalog metadata.
# --------------------------------------------------------------------
import psycopg2
from contextlib import contextmanager
from typing import Optional, Dict, Any, List

from app.core.config import settings
from app.core.logger import logger


@contextmanager
def get_conn():
    """Get a database connection context manager"""
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize database tables for model selector"""
    create_tables_sql = """
    -- Model catalog table
    CREATE TABLE IF NOT EXISTS model_catalog (
        model_id VARCHAR(100) PRIMARY KEY,
        model_name VARCHAR(255) NOT NULL,
        model_class VARCHAR(255) NOT NULL,
        category VARCHAR(50) NOT NULL,
        task_types TEXT[] NOT NULL,
        interpretability VARCHAR(20),
        training_complexity VARCHAR(20),
        supports_gpu BOOLEAN DEFAULT FALSE,
        default_params JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Model selection history table
    CREATE TABLE IF NOT EXISTS selection_history (
        id SERIAL PRIMARY KEY,
        dataset_hash VARCHAR(64),
        dataset_rows INTEGER,
        dataset_columns INTEGER,
        task_type VARCHAR(50) NOT NULL,
        metric VARCHAR(50) NOT NULL,
        selected_models TEXT[] NOT NULL,
        top_model VARCHAR(100),
        analysis JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Model performance tracking (for feedback loop)
    CREATE TABLE IF NOT EXISTS model_performance (
        id SERIAL PRIMARY KEY,
        model_id VARCHAR(100) NOT NULL,
        dataset_hash VARCHAR(64),
        metric_name VARCHAR(50) NOT NULL,
        metric_value FLOAT NOT NULL,
        training_time_seconds FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (model_id) REFERENCES model_catalog(model_id) ON DELETE CASCADE
    );

    -- Create indexes for better query performance
    CREATE INDEX IF NOT EXISTS idx_selection_history_task_type ON selection_history(task_type);
    CREATE INDEX IF NOT EXISTS idx_selection_history_created ON selection_history(created_at);
    CREATE INDEX IF NOT EXISTS idx_model_performance_model ON model_performance(model_id);
    """
    
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(create_tables_sql)
                conn.commit()
        logger.info("Database tables initialized successfully")
    except Exception as exc:
        logger.error(f"Failed to initialize database: {exc}")
        raise


def save_selection(
    dataset_hash: Optional[str],
    dataset_rows: int,
    dataset_columns: int,
    task_type: str,
    metric: str,
    selected_models: List[str],
    top_model: str,
    analysis: Dict[str, Any]
) -> Optional[int]:
    """Save a model selection to history"""
    sql = """
    INSERT INTO selection_history 
    (dataset_hash, dataset_rows, dataset_columns, task_type, metric, selected_models, top_model, analysis)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    
    try:
        import json
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (
                    dataset_hash,
                    dataset_rows,
                    dataset_columns,
                    task_type,
                    metric,
                    selected_models,
                    top_model,
                    json.dumps(analysis)
                ))
                result = cur.fetchone()
                conn.commit()
                return result[0] if result else None
    except Exception as exc:
        logger.warning(f"Failed to save selection history: {exc}")
        return None


def get_selection_history(
    task_type: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Get selection history, optionally filtered by task type"""
    sql = """
    SELECT id, dataset_hash, dataset_rows, dataset_columns, task_type, 
           metric, selected_models, top_model, analysis, created_at
    FROM selection_history
    """
    
    params = []
    if task_type:
        sql += " WHERE task_type = %s"
        params.append(task_type)
    
    sql += " ORDER BY created_at DESC LIMIT %s"
    params.append(limit)
    
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
                
                return [
                    {
                        "id": row[0],
                        "dataset_hash": row[1],
                        "dataset_rows": row[2],
                        "dataset_columns": row[3],
                        "task_type": row[4],
                        "metric": row[5],
                        "selected_models": row[6],
                        "top_model": row[7],
                        "analysis": row[8],
                        "created_at": row[9].isoformat() if row[9] else None
                    }
                    for row in rows
                ]
    except Exception as exc:
        logger.warning(f"Failed to get selection history: {exc}")
        return []


def save_model_performance(
    model_id: str,
    dataset_hash: Optional[str],
    metric_name: str,
    metric_value: float,
    training_time: Optional[float] = None
) -> bool:
    """Save model performance metrics for future reference"""
    sql = """
    INSERT INTO model_performance 
    (model_id, dataset_hash, metric_name, metric_value, training_time_seconds)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (
                    model_id,
                    dataset_hash,
                    metric_name,
                    metric_value,
                    training_time
                ))
                conn.commit()
                return True
    except Exception as exc:
        logger.warning(f"Failed to save model performance: {exc}")
        return False


def get_model_performance_stats(model_id: str) -> Dict[str, Any]:
    """Get performance statistics for a model"""
    sql = """
    SELECT metric_name, 
           AVG(metric_value) as avg_value,
           MIN(metric_value) as min_value,
           MAX(metric_value) as max_value,
           COUNT(*) as count
    FROM model_performance
    WHERE model_id = %s
    GROUP BY metric_name
    """
    
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (model_id,))
                rows = cur.fetchall()
                
                return {
                    row[0]: {
                        "avg": float(row[1]) if row[1] else None,
                        "min": float(row[2]) if row[2] else None,
                        "max": float(row[3]) if row[3] else None,
                        "count": row[4]
                    }
                    for row in rows
                }
    except Exception as exc:
        logger.warning(f"Failed to get model performance stats: {exc}")
        return {}

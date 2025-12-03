# app/storage/postgres_client.py
# --------------------------------------------------------------------
# Lightweight Postgres helper for simple metadata insertion. For
# production use, replace with a connection pool (psycopg2.pool or SQLAlchemy).
# --------------------------------------------------------------------

import psycopg2
from contextlib import contextmanager
from app.core.config import settings
from app.core.logger import logger

@contextmanager
def get_conn():
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    try:
        yield conn
    finally:
        conn.close()

def insert_file_record(object_name: str, filename: str, rows: int):
    sql = """
    INSERT INTO dataprep_files (object_name, filename, rows, created_at)
    VALUES (%s, %s, %s, NOW())
    """
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (object_name, filename, rows))
                conn.commit()
    except Exception as exc:
        logger.warning(f"Failed to insert file record: {exc}")

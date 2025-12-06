# app/core/logger.py
# --------------------------------------------------------------------
# Logging configuration using loguru for readable logs.
# --------------------------------------------------------------------
from loguru import logger
import sys

# Remove default handler and add custom one
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

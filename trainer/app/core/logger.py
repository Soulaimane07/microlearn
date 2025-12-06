# app/core/logger.py
# --------------------------------------------------------------------
# Logging configuration for Trainer microservice.
# Provides structured logging with color output.
# --------------------------------------------------------------------
import sys
from loguru import logger
from app.core.config import settings

# Remove default logger
logger.remove()

# Add custom logger with formatting
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO"
)

# Add file logger for errors
logger.add(
    "logs/trainer_errors.log",
    rotation="10 MB",
    retention="7 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# Export logger
__all__ = ["logger"]

# app/core/logger.py
# --------------------------------------------------------------------
# Thin logging wrapper using loguru for readable logs during development.
# --------------------------------------------------------------------
from loguru import logger

# Default formatting is fine for development. In production you might
# route these to stdout structured logs or to a logging system.
logger.add(lambda msg: print(msg, end=""))

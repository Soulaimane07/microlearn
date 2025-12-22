# app/services/publisher.py
import json
from app.core.logger import logger
from app.services.nats_client import nc, connect_nats

async def publish_step_done(step_name: str, payload: dict):
    try:
        if not nc.is_connected:
            await connect_nats()
        message = json.dumps(payload).encode()
        await nc.publish(f"pipeline.{step_name}.done", message)
        logger.info(f"Published {step_name} done message to orchestrator")
    except Exception as e:
        logger.error(f"Failed to publish step done: {e}")
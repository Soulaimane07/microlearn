import json
from nats.aio.client import Client as NATS

nc = NATS()

async def connect_nats():
    if not nc.is_connected:
        await nc.connect("nats://nats:4222")

async def publish_step_done(step_name: str, payload: dict):
    await connect_nats()
    subject = f"pipeline.{step_name}.done"
    await nc.publish(subject, json.dumps(payload).encode())
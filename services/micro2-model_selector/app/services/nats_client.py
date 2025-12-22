# app/services/nats_client.py
import asyncio
from nats.aio.client import Client as NATS

nc = NATS()  # global NATS client

async def connect_nats(servers=["nats://localhost:4222"]):
    if not nc.is_connected:
        await nc.connect(servers=servers)
    return nc
# import asyncio
import aioredis

from starlette.applications import Starlette
from starlette.config import Config


config = Config('.env')
REDIS_URL = config('REDIS_URL')


async def get(key: str):
    # Redis client bound to single connection (no auto reconnection).
    redis = await aioredis.create_redis(REDIS_URL)

    await redis.set('key', 'yay')
    val = await redis.get(key)
    yield val

    # gracefully closing underlying connection
    redis.close()
    await redis.wait_closed()

from fastapi import FastAPI

from .router import api_router
from guid import settings
from guid.db import (open_database_connection_pool,
                     close_database_connection_pool)


# Setup app
# import redis
# from guid import settings
# cache = redis.Redis.from_url(url=settings.REDIS_URL)

app = FastAPI()

app.debug = settings.DEBUG

app.add_event_handler('startup', open_database_connection_pool)
app.add_event_handler('shutdown', close_database_connection_pool)

app.include_router(api_router)


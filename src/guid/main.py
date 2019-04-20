"""The main app is here."""
from fastapi import FastAPI
from .router import api_router
from guid import settings
from guid.db import (open_database_connection_pool,
                     close_database_connection_pool)


app = FastAPI()

app.debug = settings.DEBUG

app.add_event_handler('startup', open_database_connection_pool)
app.add_event_handler('shutdown', close_database_connection_pool)

app.include_router(api_router)


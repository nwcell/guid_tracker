"""Initialize the DB pool.

Use the `database` attribute as your interface to the db.
"""
import databases
from guid import settings


database = databases.Database(settings.DATABASE_URL)


async def open_database_connection_pool():
    await database.connect()


async def close_database_connection_pool():
    await database.disconnect()

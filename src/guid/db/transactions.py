"""Collection of db transactions."""
# pylint:disable=no-value-for-parameter
from datetime import datetime
from collections import namedtuple
from sqlalchemy import and_
from guid.db import database, guid_tracker


@database.transaction()
async def retrieve_guid_record(guid):
    """Retrieve a record by guid."""
    # Get guid
    query = guid_tracker.select().where(and_(
        guid_tracker.c.id == guid,
        guid_tracker.c.expire > datetime.now(),
    ))

    return await database.fetch_one(query)


@database.transaction()
async def create_guid_record(guid: str, name: str, expire: datetime) -> bool:
    """Create a name value with a guid as the pk."""
    # Clean old guids
    clean_query = guid_tracker.delete().where(and_(
        guid_tracker.c.expire < datetime.now(),
    ))
    await database.execute(clean_query)

    # Add new guid
    query = guid_tracker.insert().values(
        id=guid,
        expire=expire,
        name=name,
    )
    await database.execute(query)

    return True


@database.transaction()
async def update_guid_record(guid: str, name: str = None, expire: datetime = None):
    """Update a name value with a guid as the pk."""
    # Clean old guids
    clean_query = guid_tracker.delete().where(and_(
        guid_tracker.c.expire < datetime.now(),
    ))
    await database.execute(clean_query)

    # Update guids
    update = {}
    if expire:
        update['expire'] = expire
    if name:
        update['name'] = name

    update_query = guid_tracker.update().values(
        **update,
    ).where(
        guid_tracker.c.id == guid
    )
    await database.execute(update_query)

    # Get current guid
    query = guid_tracker.select().where(and_(
        guid_tracker.c.id == guid,
        guid_tracker.c.expire > datetime.now(),
    ))

    return await database.fetch_one(query)


@database.transaction()
async def delete_guid_record(guid):
    """Delete a guid record."""
    query = guid_tracker.delete().where(guid_tracker.c.id == guid)
    await database.execute(query)


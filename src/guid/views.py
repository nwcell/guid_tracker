"""API views."""
import uuid
from typing import Type, List
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from sqlalchemy import and_
from guid.db import (guid_tracker, database, create_guid_record,
                     update_guid_record, retrieve_guid_record,
                     delete_guid_record)
from guid.serializers import GuidIn, GuidUpdate, GuidOut
from guid.util import validate_guid
from guid.cache import cache


router = APIRouter()


@router.get('/')
async def list_guid() -> List[dict]:
    """
    Lists everything.

    I added this for my own convenience during dev.
    """
    query = guid_tracker.select()
    results = await database.fetch_all(query)
    return results


@router.get('/{guid}', response_model=GuidOut)
async def retrieve_guid(guid: str):
    """
    Retrieves a single record from the DB.

    Checks redis for a non-expired record before doing anything.
    """
    cached_data = await cache.get(guid)
    if cached_data:
        return cached_data

    results = await retrieve_guid_record(guid)

    if not results:
        raise HTTPException(status_code=404, detail='Item not found')

    return GuidOut(
        id=results.id,
        expire=results.expire,
        name=results.name,
    )


@router.post('/', status_code=201, response_model=GuidOut)
async def create_guid(data: GuidIn) -> Type[GuidOut]:
    """
    Create a record w/o specifying a guid.

    Also cleans up expired records & caches the new record.
    """
    guid = uuid.uuid4().hex
    validated = data.dict()

    try:
        await create_guid_record(guid, validated['name'], validated['expire'])
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

    # Build serialized response
    out = GuidOut(
        id=guid,
        expire=validated['expire'],
        name=validated['name'],
    )

    # Cache stuff
    ttl = validated['expire'] - datetime.now(timezone.utc)
    await cache.set(guid, out, ttl=ttl.seconds)

    return out


@router.post('/{guid}', status_code=201, response_model=GuidOut)
async def create_specific_guid(guid: str, data: GuidIn):
    """
    Create a record w/ a guid specified in the path.

    Also cleans up expired records & caches the new record.

    Raises an exception if you try to overwrite an existing record.
    """
    try:
        guid = validate_guid(guid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid guid")

    validated = data.dict()

    try:
        await create_guid_record(guid, validated['name'], validated['expire'])
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

    # Build serialized response
    out = GuidOut(
        id=guid,
        expire=validated['expire'],
        name=validated['name'],
    )

    # Cache stuff
    ttl = validated['expire'] - datetime.now(timezone.utc)
    await cache.set(guid, out, ttl=ttl.seconds)

    return out


@router.patch('/{guid}', response_model=GuidOut)
async def update_guid(guid: str, data: GuidUpdate):
    """
    Updates a record.

    Also cleans up expired records & caches the updated record.
    """
    validated = data.dict()

    try:
        results = await update_guid_record(guid, validated['name'], validated['expire'])
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

    if not results:
        raise HTTPException(status_code=404, detail="Item not found")

    # Build serialized response
    out = GuidOut(
        id=results.id,
        expire=results.expire,
        name=results.name,
    )

    # Cache stuff
    ttl = results.expire - datetime.now()
    await cache.set(guid, out, ttl=ttl.seconds)

    return out


@router.delete('/{guid}')
async def destroy_guid(guid: str):
    """
    Removes a record.

    Also removes the related cached record.
    """
    try:
        await delete_guid_record(guid)
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

    await cache.delete(guid)

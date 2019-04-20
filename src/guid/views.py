import uuid
from typing import Dict, Type
from datetime import datetime

from fastapi import APIRouter, HTTPException

from guid.util import validate_guid, default_expire
from guid.db import guid_tracker, database
from guid.serializers import GuidIn, GuidUpdate, GuidOut
from guid.util import validate_guid
# from .main import cache


router = APIRouter()


@router.get('/')
async def list_guid():
    query = guid_tracker.select()
    results = await database.fetch_all(query)
    return results


@router.get('/{guid}', response_model=GuidOut)
async def read_guid(guid: str):
    # TODO: Add Cache
    # cache.set('foo', 'bar')
    # cached_data = cache.get(guid)
    query = guid_tracker.select().where(guid_tracker.c.id == guid)
    results = await database.fetch_one(query)

    if not results:
        raise HTTPException(status_code=404, detail="Item not found")

    return GuidOut(
        id=results.id,
        expire=results.expire,
        name=results.name,
    )


@router.post('/', status_code=201, response_model=GuidOut)
async def create_guid(data: GuidIn) -> Type[GuidOut]:
    guid = uuid.uuid4().hex
    validated = data.dict()

    query = guid_tracker.insert().values(
        id=guid,
        expire=validated['expire'],
        name=validated['name'],
    )

    try:
        await database.execute(query)
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

    return GuidOut(
        id=guid,
        expire=validated['expire'],
        name=validated['name'],
    )


@router.post('/{guid}', status_code=201, response_model=GuidOut)
async def create_specific_guid(guid: str, data: GuidIn):
    guid = validate_guid(guid)
    validated = data.dict()

    query = guid_tracker.insert().values(
        id=guid,
        expire=validated['expire'],
        name=validated['name'],
    )

    try:
        await database.execute(query)
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

    return GuidOut(
        id=guid,
        expire=validated['expire'],
        name=validated['name'],
    )


@router.patch('/{guid}', response_model=GuidOut)
async def update_guid(guid: str, data: GuidUpdate):
    validated = data.dict()

    update = {}
    if validated['expire']:
        update['expire'] = validated['expire']
    if validated['name']:
        update['name'] = validated['name']

    query = guid_tracker.update().values(
        **update,
    ).where(
        guid_tracker.c.id == guid
    )
    await database.execute(query)

    # Get updated record
    query = guid_tracker.select().where(guid_tracker.c.id == guid)
    results = await database.fetch_one(query)

    if not results:
        raise HTTPException(status_code=404, detail="Item not found")

    return GuidOut(
        id=results.id,
        expire=results.expire,
        name=results.name,
    )


@router.delete('/{guid}')
async def destroy_guid(guid: str):
    query = guid_tracker.delete().where(guid_tracker.c.id == guid)

    try:
        await database.execute(query)
    except Exception as detail:
        raise HTTPException(status_code=400, detail=f'{detail}')

from guid.db import database, guid_tracker


@database.transaction()
async def list_guid():
    query = guid_tracker.select()
    results = await database.execute(query)
    return results


@database.transaction()
async def retrieve_guid(guid):
    query = guid_tracker.query.get(guid)
    results = await database.execute(query)
    return results


@database.transaction()
async def create_guid_tracker(guid):
    query = guid_tracker.insert().values(
        text="you won't see me",
        completed=True
    )
    await database.execute(query)
    raise RuntimeError()


# @database.transaction()
# async def populate_note(request):
#     # This database insert occurs within a transaction.
#     # It will be rolled back by the `RuntimeError`.
#     query = notes.insert().values(text="you won't see me", completed=True)
#     await database.execute(query)
#     raise RuntimeError()

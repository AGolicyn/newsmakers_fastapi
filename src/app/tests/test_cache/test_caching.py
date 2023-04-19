import pytest
import uuid
import string
import redis.asyncio as redis

from random import randint
from app.db.cache import get_from_cache, set_to_cache
from app.service.repository import get_entity_titles
from app.schema.country_schm import EntityTitles


connection = redis.from_url("redis://cache", decode_responses=True)
fake_entities = EntityTitles(**{"entities": [uuid.uuid4() for _ in range(8)]})
fake_data = [[string.ascii_letters for _ in range(randint(5, 10))] for __ in range(8)]


@pytest.mark.asyncio
async def test_cache_return_none_if_no_cached():
    data = await get_from_cache(entities=fake_entities, conn=connection)
    assert data is None


@pytest.mark.asyncio
async def test_cache_can_set_data():
    await set_to_cache(entities=fake_entities, conn=connection, data=fake_data)
    data = await get_from_cache(entities=fake_entities, conn=connection)

    assert data == fake_data


@pytest.mark.asyncio
async def test_db_not_invoke_when_get_cached_data():
    # set to cache some data
    await set_to_cache(entities=fake_entities, conn=connection, data=fake_data)
    session = False

    data = await get_entity_titles(
        entities=fake_entities, conn=connection, session=session
    )

    assert data == fake_data

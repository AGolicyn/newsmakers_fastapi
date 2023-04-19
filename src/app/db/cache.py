import json

from redis.asyncio.client import Redis
from app.schema.country_schm import EntityTitles, EntityTitlesResponse


async def get_from_cache(
    entities: EntityTitles, conn: Redis
) -> list[EntityTitlesResponse] | None:
    base_entity = entities.entities[0]
    len_entities = len(entities.entities)
    data = await conn.get(f"{base_entity}:{len_entities}")
    if data:
        data = json.loads(data)
    return data


async def set_to_cache(
    entities: EntityTitles, conn: Redis, data: list[EntityTitlesResponse]
):
    base_entity = entities.entities[0]
    len_entities = len(entities.entities)
    await conn.set(f"{base_entity}:{len_entities}", json.dumps(data, default=str))

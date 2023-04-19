from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis
from app.crud import title
from app.db.cache import get_from_cache, set_to_cache
from app.schema.country_schm import EntityTitles


async def get_entity_titles(session: AsyncSession, entities: EntityTitles, conn: Redis):
    cached_data = await get_from_cache(entities=entities, conn=conn)
    if cached_data:
        return cached_data
    data = await title.get_entity_titles(session=session, entities=entities)
    await set_to_cache(entities=entities, conn=conn, data=data)
    return data

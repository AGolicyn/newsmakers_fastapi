from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.schema.country_schm import CountryDate, EntityTitles
from fastapi import HTTPException


async def get_daily_results(session: AsyncSession, item: CountryDate):
    res = await session.execute(text(""
                                         "SELECT entities#> '{%s}' FROM cons_data " % item.country
                                         + f"WHERE date(date) = date('{item.date}')"
                                         ))
    return res.scalars().all()[-1]


async def get_entity_titles(session: AsyncSession, entities: EntityTitles):
    ents = tuple(entities.entities)
    if len(entities.entities) == 1:
        ents = tuple(entities.entities * 2)

    res = await session.execute(text(
        "SELECT DISTINCT data FROM news_title "
        f"WHERE id IN {ents}"
    ))

    return res.scalars().all()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..schema.country_schm import CountryDate, EntityTitles


async def get_daily_results(session: AsyncSession, item: CountryDate):
    res = await session.execute(text(""
                                     "SELECT entities#> '{%s}' FROM cons_data " % item.country
                                     + f"WHERE date = date('{item.date}') "
                                       f"AND entities ? '{item.country}'"
                                     ))
    result = res.scalars().all()[-1]
    return result


async def get_entity_titles(session: AsyncSession, entities: EntityTitles):
    ents = tuple(entities.entities)
    if len(entities.entities) == 1:
        ents = tuple(entities.entities * 2)

    res = await session.execute(text(
        "SELECT DISTINCT data FROM news_title "
        f"WHERE id IN {ents}"
    ))

    return res.scalars().all()

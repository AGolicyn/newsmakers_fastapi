from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schema.country_schm import CountryDate, EntityTitles
from app.db.session import ConsolidatedData, NewsTitle


async def get_daily_results(session: AsyncSession, item: CountryDate):
    sel = await session.execute(
        select(ConsolidatedData.entities[item.country])
        .where(ConsolidatedData.date == item.date)
        .where(ConsolidatedData.entities.has_key(item.country))
    )
    result = sel.scalars().all()[-1]
    return result


async def get_entity_titles(session: AsyncSession, entities: EntityTitles):
    sel = await session.execute(
        select(NewsTitle.data)
        .where(NewsTitle.id.in_(entities.entities))
    )
    return sel.scalars().all()

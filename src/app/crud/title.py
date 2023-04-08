import datetime
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Date, desc
from app.schema.country_schm import CountryDate, EntityTitles, TrendRequest
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


async def get_sources(trend: TrendRequest, session: AsyncSession):
    stmt = select(NewsTitle.data['url'].astext).distinct() \
        .where(NewsTitle.data['country'].astext == trend.country)

    sources = await session.execute(stmt)
    return sources.all()

async def get_trand_interval(trend: TrendRequest, session: AsyncSession):
    interval = trend.date - datetime.timedelta(days=trend.day_offset)
    stmt = select(func.count(),
                  NewsTitle.data['url'].astext.label("url"),
                  NewsTitle.data['time'].astext.cast(Date).label("time")) \
        .where(NewsTitle.data['time'].astext.cast(Date) <= trend.date) \
        .where(NewsTitle.data['time'].astext.cast(Date) >= interval) \
        .where(NewsTitle.data['country'].astext == trend.country) \
        .where(func.lower(NewsTitle.data['title'].astext).like(trend.token)) \
        .group_by("time", "url") \
        .order_by(desc("time"))

    sel = await session.execute(stmt)
    res = sel.all()
    print(len(res))
    return res

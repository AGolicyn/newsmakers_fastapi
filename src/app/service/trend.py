from sqlalchemy.ext.asyncio import AsyncSession

from app.service.model.model import Trend, trend_calculator
from app.crud.title import get_trand_interval, get_sources
from app.schema.country_schm import TrendRequest


async def trend_factory(trend: TrendRequest, session: AsyncSession):
    trends = await get_trand_interval(trend=trend, session=session)
    all_sources = await get_sources(trend=trend, session=session)

    trends = [(Trend(item[2], item[0], item[1])) for item in trends]
    weighted_trends = trend_calculator(
        all_sources=all_sources,
        trends=trends,
        start_day=trend.date,
        offset=trend.day_offset,
    )

    return weighted_trends

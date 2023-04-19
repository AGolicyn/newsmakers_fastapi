import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from redis.asyncio.client import Redis

from .crud import title
from app.service.repository import get_entity_titles
from .schema.country_schm import (
    EntityTitles,
    CountryDate,
    CountryDateResponse,
    EntityTitlesResponse,
    TrendRequest,
    TrendResponse,
)
from .db.session import get_db
from .service.trend import trend_factory

app = FastAPI()

connection: Redis = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="POST",
    allow_headers="*",
)


@app.on_event("shutdown")
async def shutdown():
    await connection.close()


@app.post("/country", response_model=CountryDateResponse)
async def country_entities(item: CountryDate, session: AsyncSession = Depends(get_db)):
    return await title.get_daily_results(session=session, item=item)


@app.post("/titles", response_model=list[EntityTitlesResponse])
async def entity_titles(
    entities: EntityTitles, session: AsyncSession = Depends(get_db)
):
    return await get_entity_titles(session=session, entities=entities, conn=connection)


@app.post("/trend", response_model=list[TrendResponse])
async def test(trend: TrendRequest, session: AsyncSession = Depends(get_db)):
    return await trend_factory(trend=trend, session=session)

import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import title
from .schema.country_schm import EntityTitles, \
    CountryDate, CountryDateResponse, EntityTitlesResponse, \
    TrendRequest, TrendResponse
from .db.session import get_db
from .service.trend import trend_factory


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)


@app.post("/country", response_model=CountryDateResponse)
async def country_entities(item: CountryDate,
                           session: AsyncSession = Depends(get_db)):
    return await title.get_daily_results(session=session, item=item)


@app.post("/titles", response_model=list[EntityTitlesResponse])
async def entity_titles(entities: EntityTitles,
                        session: AsyncSession = Depends(get_db)):
    return await title.get_entity_titles(session=session, entities=entities)

@app.get("/trend/", response_model=list[TrendResponse])
async def test(country: str,
               token: str,
               date: str,
               day_offset: int,
               session: AsyncSession = Depends(get_db)):
    # return {country: country, token: token, date: date, day_offset: day_offset}
    trend = TrendRequest(country=country, token=token, date=date, day_offset=day_offset)
    return await trend_factory(trend=trend, session=session)
    # await title.test(trend=trend, session=session)
    # return {'Hey': True}

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import title
from .schema.country_schm import EntityTitles, \
    CountryDate, CountryDateResponse, EntityTitlesResponse
from .db.session import get_db


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

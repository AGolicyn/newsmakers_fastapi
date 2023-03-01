from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.crud import title
from app.schema.country_schm import EntityTitles, \
    CountryDate, CountryDateResponse, EntityTitlesResponse
from app.db.session import SessionLocal

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://*:8080",
    "http://0.0.0.0:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/country", response_model=CountryDateResponse)
async def country_entities(item: CountryDate, db: Session = Depends(get_db)):
    return title.get_daily_results(db=db, item=item)


@app.post("/titles", response_model=list[EntityTitlesResponse])
async def entity_titles(entities: EntityTitles, db: Session = Depends(get_db)):
    res = title.get_entity_titles(db=db, entities=entities)
    return res

from fastapi import FastAPI
from src.db.session import SessionLocal
from sqlalchemy.orm import Session
from src.crud import title
from fastapi import Depends
from src.schema.country_schm import EntityTitles, CountryDate, CountryDateResponse, EntityTitlesResponse

app = FastAPI()

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


from fastapi import FastAPI
from .db.session import SessionLocal
from sqlalchemy.orm import Session
from .crud import title
from fastapi import Depends
from .schema.country_schm import EntityTitles, CountryDate, CountryDateResponse, EntityTitlesResponse
from sqlalchemy import text, insert
from .db.session import *

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

@app.get("/")
async def getall(db: Session = Depends(get_db)):
    return db.execute(text("SELECT news_title.data FROM news_title")).scalars().all()

@app.post("/ins")
async def trins(data, db: Session = Depends(get_db)):
    print(data)
    tit = db.execute(insert(NewsTitle)
               .values(data=data)
               ).scalar_one_or_none()
    db.commit()
    return tit
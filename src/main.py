import datetime
import json

from fastapi import FastAPI
from src.db.session import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_daily_results(db: Session, date: datetime.date, country: str):
    print(country)
    res = db.execute(text(
        f"SELECT entities->> ('{country}') FROM cons_data "
        f"WHERE date(date) = date('{date}')"

    )).scalar_one_or_none()
    return json.loads(res)

day = datetime.date(2023, 2, 16)

def get_entity_titles(db:Session, day, country, entity, entity_name):
    res = db.execute(text(
        "SELECT data FROM news_title "
        "WHERE news_title.id::text IN "
            "(SELECT jsonb_array_elements_text(entities #> '{%s, %s, %s}') " % (country, entity, entity_name) +
            "FROM cons_data "
            f"WHERE date(date) = date('{day}'))"
    )).scalars().all()
    print(res)
    return res


@app.get("/")
async def root(db: Session = Depends(get_db)):
    res = get_daily_results(db=db, date=day, country='Russia')
    return res

@app.get("/hey")
async def brab(db: Session = Depends(get_db)):
    res = get_entity_titles(db=db, day=day, country='Russia', entity='LOC', entity_name='рф')
    return res


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


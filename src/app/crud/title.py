import pathlib
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schema.country_schm import CountryDate, EntityTitles
from fastapi import HTTPException


def get_daily_results(db: Session, item: CountryDate):
    res = db.execute(text(""
                          "SELECT entities#> '{%s}' FROM cons_data " % item.country
                          + f"WHERE date(date) = date('{item.date}')"
                          )).scalars().all()[0]
    return res


def get_entity_titles(db: Session, entities: EntityTitles):
    ents = tuple(entities.entities)
    if len(entities.entities) == 1:
        ents = tuple(entities.entities * 2)

    res = db.execute(text(
        "SELECT DISTINCT data FROM news_title "
        f"WHERE id IN {ents}"
    )).scalars().all()

    return res


def get_image_path(item: CountryDate):
    date = item.date
    country = item.country
    p = pathlib.Path(f'/media/images/{date.year}/{date.month}/'
                     f'{date.day}/{country}/LOC.png')
    if p.exists():
        return str(p)
    raise HTTPException(status_code=404, detail=f'Wordcloud images do not exists to {date}')

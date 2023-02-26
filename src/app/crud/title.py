import pathlib
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from ..schema.country_schm import CountryDate, EntityTitles
from fastapi import HTTPException

def get_daily_results(db: Session, item: CountryDate):
    res = db.execute(text(""
                          "SELECT entities#> '{%s}' FROM cons_data " % item.country +
                          f"WHERE date(date) = date('{item.date}')"
                          # res = db.execute(text(""
                          # f"SELECT jsonb_object('{item.country}'::text, "
                          #     "(SELECT jsonb_build_object('LOC'::text, "
                          #         "ARRAY ( SELECT * FROM jsonb_object_keys("
                          #             "("
                          #                 "SELECT entities#> '{%s, %s}' FROM cons_data " % (item.country, 'LOC') +
                          #                 f"WHERE date(date) = date('{item.date}')"
                          #             ")"
                          #         ") as Location) "
                          #     ") as LocKeys "
                          #     "UNION "
                          #     "SELECT jsonb_build_object('PER'::text, "
                          #         "ARRAY ( SELECT * FROM jsonb_object_keys("
                          #             "("
                          #                 "SELECT entities#> '{%s, %s}' FROM cons_data " % (item.country, 'PER') +
                          #                 f"WHERE date(date) = date('{item.date}')"
                          #             ")"
                          #         ") as Person) "
                          #     ") as PerKeys))"
                          # "UNION "
                          # "SELECT jsonb_build_object('ORG'::text, "
                          #     "ARRAY ( SELECT * FROM jsonb_object_keys("
                          #         "("
                          #             "SELECT entities#> '{%s, %s}' FROM cons_data " % (item.country, 'ORG') +
                          #             f"WHERE date(date) = date('{item.date}')"
                          #         ")"
                          #     ") as Organization) "
                          # ")"
                          # )).scalar_one_or_none()
    )).scalars().all()[0]
    return res


def get_entity_titles(db: Session, entities: EntityTitles):
    ents = tuple(entities.entities)
    if len(entities.entities) == 1:
        ents = tuple(entities.entities*2)

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
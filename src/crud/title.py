from sqlalchemy.orm import Session
from sqlalchemy import text
from src.schema.country_schm import CountryDate, EntityTitles
import datetime

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
    )).scalar_one_or_none()
    return res

def get_entity_titles(db: Session, entities: EntityTitles):
    res = db.execute(text(
        "SELECT data FROM news_title "
        f"WHERE id IN {tuple(entities.entities)}"
            # "(SELECT jsonb_array_elements_text(entities #> '{%s, %s, %s}') " % (country, entity, entity_name) +
            # "FROM cons_data "
            # f"WHERE date(date) = date('{day}'))"
    )).scalars().all()
    return res

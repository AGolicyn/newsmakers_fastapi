import datetime

import pytest
from sqlalchemy.orm import Session
from src.crud.title import get_daily_results, get_entity_titles
from src.schema.country_schm import CountryDate, EntityTitles
from src.tests.data_garbage import RUSSIAN_CONS_DATA, TEST_TITLES

def test_get_country_entity(db: Session, insert_cons_data):
    required_data = {
        "country": "Russia",
        "date": datetime.date.today()
    }
    item = CountryDate(**required_data)

    db_data = get_daily_results(db=db, item=item)

    for ent_name in RUSSIAN_CONS_DATA['Russia']:
        assert RUSSIAN_CONS_DATA['Russia'][ent_name] == db_data[ent_name]

def test_get_titles_by_id(db: Session, insert_titles):
    ids = []
    for title_db in insert_titles:
        ids.append(title_db.id)
    entities = EntityTitles(**{'entities': ids})

    result = get_entity_titles(db=db, entities=entities)

    assert result == TEST_TITLES

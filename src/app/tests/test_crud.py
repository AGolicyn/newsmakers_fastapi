import pytest
import datetime
from collections.abc import AsyncGenerator
from ..crud.title import get_daily_results, get_entity_titles
from ..schema.country_schm import CountryDate, EntityTitles
from ..tests.data_garbage import RUSSIAN_CONS_DATA, TEST_TITLES
from app.db.session import NewsTitle, ConsolidatedData
from sqlalchemy import insert


@pytest.mark.asyncio
async def test_get_country_entity(session: AsyncGenerator):
    # fill db with some data
    db = await anext(session)
    await db.execute(insert(ConsolidatedData)
                     .values(entities=RUSSIAN_CONS_DATA)
                     .returning(ConsolidatedData))
    await db.commit()
    # try to get data
    required_data = {
        "country": "Russia",
        "date": datetime.date.today()
    }
    item = CountryDate(**required_data)
    db_data = await get_daily_results(session=db, item=item)
    # check if its equal to source
    for ent_name in RUSSIAN_CONS_DATA['Russia']:
        assert RUSSIAN_CONS_DATA['Russia'][ent_name] == db_data[ent_name]


@pytest.mark.asyncio
async def test_get_titles_by_id(session: AsyncGenerator):
    # fill db with new titles
    db = await anext(session)
    result = []
    for title in TEST_TITLES:
        new_title = await db.execute(insert(NewsTitle)
                                     .values(data=title)
                                     .returning(NewsTitle))
        result.append(new_title.scalar_one_or_none())
    await db.commit()
    ids = []
    for title_db in result:
        ids.append(title_db.id)
    entities = EntityTitles(**{'entities': ids})
    # Try to get id's of titles that returned by inserting
    result = await get_entity_titles(session=db, entities=entities)
    # Check if they equal to source
    for title in result:
        assert title in TEST_TITLES

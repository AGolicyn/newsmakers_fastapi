import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.tests.data_garbage import TEST_TITLES
from app.db.session import NewsTitle
from sqlalchemy import insert
from app.main import app


@pytest.mark.asyncio
async def test_post_entities(session: AsyncSession):
    result = []
    for title in TEST_TITLES:
        new_title = await session.execute(insert(NewsTitle)
                                          .values(data=title)
                                          .returning(NewsTitle))
        result.append(new_title.scalar_one_or_none())
    await session.commit()

    ids = []
    for title_db in result:
        ids.append(str(title_db.id))
    payload = {"entities": ids}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/titles", json=payload)

    assert response.status_code == 200
    data = response.json()

    result = set()
    test = set()

    for res in data:
        result.add(res['href'])
        result.add(res['title'])

    for res in TEST_TITLES:
        test.add(res['href'])
        test.add(res['title'])

    assert result == test

import pytest
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.tests.data_garbage import RUSSIAN_CONS_DATA
from app.db.session import ConsolidatedData
from sqlalchemy import insert
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_post_country(session: AsyncSession):
    # insert some data
    await session.execute(
        insert(ConsolidatedData)
        .values(entities=RUSSIAN_CONS_DATA)
        .returning(ConsolidatedData)
    )
    await session.commit()
    payload = {"country": "Russia", "date": str(datetime.date.today())}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/country", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data == RUSSIAN_CONS_DATA["Russia"]


@pytest.mark.asyncio
async def test_post_country_with_date_from_future(session: AsyncSession):
    await session.execute(
        insert(ConsolidatedData)
        .values(entities=RUSSIAN_CONS_DATA)
        .returning(ConsolidatedData)
    )
    await session.commit()

    payload = {"country": "Russia", "date": "2023-12-12"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/country", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "Invalid date from future"


@pytest.mark.asyncio
async def test_post_country_with_invalid_country(session: AsyncSession):
    await session.execute(
        insert(ConsolidatedData)
        .values(entities=RUSSIAN_CONS_DATA)
        .returning(ConsolidatedData)
    )
    await session.commit()

    payload = {"country": "Vacanda", "date": "2023-2-16"}

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/country", json=payload)

    assert response.status_code == 422

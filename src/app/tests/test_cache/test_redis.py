import pytest
from httpx import AsyncClient
from app.main import app, connection


@app.get("/ping/redis")
async def ping_redis():
    return {"redis_status": await connection.ping()}


@pytest.mark.asyncio
async def test_event_redis_on_startup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/ping/redis")
        assert response.status_code == 200
        assert response.json()["redis_status"]

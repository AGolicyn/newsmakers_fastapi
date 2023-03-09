import os
import asyncio
import pytest
from sqlalchemy.orm import declarative_base
from ..db.session import text, get_db
from sqlalchemy.ext.asyncio import async_sessionmaker, \
    create_async_engine, AsyncSession

from ..main import app

TEST_SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True, future=True)
Base = declarative_base()

TestSessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def override_get_db() -> AsyncSession:
    async with TestSessionFactory() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
async def session():
    async with TestSessionFactory() as session:
        try:
            yield session
        finally:
            await session.execute(text('DELETE FROM news_title'))
            await session.execute(text('DELETE FROM cons_data'))
            await session.commit()
            await session.close()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

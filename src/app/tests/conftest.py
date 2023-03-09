import os
import asyncio
import uuid
from datetime import datetime
from typing import Mapping

import pytest
from sqlalchemy import UUID, text, Date, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, \
    create_async_engine, AsyncSession

app = 0

TEST_SQLALCHEMY_DATABASE_URL = os.environ.get('ASYNC_TEST_DATABASE_URL')
engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True, future=True)
Base = declarative_base()
TestSessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    pass
    # async with AsyncSessionFactory() as session:
    #     yield session


class NewsTitle(Base):
    __tablename__ = 'news_title'

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True),
                                     primary_key=True,
                                     server_default=text('gen_random_uuid()'))
    data: Mapped[Mapping] = mapped_column(JSONB)


class ConsolidatedData(Base):
    __tablename__ = 'cons_data'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entities: Mapped[Mapping] = mapped_column(JSONB)
    date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())


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

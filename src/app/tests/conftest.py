import os

import pytest
from sqlalchemy import insert
from app.tests.data_garbage import RUSSIAN_CONS_DATA, TEST_TITLES
from fastapi.testclient import TestClient
from app.db.session import \
    Base, create_engine, sessionmaker, text, \
    ConsolidatedData, NewsTitle
from sqlalchemy.orm import Session
from app.main import app, get_db

TEST_SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.execute(text('DELETE FROM news_title'))
        test_db.execute(text('DELETE FROM cons_data'))
        test_db.commit()
        test_db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module')
def client():
    yield TestClient(app)


@pytest.fixture()
def db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.execute(text('DELETE FROM news_title'))
        test_db.execute(text('DELETE FROM cons_data'))
        test_db.commit()
        test_db.close()


@pytest.fixture()
def insert_cons_data(db: Session):
    """ROUTE FOR TEST PURPOSES ONLY"""
    new_res = db.execute(insert(ConsolidatedData)
                         .values(entities=RUSSIAN_CONS_DATA)
                         .returning(ConsolidatedData)
                         ).scalar_one_or_none()
    db.commit()
    yield new_res


@pytest.fixture()
def insert_titles(db: Session):
    result = []
    for title in TEST_TITLES:
        new_title = db.execute(insert(NewsTitle)
                               .values(data=title)
                               .returning(NewsTitle)
                               ).scalar_one_or_none()
        result.append(new_title)
    db.commit()
    return result

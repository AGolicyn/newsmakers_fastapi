import pytest
from sqlalchemy import insert
from src.db.session import *
from sqlalchemy.orm import Session
from src.tests.data_garbage import RUSSIAN_CONS_DATA, TEST_TITLES
from fastapi.testclient import TestClient
from src.main import *

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{TEST_DB_NAME}"
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
                         .values(entities=RUSSIAN_CONS_DATA,
                                 lang='RU')
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

# @pytest.fixture()
# def fill_db_with_data(insert_titles, insert_cons_data):
#     return insert_titles, insert_cons_data


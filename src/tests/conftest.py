import pytest
from sqlalchemy.sql import text
from src.db.session import *

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{TEST_DB_NAME}"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.execute(text('DELETE FROM news_title'))
        test_db.commit()
        test_db.close()

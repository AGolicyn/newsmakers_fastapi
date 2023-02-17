from sqlalchemy.orm import Session
from src.db.session import NewsTitle
from sqlalchemy import insert
from collections.abc import Mapping


def insert_title(db: Session, title: Mapping):
    new_title = db.execute(
        insert(NewsTitle)
        .values(data=title)
        .returning(NewsTitle)
    ).scalar_one_or_none()

    db.commit()
    return new_title

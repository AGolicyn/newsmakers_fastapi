import pytest
from sqlalchemy.orm import Session
from src.crud.title import insert_title

def test_insert_new(db: Session):
    title = {'url': 'https://aif.ru/',
             'time': '2023-02-11 00:41:24.592574',
             'lang': 'RU',
             'title': 'Число погибших при землетрясении в Турции превысило 20 тысяч'}

    new_title = insert_title(db, title)

    assert new_title.data['title'] == title['title']
    assert new_title.data['url'] == title['url']
    assert new_title.data['lang'] == title['lang']
    assert new_title.data['time'] == title['time']

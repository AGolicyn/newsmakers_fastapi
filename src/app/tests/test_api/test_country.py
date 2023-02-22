import datetime
from ..data_garbage import RUSSIAN_CONS_DATA
from fastapi.testclient import TestClient


def test_post_country(client: TestClient, insert_cons_data):
    payload = {"country": 'Russia',
               "date": str(datetime.date.today())}

    response = client.post(f'/country/', json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data == RUSSIAN_CONS_DATA['Russia']

def test_post_country_with_date_from_future(client: TestClient, insert_cons_data):
    payload = {"country": 'Russia',
               "date": '2023-12-12'}

    response = client.post(f'/country/', json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data['detail'] == "Invalid date from future"

def test_post_country_with_invalid_country(client: TestClient, insert_cons_data):
    payload = {"country": 'Vacanda',
               "date": '2023-2-16'}

    response = client.post(f'/country/', json=payload)

    assert response.status_code == 422


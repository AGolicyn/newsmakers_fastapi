from ..data_garbage import TEST_TITLES
from fastapi.testclient import TestClient


def test_post_entities(client: TestClient, insert_titles):
    ids = []
    for title_db in insert_titles:
        ids.append(str(title_db.id))
    payload = {"entities": ids}

    response = client.post("/titles", json=payload)

    assert response.status_code == 200
    data = response.json()

    result = set()
    test = set()

    for res in data:
        result.add(res['href'])
        result.add(res['title'])

    for res in TEST_TITLES:
        test.add(res['href'])
        test.add(res['title'])

    assert result == test

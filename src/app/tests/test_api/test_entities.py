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
    for result, test in zip(data, TEST_TITLES):
        assert result['href'] == test['href']
        assert result['title'] == test['title']

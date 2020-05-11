import json


@pytest.mark.e2e
def test_end_to_end(api):

    response = api.get("/pets", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    print(body)
    assert len(body) == 1

import pytest
import json


@pytest.mark.requiresdb
def test_end_to_end(e2e, empty_database):
    api = e2e

    # GET
    response = api.get("/peoples", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body) == 0

    # POST
    response = api.post("/peoples", json={"name": "testname"})
    assert response.status_code == 201

    # CHECK THAT POST WORKED
    response = api.get("/peoples", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body) == 1

    assert body[0]["id"] == 1
    assert body[0]["name"] == "testname"

    # CHECK THAT POST WORKED
    response = api.get("/peoples/1", json={})
    assert response.status_code == 200

    body = json.loads(response.data)

    assert len(body) == 2

    assert body["id"] == 1
    assert body["name"] == "testname"

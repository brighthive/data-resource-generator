import json
import pytest


@pytest.mark.unit
def test_all_routes_exist(VALID_DATA_DICTIONARY, e2e_app):
    api = e2e_app

    assert api.get("/peoples", json={}).status_code != 404
    assert api.post("/peoples", json={}).status_code != 404
    assert api.get("/peoples/1", json={}).status_code != 404
    assert api.put("/peoples/1", json={}).status_code != 404
    assert api.patch("/peoples/1", json={}).status_code != 404
    assert api.delete("/peoples/1", json={}).status_code != 404


@pytest.mark.unit
def test_end_to_end(VALID_DATA_DICTIONARY, e2e_app):
    api = e2e_app

    # GET
    response = api.get("/peoples", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body) == 0

    # POST
    response = api.post("/peoples", json={"name": "testname"})
    assert response.status_code == 200

    # CHECK THAT POST WORKED
    response = api.get("/peoples", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body) == 1

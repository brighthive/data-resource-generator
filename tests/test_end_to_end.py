import pytest
import json


@pytest.mark.requiresdb
def test_end_to_end(generated_e2e, empty_database):
    api = generated_e2e

    # GET
    response = api.get("/people", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body["people"]) == 0

    # POST
    response = api.post("/people", json={"name": "testname"})
    assert response.status_code == 201

    # CHECK THAT POST WORKED
    response = api.get("/people", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["people"] == [{"id": 1, "name": "testname"}]

    # GET 1
    response = api.get("/people/1", json={})
    assert response.status_code == 200

    body = json.loads(response.data)

    assert body["id"] == 1
    assert body["name"] == "testname"

    # DELETE is not implemented for reasons!
    response = api.delete("/people/1", json={})
    assert response.status_code == 405

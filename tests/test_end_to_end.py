import pytest
import json


@pytest.mark.requiresdb
def test_end_to_end_refactor_helper_delete_me(generated_e2e, empty_database):
    api = generated_e2e

    # GET
    response = api.get("/people", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body["people"]) == 0


@pytest.mark.xfail
@pytest.mark.requiresdb
def test_end_to_end(generated_e2e, empty_database):
    api = generated_e2e

    # GET
    response = api.get("/people", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body["people"]) == 0

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

    # GET 1
    response = api.get("/peoples/1", json={})
    assert response.status_code == 200

    body = json.loads(response.data)

    assert len(body) == 2

    assert body["id"] == 1
    assert body["name"] == "testname"

    # DELETE 1
    response = api.delete("/peoples/1", json={})
    assert response.status_code == 204

    # GET 1
    response = api.get("/peoples/1", json={})
    assert response.status_code == 404

import pytest
import json


# TODO these asserts should assert on the entire response
@pytest.mark.requiresdb
def test_end_to_end(
    generated_e2e, empty_database
):  # This e2e test is probably not needed.
    api = generated_e2e

    # Check for no data in DB
    response = api.get("/people", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert len(body["people"]) == 0

    # Create a person
    response = api.post("/people", json={"name": "testname"})
    assert response.status_code == 201

    # Check all the data in the DB
    response = api.get("/people", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["people"] == [{"id": 1, "name": "testname"}]

    # Check the specific data for the person we created
    response = api.get("/people/1", json={})
    assert response.status_code == 200

    body = json.loads(response.data)

    assert body["id"] == 1
    assert body["name"] == "testname"

    # DELETE is not implemented. For reasons!
    response = api.delete("/people/1", json={})
    assert response.status_code == 405

    # Modify the item
    response = api.put("/people/1", json={"name": "newname"})
    assert response.status_code == 201

    body = json.loads(response.data)
    assert body["id"] == 1

    # Patch the item
    response = api.patch("/people/1", json={"name": "patched"})
    assert response.status_code == 201

    body = json.loads(response.data)
    assert body["id"] == 1

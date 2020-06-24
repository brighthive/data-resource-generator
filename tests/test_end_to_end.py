import pytest
import json


@pytest.mark.requiresdb
def test_end_to_end(generated_e2e_client, empty_database):
    # This test should assert on the entire body of the responses
    api = generated_e2e_client

    # Check for no data in DB
    response = api.get("/people", json={})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == {"links": [], "people": []}

    # Create a person
    response = api.post("/people", json={"name": "testname"})
    body = json.loads(response.data)

    assert response.status_code == 201
    assert body == {"message": "Successfully added new resource.", "id": 1}

    # Check all the data in the DB
    response = api.get("/people", json={})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == {
        "people": [{"id": 1, "name": "testname"}],
        "links": [
            {"rel": "self", "href": "/people?offset=0&limit=20"},
            {"rel": "first", "href": "/people?offset=0&limit=20"},
            {"rel": "last", "href": "/people?offset=0&limit=20"},
        ],
    }

    # Check the specific data for the person we created
    response = api.get("/people/1", json={})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == {"name": "testname", "id": 1}

    # Modify the item
    response = api.put("/people/1", json={"name": "newname"})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == {"message": "Successfully updated resource.", "id": 1}

    # Patch the item
    response = api.patch("/people/1", json={"name": "patched"})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == {"message": "Successfully updated resource.", "id": 1}

    # DELETE is not implemented. For reasons!
    response = api.delete("/people/1", json={})
    body = json.loads(response.data)

    assert response.status_code == 405
    assert body == {"message": "Unimplemented unsecure delete"}

    # QUERY with valid data
    response = api.post("/people/query", json={"name": "patched"})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == {"results": [{"id": 1, "name": "patched"}]}

    # QUERY with wrong data
    response = api.post("/people/query", json={"name": "does not exist"})
    body = json.loads(response.data)

    assert response.status_code == 404
    assert body == {"message": "No matches found"}

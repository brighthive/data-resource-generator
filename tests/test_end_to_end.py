import pytest
import json


@pytest.mark.requiresdb
def test_end_to_end(
    generated_e2e, empty_database
):  # This e2e test is probably not needed.
    api = generated_e2e

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

    # DELETE is not implemented. For reasons!
    response = api.delete("/people/1", json={})
    body = json.loads(response.data)

    assert response.status_code == 405
    assert body == {"message": "Unimplemented unsecure delete"}

    # Modify the item
    response = api.put("/people/1", json={"name": "newname"})
    body = json.loads(response.data)

    assert response.status_code == 201
    assert body == {"message": "Successfully updated resource.", "id": 1}

    # Patch the item
    response = api.patch("/people/1", json={"name": "patched"})
    body = json.loads(response.data)

    assert response.status_code == 201
    assert body == {"message": "Successfully updated resource.", "id": 1}

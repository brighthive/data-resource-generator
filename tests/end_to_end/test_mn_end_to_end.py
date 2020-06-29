import pytest
import json


@pytest.mark.requiresdb
def test_many_to_many_end_to_end(generated_e2e_client, empty_database):
    # This test should assert on the entire body of the responses
    api = generated_e2e_client

    # Assosication list should be empty
    api.put("/people/1", json={"name": "person1"})
    api.put("/team/1", json={"name": "team1"})
    response = api.get("/people/1/team", json={})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == []

    # Generate
    response = api.put("/people/1/team", json={"data": [1]})
    body = json.loads(response.data)

    assert response.status_code == 200
    assert body == [1]

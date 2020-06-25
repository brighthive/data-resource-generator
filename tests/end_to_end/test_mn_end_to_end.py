import pytest
import json


@pytest.mark.requiresdb
def test_many_to_many_end_to_end(generated_e2e_client, empty_database):
    # This test should assert on the entire body of the responses
    # api = generated_e2e_client
    pass

    # Assosication list should be empty
    # response = api.get("/people/1/team", json={})
    # body = json.loads(response.data)

    # assert response.status_code == 200
    # assert body == {"team": []}

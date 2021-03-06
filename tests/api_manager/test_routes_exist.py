import pytest


@pytest.mark.unit
def test_all_routes_exist(generated_e2e_client):
    api = generated_e2e_client

    assert api.get("/people", json={}).status_code != 404
    assert api.post("/people", json={}).status_code != 404
    assert api.post("/people/query", json={}).status_code == 400  # Empty request body
    assert api.get("/people/1", json={}).status_code != 404
    assert api.put("/people/1", json={}).status_code != 404
    assert api.patch("/people/1", json={}).status_code != 404
    assert api.delete("/people/1", json={}).status_code != 404

    assert api.get("/people/0/team", json={}).status_code == 200
    assert api.get("/team/0/people", json={}).status_code == 200

    assert api.put("/people/0/team", json={}).status_code == 200
    assert api.put("/team/0/people", json={}).status_code == 200

    assert api.patch("/people/0/team", json={}).status_code == 200
    assert api.patch("/team/0/people", json={}).status_code == 200

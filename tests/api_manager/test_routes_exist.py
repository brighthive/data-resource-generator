import pytest


@pytest.mark.unit
def test_all_routes_exist(generated_e2e):
    api = generated_e2e

    assert api.get("/people", json={}).status_code != 404
    assert api.post("/people", json={}).status_code != 404
    assert api.get("/people/1", json={}).status_code != 404
    assert api.put("/people/1", json={}).status_code != 404
    assert api.patch("/people/1", json={}).status_code != 404
    assert api.delete("/people/1", json={}).status_code != 404

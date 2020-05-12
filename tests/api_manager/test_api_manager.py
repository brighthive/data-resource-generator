import json
import pytest


@pytest.mark.unit
def test_all_routes_exist(api):
    assert api.get("/peoples", json={}).status_code != 404
    assert api.post("/peoples", json={}).status_code != 404
    assert api.get("/peoples/1", json={}).status_code != 404
    assert api.put("/peoples/1", json={}).status_code != 404
    assert api.patch("/peoples/1", json={}).status_code != 404
    assert api.delete("/peoples/1", json={}).status_code != 404


# @pytest.mark.unit
# def test_get_all():
#     pass

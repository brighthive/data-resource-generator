import pytest
import json


# @pytest.mark.requiresdb
# def test_end_to_end(e2e):
#     MetadataSingleton._clear()
#     AutobaseSingleton._clear()
#     api = e2e

#     # GET
#     response = api.get("/peoples", json={})
#     assert response.status_code == 200

#     body = json.loads(response.data)
#     assert len(body) == 0

#     # POST
#     response = api.post("/peoples", json={"name": "testname"})
#     assert response.status_code == 200

#     # CHECK THAT POST WORKED
#     response = api.get("/peoples", json={})
#     assert response.status_code == 200

#     body = json.loads(response.data)
#     assert len(body) == 1

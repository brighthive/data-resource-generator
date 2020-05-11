import json
import pytest


@pytest.mark.e2e
def test_end_to_end(VALID_DATA_DICTIONARY, e2e_app):
    api = e2e_app

    # GET
    response = api.get("/peoples", json={})
    assert response.status_code == 200

    body = json.loads(response.data)
    print(body)
    assert len(body) == 0

    # # POST
    # response = api.post("/people", json={"name": "testname"})
    # assert response.status_code == 201

    # body = json.loads(response.data)
    # print(body)

    # # CHECK THAT POST WORKED
    # response = api.get("/people", json={})
    # assert response.status_code == 200

    # body = json.loads(response.data)
    # print(body)
    # assert len(body) == 1


# def test_get_response(VALID_DATA_DICTIONARY, api):
#     table_descriptors = VALID_DATA_DICTIONARY["data"]

#     response = api.put("/pets/1", json={
#         "animal_type": "cat",
#         "name": "Susie"
#     })
#     assert response.status_code == 201

#     response = api.get("/pets", json={})
#     assert response.status_code == 200

#     body = json.loads(response.data)
#     print(body)
#     assert len(body) == 1

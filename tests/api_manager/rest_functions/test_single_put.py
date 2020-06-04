from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
import pytest


@pytest.mark.requiresdb
def test_put(empty_database, valid_people_orm):
    # When nothing in DB - PUT will add the resource
    resource_handler = ResourceHandler()
    resource_name = "test"
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"name": "tester"}

    result = resource_handler.update_one(
        id=1,
        resource_name=resource_name,
        resource_orm=resource_orm,
        request=FakeFlaskRequest(),
        mode="PUT",
    )

    assert result == ({"id": 1, "message": "Successfully added new resource."}, 201)

    #  When something in DB - PUT changes the item
    class FakeFlaskRequestPut:
        json = {"name": "newtester"}

    result = resource_handler.update_one(
        id=1,
        resource_name=resource_name,
        resource_orm=resource_orm,
        request=FakeFlaskRequestPut(),
        mode="PUT",
    )

    assert result == ({"id": 1, "message": "Successfully updated resource."}, 201)

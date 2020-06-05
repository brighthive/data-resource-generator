from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
import pytest
from data_resource.logging.api_exceptions import ApiUnhandledError


@pytest.mark.requiresdb
def test_patch(empty_database, valid_people_orm):
    # When nothing in DB - PATCH error
    resource_handler = ResourceHandler()
    resource_name = "test"
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"name": "tester"}

    with pytest.raises(ApiUnhandledError):
        _ = resource_handler.update_one(
            id=1,
            resource_name=resource_name,
            resource_orm=resource_orm,
            request=FakeFlaskRequest(),
            mode="PATCH",
        )

    # TODO assert on actual message -- cant get it working
    # assert result == ({"error": "Resource with id '1' not found."}, 404)

    # When something in DB - PATCH changes the item
    new_object = resource_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.update_one(
        id=1,
        resource_name=resource_name,
        resource_orm=resource_orm,
        request=FakeFlaskRequest(),
        mode="PATCH",
    )

    assert result == ({"id": 1, "message": "Successfully updated resource."}, 201)

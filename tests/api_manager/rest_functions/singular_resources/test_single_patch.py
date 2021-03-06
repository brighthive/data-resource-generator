from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
import pytest
from data_resource.shared_utils.api_exceptions import ApiError


@pytest.mark.requiresdb
def test_patch_error_when_empty(empty_database, valid_people_orm):
    """Ideally we would be able to also assert on the error message that
    returns.

    # assert result == ({"error": "Resource with id '1' not found."},
    404)
    """
    # When nothing in DB - PATCH error
    resource_handler = ResourceHandler()

    class FakeFlaskRequest:
        json = {"name": "tester"}

    with pytest.raises(ApiError):
        _ = resource_handler.update_one(
            id=1,
            resource_name="test",
            resource_orm=valid_people_orm,
            request=FakeFlaskRequest(),
            mode="PATCH",
        )


@pytest.mark.requiresdb
def test_patch_works_when_item_exists(empty_database, valid_people_orm):
    # When something in DB - PATCH changes the item
    resource_handler = ResourceHandler()

    class FakeFlaskRequest:
        json = {"name": "tester"}

    new_object = valid_people_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.update_one(
        id=1,
        resource_name="test",
        resource_orm=valid_people_orm,
        request=FakeFlaskRequest(),
        mode="PATCH",
    )

    assert result == ({"id": 1, "message": "Successfully updated resource."}, 200)

from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
import pytest
from data_resource.logging.api_exceptions import ApiError


@pytest.mark.requiresdb
def test_post(empty_database, valid_people_orm):
    # When nothing in DB, adds to db.
    resource_handler = ResourceHandler()
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"name": "tester"}

    result = resource_handler.insert_one(
        resource_orm=resource_orm, request=FakeFlaskRequest()
    )

    assert result[0]["id"] == 1
    assert result[1] == 201


def test_post_missing_required_fields(empty_database, valid_orm_with_required_field):
    # Creating without required fields errors
    resource_handler = ResourceHandler()
    resource_orm = valid_orm_with_required_field

    class FakeFlaskRequest:
        json = {"optional": 1}

    with pytest.raises(ApiError):
        _ = resource_handler.insert_one(
            resource_orm=resource_orm, request=FakeFlaskRequest()
        )

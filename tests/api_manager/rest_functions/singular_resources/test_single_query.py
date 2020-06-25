from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
import pytest
from data_resource.logging.api_exceptions import ApiError
from data_resource.db.base import db_session


@pytest.mark.requiresdb
def test_query_works_with_correct_data(valid_people_orm):
    resource_handler = ResourceHandler()
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"name": "tester"}

    new_object = resource_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.query_one(
        resource_orm=resource_orm, request=FakeFlaskRequest()
    )

    assert result == ({"results": [{"id": 1, "name": "tester"}]}, 200)

    db_session.rollback()


@pytest.mark.requiresdb
def test_query_returns_none_when_given_incorrect_field_data(valid_people_orm):
    # When one item in DB - GET returns that item
    resource_handler = ResourceHandler()
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"name": "wrongname"}

    new_object = resource_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.query_one(
        resource_orm=resource_orm, request=FakeFlaskRequest()
    )

    assert result == ({"message": "No matches found"}, 404)

    db_session.rollback()


@pytest.mark.requiresdb
def test_query_errors_when_given_incorrect_field_data(valid_people_orm):
    # When one item in DB - GET returns that item
    resource_handler = ResourceHandler()
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"doesnotexist": "error"}

    new_object = resource_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    with pytest.raises(ApiError):
        resource_handler.query_one(
            resource_orm=resource_orm, request=FakeFlaskRequest()
        )

    # assert result == ({"errors": "Unknown or restricted field '{}' found."}, 400)

    db_session.rollback()


@pytest.mark.requiresdb
def test_query_empty_body_errors(valid_people_orm):
    resource_handler = ResourceHandler()
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {}

    with pytest.raises(ApiError):
        resource_handler.query_one(
            resource_orm=resource_orm, request=FakeFlaskRequest()
        )

    # assert result == ({"error": "No fields found in body."}, 400)

    db_session.rollback()

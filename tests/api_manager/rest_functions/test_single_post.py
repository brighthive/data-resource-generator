from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
import pytest
from data_resource.logging.api_exceptions import ApiError
from data_resource.db.base import db_session


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


def test_query_works_with_correct_data(empty_database, valid_people_orm):
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


def test_query_errors_when_given_field_that_does_not_exist(
    empty_database, valid_people_orm
):
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


def test_query_empty_body_errors(empty_database, valid_people_orm):
    resource_handler = ResourceHandler()
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {}

    with pytest.raises(ApiError):
        resource_handler.query_one(
            resource_orm=resource_orm, request=FakeFlaskRequest()
        )

    # assert result == ({"error": "No fields found in body."}, 400)

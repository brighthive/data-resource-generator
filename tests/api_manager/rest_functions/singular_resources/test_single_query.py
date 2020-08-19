from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
import pytest
from data_resource.shared_utils.api_exceptions import ApiError
from data_resource.db.base import db_session


@pytest.mark.requiresdb
def test_query_works_with_correct_data(valid_people_orm):
    resource_handler = ResourceHandler()

    class FakeFlaskRequest:
        json = {"name": "tester"}

    new_object = valid_people_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.query_one(
        resource_orm=valid_people_orm, request=FakeFlaskRequest()
    )

    assert result == ({"results": [{"id": 1, "name": "tester"}]}, 200)


@pytest.mark.requiresdb
def test_query_returns_none_when_given_incorrect_field_data(valid_people_orm):
    # When one item in DB - GET returns that item
    resource_handler = ResourceHandler()

    class FakeFlaskRequest:
        json = {"name": "wrongname"}

    new_object = valid_people_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.query_one(
        resource_orm=valid_people_orm, request=FakeFlaskRequest()
    )

    assert result == ({"message": "No matches found"}, 404)


@pytest.mark.requiresdb
def test_query_errors_when_given_incorrect_field_data(valid_people_orm):
    """Ideally we would be able to also assert on the error message that
    returns.

    # assert result == ({"error": "Resource with id '1' not found."},
    404)
    """
    # When one item in DB - GET returns that item
    resource_handler = ResourceHandler()

    class FakeFlaskRequest:
        json = {"doesnotexist": "error"}

    new_object = valid_people_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    with pytest.raises(ApiError):
        resource_handler.query_one(
            resource_orm=valid_people_orm, request=FakeFlaskRequest()
        )


@pytest.mark.requiresdb
def test_query_empty_body_errors(valid_people_orm):
    """Ideally we would be able to also assert on the error message that
    returns.

    # assert result == ({"error": "Resource with id '1' not found."},
    404)
    """
    resource_handler = ResourceHandler()

    class FakeFlaskRequest:
        json = {}

    with pytest.raises(ApiError):
        resource_handler.query_one(
            resource_orm=valid_people_orm, request=FakeFlaskRequest()
        )

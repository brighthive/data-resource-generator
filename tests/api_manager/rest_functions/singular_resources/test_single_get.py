from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import ApiError
import pytest


@pytest.mark.requiresdb
def test_get_all(empty_database, valid_people_orm):
    # When nothing in DB - GET returns empty list
    resource_handler = ResourceHandler()

    result = resource_handler.get_all(
        resource_name="test", resource_orm=valid_people_orm, offset=0, limit=10
    )

    assert result == ({"test": [], "links": []}, 200)

    # When one item in DB - GET returns an item
    new_object = valid_people_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.get_all(
        resource_name="test", resource_orm=valid_people_orm, offset=0, limit=10
    )

    assert result[0]["test"] == [{"id": 1, "name": "tester"}]
    assert result[1] == 200


@pytest.mark.requiresdb
def test_get_one_errors_when_it_does_not_exist(empty_database, valid_people_orm):
    """Ideally we would be able to also assert on the error message that
    returns.

    # assert result == ({"error": "Resource with id '1' not found."},
    404)
    """
    # When nothing in DB - GET returns error
    resource_handler = ResourceHandler()

    with pytest.raises(ApiError):
        _ = resource_handler.get_one(
            resource_name="test", resource_orm=valid_people_orm, id=1
        )


@pytest.mark.requiresdb
def test_get_one_works_when_item_exists(empty_database, valid_people_orm):
    # When one item in DB - GET returns that item
    resource_handler = ResourceHandler()

    new_object = valid_people_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.get_one(
        resource_name="test", resource_orm=valid_people_orm, id=1
    )

    assert result == ({"id": 1, "name": "tester"}, 200)

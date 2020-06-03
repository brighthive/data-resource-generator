from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from collections import OrderedDict


def test_get_all(empty_database, valid_people_orm):
    # When nothing in DB, returns nothing
    resource_handler = ResourceHandler()
    resource_name = "test"
    resource_orm = valid_people_orm

    result = resource_handler.get_all(
        resource_name=resource_name, resource_orm=resource_orm, offset=0, limit=10
    )

    assert len(result[0]["test"]) == 0

    # When one item in DB, returns an item
    new_object = resource_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.get_all(
        resource_name=resource_name, resource_orm=resource_orm, offset=0, limit=10
    )

    assert result[0]["test"] == [{"id": 1, "name": "tester"}]


def test_get_one(empty_database, valid_people_orm):
    # When nothing in DB, returns nothing
    resource_handler = ResourceHandler()
    resource_name = "test"
    resource_orm = valid_people_orm

    result = resource_handler.get_one(
        resource_name=resource_name, resource_orm=resource_orm, id=1
    )

    # should get nothing
    assert result == ({"error": f"Resource with id '1' not found."}, 404)

    # When one item in DB, returns that item
    new_object = resource_orm(name="tester")
    db_session.add(new_object)
    db_session.commit()

    result = resource_handler.get_one(
        resource_name=resource_name, resource_orm=resource_orm, id=1
    )

    # should get one item
    assert result == ({"id": 1, "name": "tester"}, 200)

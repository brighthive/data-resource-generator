from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from collections import OrderedDict


def test_get_all(empty_database, valid_people_orm):
    # When nothing in DB, returns nothing
    resource_handler = ResourceHandler()

    resource_name = "test"
    resource_orm = valid_people_orm

    result = resource_handler.get_all(
        name=resource_name, resource_orm=resource_orm, offset=0, limit=10
    )

    assert result == (OrderedDict([("test", []), ("links", [])]), 200)

    # When one item in DB, returns an item
    # db_session.query(valid_people_orm)

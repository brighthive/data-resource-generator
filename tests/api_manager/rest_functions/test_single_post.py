from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from collections import OrderedDict


def test_post(empty_database, valid_people_orm):
    # When nothing in DB, adds to db.
    resource_handler = ResourceHandler()
    resource_name = "test"
    resource_orm = valid_people_orm

    class FakeFlaskRequest:
        json = {"name": "tester"}

    result = resource_handler.insert_one(
        resource_name=resource_name,
        resource_orm=resource_orm,
        request=FakeFlaskRequest(),
    )

    assert result[0]["id"] == 1

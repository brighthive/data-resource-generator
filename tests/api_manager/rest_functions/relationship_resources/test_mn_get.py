from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import ApiError
import pytest


# @pytest.mark.requiresdb
# def test_get_one_errors_when_it_does_not_exist(empty_database, valid_people_orm):
#     # When nothing in DB - GET returns error
#     resource_handler = ResourceHandler()
#     resource_name = "test"
#     resource_orm = valid_people_orm

#     with pytest.raises(ApiError):
#         _ = resource_handler.get_one(
#             resource_name=resource_name, resource_orm=resource_orm, id=1
#         )

#     # assert result == ({"error": "Resource with id '1' not found."}, 404)  # TODO assert on message


@pytest.mark.requiresdb
def test_get_mn_one_works_when_item_exists(
    empty_database, valid_people_orm, valid_team_orm
):
    # When the resource exists, returns list of data
    resource_handler = ResourceHandler()
    people_orm = valid_people_orm
    team_orm = valid_team_orm

    person = people_orm(name="tester")
    team = team_orm(name="team")
    person.team_collection.append(team)

    db_session.add(person)
    db_session.add(team)
    db_session.commit()

    result = resource_handler.get_mn_one(
        id=1, parent_orm=valid_people_orm, child_orm=valid_team_orm
    )

    assert result == ([1], 200)

from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import ApiError
import pytest


@pytest.mark.requiresdb
def test_get_one_errors_when_it_does_not_exist(
    empty_database, valid_people_orm, valid_team_orm
):
    """Ideally we would be able to also assert on the error message that
    returns.

    # assert result == ({"error": "Resource with id '1' not found."},
    404)
    """
    resource_handler = ResourceHandler()

    with pytest.raises(ApiError):
        _ = resource_handler.get_mn_one(
            id=1, parent_orm=valid_people_orm, child_orm=valid_team_orm
        )


@pytest.mark.requiresdb
def test_get_mn_one_works_when_item_exists(
    empty_database, valid_people_orm, valid_team_orm
):
    resource_handler = ResourceHandler()

    person = valid_people_orm(name="tester")
    team = valid_team_orm(name="team")
    person.team_collection.append(team)

    db_session.add(person)
    db_session.add(team)
    db_session.commit()

    result = resource_handler.get_mn_one(
        id=1, parent_orm=valid_people_orm, child_orm=valid_team_orm
    )

    assert result == ([1], 200)

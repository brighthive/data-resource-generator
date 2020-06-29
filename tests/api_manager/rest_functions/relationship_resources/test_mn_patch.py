from data_resource.generator.api_manager.v1_0_0.resource_handler import ResourceHandler
from data_resource.db.base import db_session
from data_resource.logging.api_exceptions import ApiError
import pytest


@pytest.mark.requiresdb
def test_put_mn_one_works_when_items_exist(
    empty_database, valid_people_orm, valid_team_orm
):
    resource_handler = ResourceHandler()
    people_orm = valid_people_orm
    team_orm = valid_team_orm

    person = people_orm(name="tester")
    team1 = team_orm(name="team")
    team2 = team_orm(name="team2")
    person.team_collection.append(team1)

    db_session.add(person)
    db_session.add(team1)
    db_session.add(team2)
    db_session.commit()

    result = resource_handler.put_mn_one(
        id=1,
        body=[2],
        parent_orm=valid_people_orm,
        child_orm=valid_team_orm,
        patch=True,
    )

    assert result == ([1, 2], 200)


@pytest.mark.requiresdb
def test_put_errors_when_parent_does_not_exist(
    empty_database, valid_people_orm, valid_team_orm
):
    resource_handler = ResourceHandler()

    with pytest.raises(ApiError):
        _ = resource_handler.put_mn_one(
            id=1,
            body=[1],
            parent_orm=valid_people_orm,
            child_orm=valid_team_orm,
            patch=True,
        )

    # assert result == ({"error": "Resource with id '1' not found."}, 404)  # TODO assert on message


@pytest.mark.requiresdb
def test_put_errors_when_a_child_does_not_exist(
    empty_database, valid_people_orm, valid_team_orm
):
    resource_handler = ResourceHandler()
    people_orm = valid_people_orm
    team_orm = valid_team_orm

    person = people_orm(id=1, name="tester")
    team = team_orm(id=1, name="team")
    person.team_collection.append(team)

    db_session.add(person)
    db_session.add(team)
    db_session.commit()

    with pytest.raises(ApiError):
        _ = resource_handler.put_mn_one(
            id=1,
            body=[1, 2],
            parent_orm=valid_people_orm,
            child_orm=valid_team_orm,
            patch=True,
        )

    # assert result == ({"error": "Resource with id '1' not found."}, 404)  # TODO assert on message

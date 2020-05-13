import pytest
from data_resource.model_manager.model_manager import (
    create_all_tables_from_schemas,
    get_table_names_and_descriptors,
    model_manager_run,
    get_relationships_from_data_dict,
)
from data_resource.db.base import db_session
from sqlalchemy.orm.attributes import InstrumentedAttribute


@pytest.mark.unit  # Does this requiredb tho?
def test_model_manager_run_creates_all_required_orm(
    VALID_DATA_DICTIONARY, empty_database
):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    base = model_manager_run(table_descriptors)

    metadata = base.metadata

    assert "People" in metadata.tables
    assert "Team" in metadata.tables
    assert "Order" in metadata.tables
    assert "assoc_people_team" in metadata.tables

    # Assert that the auto mapped python classes exist
    assert base.classes.People
    people_orm = getattr(base.classes, "People")

    # Assert that the relational fields exist on the orm instance
    person1 = people_orm()
    assert person1.order_collection is not None
    assert person1.team_collection is not None

    assert base.classes.Team
    team_orm = getattr(base.classes, "Team")

    team1 = team_orm()
    assert team1.people_collection is not None

    assert base.classes.Order


# end to end test
@pytest.mark.requiresdb
def test_model_manager_run_can_add_data_with_orm(VALID_DATA_DICTIONARY, empty_database):
    # Arrange
    # create orm
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    base = model_manager_run(table_descriptors)

    # Act
    # add items to db via classes
    people_orm = getattr(base.classes, "People")
    order_orm = getattr(base.classes, "Order")
    team_orm = getattr(base.classes, "Team")

    person1 = people_orm(name="testperson")
    order1 = order_orm(items="testitems")
    team1 = team_orm(name="testteam")

    person1.order_collection.append(order1)
    person1.team_collection.append(team1)

    db_session.add(order1)
    db_session.add(team1)
    db_session.add(person1)

    db_session.commit()


@pytest.mark.requiresdb
def test_valid_descriptor_creates_databased(VALID_DATA_DICTIONARY, empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    metadata = create_all_tables_from_schemas(table_descriptors)

    assert len(metadata.tables) == 3


@pytest.mark.unit
def test_get_table_names_and_descriptors(VALID_DATA_DICTIONARY):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    table_names, descriptors = get_table_names_and_descriptors(table_descriptors)

    assert len(table_names) == 3
    assert table_names == ["People", "Team", "Order"]
    assert len(descriptors) == 3


@pytest.mark.unit
def test_get_relationships_from_data_dict(VALID_DATA_DICTIONARY):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    result = get_relationships_from_data_dict(table_descriptors)

    assert result == {
        # "oneToOne": [["People", "haveA", "Passport"],
        "oneToMany": [["People", "Order"]],
        "manyToMany": [["People", "Team"]],
    }

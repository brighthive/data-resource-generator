import pytest
from data_resource.generator.model_manager.model_manager import (
    create_all_tables_from_schemas,
    get_table_names_and_descriptors,
    create_models,
)
from data_resource.db.base import db_session


@pytest.mark.requiresdb
def test_creates_all_required_tables(generated_e2e_database_inspector):
    tables = generated_e2e_database_inspector.get_table_names()
    tables.sort()
    expected = ["required", "people", "order", "assoc_people_team", "team"]
    expected.sort()

    assert tables == expected
    # TODO assert on fields of tables


@pytest.mark.unit
def test_create_models_creates_all_required_orm(VALID_DATA_DICTIONARY, empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    base = create_models(table_descriptors)

    metadata = base.metadata

    assert "people" in metadata.tables
    assert "team" in metadata.tables
    assert "order" in metadata.tables
    assert "assoc_people_team" in metadata.tables

    # The auto mapped python classes exist
    assert base.classes.people
    people_orm = getattr(base.classes, "people")

    # The relational fields exist on the orm instance
    person1 = people_orm()
    # TODO: assert that the one to many relationship with Order is correct?
    assert person1.team_collection is not None

    assert base.classes.team
    team_orm = getattr(base.classes, "team")

    team1 = team_orm()
    assert team1.people_collection is not None

    assert base.classes.order


@pytest.mark.requiresdb
def test_create_models_can_add_data_with_orm(VALID_DATA_DICTIONARY, empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]
    base = create_models(table_descriptors)

    people_orm = getattr(base.classes, "people")
    team_orm = getattr(base.classes, "team")

    person1 = people_orm(name="testperson")
    team1 = team_orm(name="testteam")

    person1.team_collection.append(team1)

    db_session.add(team1)
    db_session.add(person1)

    db_session.commit()


@pytest.mark.requiresdb
def test_valid_descriptor_creates_base(VALID_DATA_DICTIONARY, empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    metadata = create_all_tables_from_schemas(table_descriptors)

    assert len(metadata.tables) == 4


@pytest.mark.unit
def test_get_table_names_and_descriptors(VALID_DATA_DICTIONARY):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    table_names, descriptors = get_table_names_and_descriptors(table_descriptors)

    assert len(table_names) == 4
    assert table_names == ["people", "team", "order", "required"]
    assert len(descriptors) == 4

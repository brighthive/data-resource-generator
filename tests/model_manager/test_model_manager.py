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
    expected = ["required", "people", "order", "people/team", "team"]
    expected.sort()

    assert tables == expected


@pytest.mark.unit
def test_create_models_creates_all_required_orm(valid_data_dictionary, empty_database):
    table_descriptors = valid_data_dictionary["data"]

    base = create_models(table_descriptors)

    metadata = base.metadata

    assert "people" in metadata.tables
    assert "team" in metadata.tables
    assert "order" in metadata.tables
    assert "people/team" in metadata.tables

    # The auto mapped python classes exist
    assert base.classes.people
    people_orm = getattr(base.classes, "people")

    # The relational fields exist on the orm instance
    person1 = people_orm()
    assert person1.team_collection is not None

    assert base.classes.team
    team_orm = getattr(base.classes, "team")

    team1 = team_orm()
    assert team1.people_collection is not None

    assert base.classes.order


@pytest.mark.requiresdb
def test_create_models_can_add_data_with_orm(valid_data_dictionary, empty_database):
    table_descriptors = valid_data_dictionary["data"]
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
def test_valid_descriptor_creates_base(valid_data_dictionary, empty_database):
    table_descriptors = valid_data_dictionary["data"]

    metadata = create_all_tables_from_schemas(table_descriptors)

    assert len(metadata.tables) == 4


@pytest.mark.unit
def test_get_table_names_and_descriptors(valid_data_dictionary):
    table_descriptors = valid_data_dictionary["data"]

    table_names, descriptors = get_table_names_and_descriptors(table_descriptors)

    assert len(table_names) == 4
    assert table_names == ["people", "team", "order", "required"]
    assert len(descriptors) == 4

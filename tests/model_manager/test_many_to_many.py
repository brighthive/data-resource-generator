import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.generator.model_manager.model_manager import (
    construct_many_to_many_assoc,
    automap_metadata,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute


@pytest.mark.unit
def test_create_mn_association_table():
    many_to_many_relationships = ["people", "team"]
    metadata = MetaData()
    People = Table(
        "people",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    Team = Table(
        "team",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )

    result = construct_many_to_many_assoc(metadata, many_to_many_relationships)

    # Returns the table name
    assert result == "people/team"
    assert "people/team" in metadata.tables
    # The field has the correct foreign key
    try:
        assert "{ForeignKey('people.id')}" == str(
            metadata.tables["people/team"].columns["people_id"].foreign_keys
        )
    except KeyError:
        pytest.fail("KeyError: Column was probably not found.")

    try:
        assert "{ForeignKey('team.id')}" == str(
            metadata.tables["people/team"].columns["team_id"].foreign_keys
        )
    except KeyError:
        pytest.fail("KeyError: Column was probably not found.")


@pytest.mark.unit
def test_automap_metadata_for_mn():
    metadata = MetaData()
    _ = Table(
        "people/team",
        metadata,
        Column("people_id", Integer, ForeignKey("people.id"), primary_key=True),
        Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
    )
    _ = Table(
        "people",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    _ = Table(
        "team",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )

    base = automap_metadata(metadata)

    people_orm = getattr(base.classes, "people")
    assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)

    team_orm = getattr(base.classes, "team")
    assert isinstance(getattr(team_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(team_orm, "name"), InstrumentedAttribute)

    person1 = people_orm()
    team1 = team_orm()
    person1.team_collection.append(team1)
    assert len(person1.team_collection) == 1
    assert len(team1.people_collection) == 1

    team1.people_collection.append(person1)
    assert len(person1.team_collection) == 2
    assert len(team1.people_collection) == 2

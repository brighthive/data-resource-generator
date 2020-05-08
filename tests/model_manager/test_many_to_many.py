import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.model_manager.model_manager import (
    construct_many_to_many_assoc,
    # add_foreign_keys_to_tables,
    automap_metadata,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from data_resource.db import AutobaseSingleton
from sqlalchemy.orm.attributes import InstrumentedAttribute


@pytest.mark.unit
def test_create_mn_association_table():
    many_to_many_relationships = ["People", "Team"]
    metadata = MetaData()
    People = Table(
        "People",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    Team = Table(
        "Team",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )

    result = construct_many_to_many_assoc(metadata, many_to_many_relationships)

    # Returns the table name
    assert result == "assoc_people_team"
    assert "assoc_people_team" in metadata.tables
    # The field has the correct foreign key
    try:
        assert "{ForeignKey('People.id')}" == str(
            metadata.tables["assoc_people_team"].columns["people"].foreign_keys
        )
    except KeyError:
        pytest.fail("KeyError: Column was probably not found.")

    try:
        assert "{ForeignKey('Team.id')}" == str(
            metadata.tables["assoc_people_team"].columns["team"].foreign_keys
        )
    except KeyError:
        pytest.fail("KeyError: Column was probably not found.")


@pytest.mark.unit
def test_automap_metadata_for_mn():
    metadata = MetaData()
    association = Table(
        f"assoc_people_team",
        metadata,
        Column("People", Integer, ForeignKey("People.id"), primary_key=True),
        Column("Team", Integer, ForeignKey("Team.id"), primary_key=True),
    )
    People = Table(
        "People",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    Team = Table(
        "Team",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    AutobaseSingleton._clear()

    automap_metadata(metadata)

    base = AutobaseSingleton.instance()

    people_orm = getattr(base.classes, "People")
    assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)

    team_orm = getattr(base.classes, "Team")
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

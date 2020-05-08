import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.model_manager.model_manager import (
    construct_many_to_many_assoc,
    add_foreign_keys_to_tables,
    automap_metadata,
    add_foreign_keys_to_many_to_one_parent,
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
def test_add_foreign_keys_to_mn_tables():
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
    assoc_table_name = "assoc_people_team"

    result = add_foreign_keys_to_tables(
        metadata, many_to_many_relationships, assoc_table_name
    )

    assert "mn_reference_team" in metadata.tables["People"].columns
    assert "mn_reference_people" in metadata.tables["Team"].columns

    assert "ForeignKey('assoc_people_team.team')" == str(
        list(metadata.tables["People"].columns["mn_reference_team"].foreign_keys)[0]
    )
    assert "ForeignKey('assoc_people_team.people')" == str(
        list(metadata.tables["Team"].columns["mn_reference_people"].foreign_keys)[0]
    )


@pytest.mark.unit
def test_automap_metadata_for_mn():
    metadata = MetaData()
    association = Table(
        f"assoc_people_team",
        metadata,
        Column("people", Integer, ForeignKey("People.id"), primary_key=True),
        Column("team", Integer, ForeignKey("Team.id"), primary_key=True),
    )
    People = Table(
        "People",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column(f"mn_reference_team", Integer, ForeignKey(f"assoc_people_team.team")),
    )
    Team = Table(
        "Team",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column(
            f"mn_reference_people", Integer, ForeignKey(f"assoc_people_team.people")
        ),
    )
    AutobaseSingleton._clear()

    automap_metadata(metadata)

    base = AutobaseSingleton.instance()

    people_orm = getattr(base.classes, "People")
    assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "mn_reference_team"), InstrumentedAttribute)

    team_orm = getattr(base.classes, "Team")
    assert isinstance(getattr(team_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(team_orm, "name"), InstrumentedAttribute)
    assert isinstance(getattr(team_orm, "mn_reference_people"), InstrumentedAttribute)

import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.model_manager.model_manager import (
    construct_many_to_many_assoc,
    add_foreign_keys_to_tables,
    automap_metadata_for_many_to_many,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from data_resource.db import AutobaseSingleton
from sqlalchemy.orm.attributes import InstrumentedAttribute


# https://github.com/brighthive/etl-goodwill/blob/master/tests/conftest.py#L103
@pytest.mark.unit
def test_create_one_many_to_many_assoc():
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
def test_add_foreign_keys_to_tables():
    many_to_many_relationships = ["People", "Team"]
    METADATA = MetaData()  # People, Teams as sqlalchemy METADATA
    People = Table(
        "People",
        METADATA,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    Team = Table(
        "Team",
        METADATA,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    assoc_table_name = "assoc_people_team"

    result = add_foreign_keys_to_tables(
        METADATA, many_to_many_relationships, assoc_table_name
    )

    assert "mn_reference_team" in METADATA.tables["People"].columns
    assert "mn_reference_people" in METADATA.tables["Team"].columns

    assert "ForeignKey('assoc_people_team.team')" == str(
        list(METADATA.tables["People"].columns["mn_reference_team"].foreign_keys)[0]
    )
    assert "ForeignKey('assoc_people_team.people')" == str(
        list(METADATA.tables["Team"].columns["mn_reference_people"].foreign_keys)[0]
    )


@pytest.mark.unit
def test_automap_metadata_for_many_to_many():
    METADATA = MetaData()  # People, Teams as sqlalchemy METADATA
    association = Table(
        f"assoc_people_team",
        METADATA,
        Column("people", Integer, ForeignKey("People.id"), primary_key=True),
        Column("team", Integer, ForeignKey("Team.id"), primary_key=True),
    )
    People = Table(
        "People",
        METADATA,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column(f"mn_reference_team", Integer, ForeignKey(f"assoc_people_team.team")),
    )
    Team = Table(
        "Team",
        METADATA,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column(
            f"mn_reference_people", Integer, ForeignKey(f"assoc_people_team.people")
        ),
    )
    AutobaseSingleton._clear()

    automap_metadata_for_many_to_many(METADATA)

    base = AutobaseSingleton.instance()

    people_orm = getattr(base.classes, "People")
    assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "mn_reference_team"), InstrumentedAttribute)

    team_orm = getattr(base.classes, "Team")
    assert isinstance(getattr(team_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(team_orm, "name"), InstrumentedAttribute)
    assert isinstance(getattr(team_orm, "mn_reference_people"), InstrumentedAttribute)


#     # assert new_metadata has association table
#     # assert new_metadata -> Peoples has peoples reference


# @pytest.mark.unit
# def test_aaaaaaa_add_assoc_ref_to_table():
#     METADATA = declarative_base(MetaData())
#     association = Table(
#         f"assoc_people_team",
#         METADATA.metadata,
#         Column("left", Integer, ForeignKey("People.id"), primary_key=True),
#         Column("right", Integer, ForeignKey("Team.id"), primary_key=True),
#     )
#     class People(METADATA):
#         __tablename__ = "People"
#         id = Column(Integer, primary_key=True)
#         name = Column(String(50))
#         teams = relationship(
#             "Team",
#             secondary=association,
#             backref="peoples"
#         )

#     class Team(METADATA):
#         __tablename__ = "Team"
#         id = Column(Integer, primary_key=True)
#         name = Column(String(50))

#     # print(METADATA.metadata.tables)
#     print([print(x) for x in People.__mapper__.relationships])
#     print(type(People))
#     print(dir(People))
#     print(type(METADATA.metadata.tables['People']))
#     assert 1 == 0


# @pytest.mark.unit
# def test_add_assoc_ref_to_table():
#     many_to_many_relationships = ["People", "Team"]
#     METADATA = declarative_base(MetaData()).metadata
#     People = Table(
#         "People",
#         METADATA,
#         Column("id", Integer, primary_key=True),
#         Column("name", String(50)),
#     )
#     Team = Table(
#         "Team",
#         METADATA,
#         Column("id", Integer, primary_key=True),
#         Column("name", String(50)),
#     )
#     association = Table(
#         f"assoc_people_team",
#         METADATA,
#         Column("left", Integer, ForeignKey("People.id"), primary_key=True),
#         Column("right", Integer, ForeignKey("Team.id"), primary_key=True),
#     )

#     add_assoc_ref_to_table(METADATA, many_to_many_relationships, association)

#     # lol = METADATA.tables['Person']
#     # print(dir(lol))
#     # import pdb; pdb.set_trace()

#     # assert new_metadata -> People has teams reference
#     # (Pdb) lol.columns
#     # <sqlalchemy.sql.base.ImmutableColumnCollection object at 0x104871f30>
#     # (Pdb) print(lol.columns)
#     # ['Person.person_id', 'Person.name']
#     assert "People.mn_reference_team" in METADATA.tables["People"].columns

#     # assert new_metadata -> Teams has peoples reference
#     # assert 'Person.mn_reference_team' in METADATA.tables['Team'].columns

#     # assert new_metadata -> People has teams reference
#     # (Pdb) lol.columns
#     # <sqlalchemy.sql.base.ImmutableColumnCollection object at 0x104871f30>
#     # (Pdb) print(lol.columns)
#     # ['Person.person_id', 'Person.name']
#     # assert 'Person.mn_reference_team' in METADATA.tables['Person'].columns

#     # assert new_metadata -> Teams has peoples reference
#     # assert 'Person.mn_reference_team' in METADATA.tables['Team'].columns

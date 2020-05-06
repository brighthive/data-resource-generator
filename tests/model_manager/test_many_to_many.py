import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String
from data_resource.model_manager.model_manager import construct_many_to_many_assoc


# https://github.com/brighthive/etl-goodwill/blob/master/tests/conftest.py#L103
@pytest.mark.unit
def test_create_one_many_to_many_assoc():
    many_to_many_relationships = ["People", "Team"]
    METADATA = MetaData()  # People, Teams as sqlalchemy METADATA
    People = Table(
        "People",
        METADATA,
        Column("person_id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    Team = Table(
        "Team",
        METADATA,
        Column("team_id", Integer, primary_key=True),
        Column("name", String(50)),
    )

    construct_many_to_many_assoc(METADATA, many_to_many_relationships)

    # lol = METADATA.tables['Person']
    # print(dir(lol))
    # import pdb; pdb.set_trace()

    # assert new_metadata has association table
    assert "assoc_people_team" in METADATA.tables

    # assert new_metadata -> People has teams reference
    # (Pdb) lol.columns
    # <sqlalchemy.sql.base.ImmutableColumnCollection object at 0x104871f30>
    # (Pdb) print(lol.columns)
    # ['Person.person_id', 'Person.name']
    # assert 'Person.mn_reference_team' in METADATA.tables['Person'].columns

    # assert new_metadata -> Teams has peoples reference
    # assert 'Person.mn_reference_team' in METADATA.tables['Team'].columns


# @pytest.mark.unit
# def test_create_many_to_many():
#     relationships = VALID_DATA_DICTIONARY["data"]["relationships"] # only People, People
#     metadata_dict = {}
#     new_metadata = MetaData({}) # People, People as sqlalchemy metadata

#     construct_many_to_many(new_metadata, relationships)

#     # assert new_metadata has association table
#     # assert new_metadata -> Peoples has peoples reference

import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.model_manager.model_manager import (
    construct_many_to_many_assoc,
    add_foreign_keys_to_tables,
    automap_metadata_for_many_to_many,
    add_foreign_keys_to_many_to_one_parent,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from data_resource.db import AutobaseSingleton
from sqlalchemy.orm.attributes import InstrumentedAttribute


@pytest.mark.unit
def test_add_foreign_keys_to_tables():
    many_to_one_relationships = ["People", "Order"]
    metadata = MetaData()
    People = Table(
        "People",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    Order = Table(
        "Order",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )

    result = add_foreign_keys_to_many_to_one_parent(metadata, many_to_one_relationships)

    assert "m1_reference_order" in metadata.tables["People"].columns
    # assert "1m_reference_people" in metadata.tables["Order"].columns

    assert "ForeignKey('Order.id')" == str(
        list(metadata.tables["People"].columns["m1_reference_order"].foreign_keys)[0]
    )


# @pytest.mark.unit
# def test_create_many_to_one():
#     # add foreign key to parent referencing child
#     metadata = MetaData()
#     People = Table(
#         "People",
#         metadata,
#         Column("id", Integer, primary_key=True),
#         Column("name", String(50)),
#         Column(f"mn_reference_team", Integer, ForeignKey(f"assoc_people_team.team")),
#     )
#     Team = Table(
#         "Team",
#         metadata,
#         Column("id", Integer, primary_key=True),
#         Column("name", String(50)),
#         Column(
#             f"mn_reference_people", Integer, ForeignKey(f"assoc_people_team.people")
#         ),
#     )
#     AutobaseSingleton._clear()

#     automap_metadata_for_many_to_many(metadata)

#     base = AutobaseSingleton.instance()

#     people_orm = getattr(base.classes, "People")
#     assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
#     assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)
#     assert isinstance(getattr(people_orm, "mn_reference_team"), InstrumentedAttribute)

#     team_orm = getattr(base.classes, "Team")
#     assert isinstance(getattr(team_orm, "id"), InstrumentedAttribute)
#     assert isinstance(getattr(team_orm, "name"), InstrumentedAttribute)
#     assert isinstance(getattr(team_orm, "mn_reference_people"), InstrumentedAttribute)

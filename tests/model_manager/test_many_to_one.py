import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.model_manager.model_manager import (
    construct_many_to_many_assoc,
    add_foreign_keys_to_tables,
    add_foreign_keys_to_many_to_one_parent,
    automap_metadata,
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


@pytest.mark.unit
def test_automap_metadata_for_m1():
    metadata = MetaData()
    People = Table(
        "People",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column(f"m1_reference_order", Integer, ForeignKey(f"Order.id")),
    )
    Order = Table(
        "Order",
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
    assert isinstance(getattr(people_orm, "m1_reference_order"), InstrumentedAttribute)

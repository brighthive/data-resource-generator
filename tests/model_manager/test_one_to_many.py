import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.model_manager.model_manager import (
    construct_many_to_many_assoc,
    add_foreign_keys_to_one_to_many_parent,
    automap_metadata,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from data_resource.db import AutobaseSingleton, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.collections import InstrumentedList


@pytest.mark.unit
def test_add_foreign_keys_to_tables():
    one_to_many_relationships = ["People", "Order"]
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

    _ = add_foreign_keys_to_one_to_many_parent(metadata, one_to_many_relationships)

    assert "om_reference_people" in metadata.tables["Order"].columns
    assert "ForeignKey('People.id')" == str(
        list(metadata.tables["Order"].columns["om_reference_people"].foreign_keys)[0]
    )


@pytest.mark.unit
def test_automap_metadata_for_m1():
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
        Column(f"om_reference_people", Integer, ForeignKey(f"People.id")),
    )
    AutobaseSingleton._clear()

    automap_metadata(metadata)

    base = AutobaseSingleton.instance()

    people_orm = getattr(base.classes, "People")
    assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)

    person = people_orm()
    assert isinstance(getattr(person, "order_collection"), InstrumentedList)

    order_orm = getattr(base.classes, "Order")
    assert isinstance(getattr(order_orm, "om_reference_people"), InstrumentedAttribute)

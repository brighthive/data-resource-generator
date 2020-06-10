import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from data_resource.generator.model_manager.model_manager import (
    add_foreign_keys_to_one_to_many_parent,
    automap_metadata,
)
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.collections import InstrumentedList


@pytest.mark.unit
def test_add_foreign_keys_to_tables():
    one_to_many_relationships = ["People", "Order"]
    metadata = MetaData()
    _ = Table(
        "people",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    _ = Table(
        "order",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )

    _ = add_foreign_keys_to_one_to_many_parent(metadata, one_to_many_relationships)

    assert "om_reference_people" in metadata.tables["order"].columns
    assert "ForeignKey('people.id')" == str(
        list(metadata.tables["order"].columns["om_reference_people"].foreign_keys)[0]
    )


@pytest.mark.unit
def test_automap_metadata_for_m1():
    metadata = MetaData()
    _ = Table(
        "people",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
    )
    _ = Table(
        "order",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("om_reference_people", Integer, ForeignKey("people.id")),
    )

    base = automap_metadata(metadata)

    people_orm = getattr(base.classes, "people")
    assert isinstance(getattr(people_orm, "id"), InstrumentedAttribute)
    assert isinstance(getattr(people_orm, "name"), InstrumentedAttribute)

    person = people_orm()
    assert isinstance(getattr(person, "order_collection"), InstrumentedList)

    order_orm = getattr(base.classes, "order")
    assert isinstance(getattr(order_orm, "om_reference_people"), InstrumentedAttribute)

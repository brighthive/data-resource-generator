from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine, MetadataSingleton, AutobaseSingleton
from sqlalchemy.orm import relationship, mapper
from sqlalchemy.ext.automap import automap_base
import itertools


# main
def main(data_catalog: list) -> None:
    """Given the data portion of a data catalog, Produce all the SQLAlchemy
    ORM."""
    # Create base items
    create_all_tables_from_schemas(data_catalog)

    metadata = MetadataSingleton.instance()

    relationships = get_relationships_from_data_dict(data_catalog)

    for relationship in relationships["oneToMany"]:
        add_foreign_keys_to_one_to_many_parent(metadata, relationship)

    for relationship in relationships["manyToMany"]:
        assoc_table_name = construct_many_to_many_assoc(metadata, relationship)

    # Create ORM relationships
    automap_metadata(metadata)


# base
def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
    """Generates the tables from frictionless table schema (without
    relations)."""
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)

    try:
        storage = Storage(engine=engine)

        metadata = storage._Storage__metadata

        storage.create(table_names, descriptors)

        MetadataSingleton.set_metadata(metadata)

    except ValidationError as e:
        print(e.errors)
        raise


# base
def automap_metadata(metadata):
    """Given a complete set of tables with foreign keys setup correctly, this
    will produce python classes that contain methods that handle the magic of
    relationships."""
    base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    base.prepare()

    AutobaseSingleton.set_autobase(base)

    # For testing
    if base.metadata.is_bound() is True:
        base.metadata.drop_all()
        base.metadata.create_all()


# util
def get_table_names_and_descriptors(data_dict: list) -> (list, list):
    """Given a data catalog, this simply gets the table names and frictionless
    table schemas."""
    data_dict = data_dict["dataDictionary"]

    table_names = []
    descriptors = []

    table_names = [schema["name"] for schema in data_dict]
    descriptors = [schema["tableSchema"] for schema in data_dict]

    return table_names, descriptors


# util
def get_relationships_from_data_dict(data_dict: dict) -> list:
    """Given a data catalog, this simply gets the SQL relationships."""
    relationships = data_dict["relationships"]

    return relationships


# mn
def construct_many_to_many_assoc(metadata: "MetaData", relationship: list) -> str:
    """Given a single many to many relationship, creates the required
    association table."""

    relationship.sort()

    association = Table(
        f"assoc_{relationship[0].lower()}_{relationship[1].lower()}",
        metadata,
        Column(
            f"{relationship[0].lower()}",
            Integer,
            ForeignKey(f"{relationship[0]}.id"),
            primary_key=True,
        ),
        Column(
            f"{relationship[1].lower()}",
            Integer,
            ForeignKey(f"{relationship[1]}.id"),
            primary_key=True,
        ),
    )

    return str(association)


# one to many
def add_foreign_keys_to_one_to_many_parent(metadata, one_to_many_relationships):
    """Given a single one to many relationship, extends the existing child
    table with the correct foreign key information."""
    parent_table = one_to_many_relationships[0]
    child_table = one_to_many_relationships[1]

    Table(
        f"{child_table}",
        metadata,
        Column(
            f"om_reference_{parent_table.lower()}",
            Integer,
            ForeignKey(f"{parent_table}.id"),  # lookup their primary key? TODO?
        ),
        extend_existing=True,
    )

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
    # Many to one
    for relationship in relationships["oneToMany"]:
        add_foreign_keys_to_one_to_many_parent(metadata, relationship)

    # Many to many
    for relationship in relationships["manyToMany"]:
        # Create assoc table
        assoc_table_name = construct_many_to_many_assoc(metadata, relationship)

        # Create foreign keys
        add_foreign_keys_to_tables(metadata, relationship, assoc_table_name)

    # Create automapping relationships
    automap_metadata(metadata)


# base
def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
    """Generates the tables from frictionless table schema (without
    relations)."""
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)

    try:
        storage = Storage(engine=engine)

        # Hijack the metadata / create_all()
        metadata = storage._Storage__metadata
        # Base = declarative_base(metadata)

        # TODO: get table names from data dict
        storage.create(table_names, descriptors)

        MetadataSingleton.set_metadata(metadata)  # Sqlalchemy metadata

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

    # create many to many association table
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


# mn
def add_foreign_keys_to_tables(METADATA, mn_relationship, assoc_table_name):
    """Given a single many to many relationship, extends the existing tables
    with the correct foreign key information."""
    # Get tables
    mn_relationship.sort()
    table = METADATA.tables[mn_relationship[0]]
    other_table = METADATA.tables[mn_relationship[1]]

    # Extend / add foreign key
    Table(
        f"{mn_relationship[0]}",
        METADATA,
        Column(
            f"mn_reference_{mn_relationship[1].lower()}",
            Integer,
            ForeignKey(f"{assoc_table_name}.{mn_relationship[1].lower()}"),
        ),
        extend_existing=True,
    )

    Table(
        f"{mn_relationship[1]}",
        METADATA,
        Column(
            f"mn_reference_{mn_relationship[0].lower()}",
            Integer,
            ForeignKey(f"{assoc_table_name}.{mn_relationship[0].lower()}"),
        ),
        extend_existing=True,
    )


# one to many
def add_foreign_keys_to_one_to_many_parent(metadata, one_to_many_relationships):
    """Given a single many to one relationship, extends the existing parent
    table with the correct foreign key information."""
    # Get tables
    parent_table = one_to_many_relationships[0]
    child_table = one_to_many_relationships[1]

    # Extend / add foreign key
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

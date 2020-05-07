from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine, MetadataSingleton
from sqlalchemy.orm import relationship, mapper

# from sqlalchemy.ext.declarative import declarative_base


# Need end to end?
def main(table_schemas: list) -> None:
    # Create base items
    create_all_tables_from_schemas(table_schemas)

    metadata = MetadataSingleton.instance()
    # Many to many
    # Create assoc table
    construct_many_to_many_assoc(metadata)

    # Create foreign keys
    add_foreign_keys_to_tables

    # Create automapping relationships


def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)

    try:
        storage = Storage(engine=engine)

        # Hijack the metadata / create_all()
        metadata = storage._Storage__metadata
        # Base = declarative_base(metadata)

        storage.create(table_names, descriptors)

        MetadataSingleton.set_metadata(metadata)  # Sqlalchemy metadata

    except ValidationError as e:
        print(e.errors)
        raise


def get_table_names_and_descriptors(table_schemas: list) -> (list, list):
    table_names = []
    descriptors = []

    table_names = [schema["name"] for schema in table_schemas]
    descriptors = [schema["tableSchema"] for schema in table_schemas]

    return table_names, descriptors


def construct_many_to_many_assoc(metadata: "MetaData", relationship: list) -> str:
    """Given a single many to many, creates it."""

    # create many to many association table
    relationship.sort()

    association = Table(
        f"assoc_{relationship[0].lower()}_{relationship[1].lower()}",
        metadata,
        Column("left", Integer, ForeignKey(f"{relationship[0]}.id"), primary_key=True),
        Column("right", Integer, ForeignKey(f"{relationship[1]}.id"), primary_key=True),
    )

    return str(association)


def add_foreign_keys_to_tables(METADATA, many_to_many_relationships, assoc_table_name):
    # Get tables
    many_to_many_relationships.sort()
    table = METADATA.tables[many_to_many_relationships[0]]
    other_table = METADATA.tables[many_to_many_relationships[1]]

    # Extend / add foreign key
    Table(
        f"{many_to_many_relationships[0]}",
        METADATA,
        Column(
            f"mn_reference_{many_to_many_relationships[1].lower()}",
            Integer,
            ForeignKey(f"{assoc_table_name}.{many_to_many_relationships[1].lower()}"),
        ),
        extend_existing=True,
    )

    Table(
        f"{many_to_many_relationships[1]}",
        METADATA,
        Column(
            f"mn_reference_{many_to_many_relationships[0].lower()}",
            Integer,
            ForeignKey(f"{assoc_table_name}.{many_to_many_relationships[0].lower()}"),
        ),
        extend_existing=True,
    )

from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine, MetadataSingleton, AutobaseSingleton
from sqlalchemy.orm import relationship, mapper
from sqlalchemy.ext.automap import automap_base


def main(table_schemas: list) -> None:
    # Create base items
    create_all_tables_from_schemas(table_schemas)

    metadata = MetadataSingleton.instance()

    # Many to many
    relationships = [["People", "Team"]]
    for relationship in relationships:
        # Create assoc table
        assoc_table_name = construct_many_to_many_assoc(metadata, relationship)

        # Create foreign keys
        add_foreign_keys_to_tables(metadata, relationship, assoc_table_name)

    # Create automapping relationships
    automap_metadata_for_many_to_many(metadata)


def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
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


def get_table_names_and_descriptors(data_dict: list) -> (list, list):
    data_dict = data_dict["dataDictionary"]

    table_names = []
    descriptors = []

    table_names = [schema["name"] for schema in data_dict]
    descriptors = [schema["tableSchema"] for schema in data_dict]

    return table_names, descriptors


def construct_many_to_many_assoc(metadata: "MetaData", relationship: list) -> str:
    """Given a single many to many, creates it."""

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


def add_foreign_keys_to_tables(METADATA, mn_relationship, assoc_table_name):
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


def automap_metadata_for_many_to_many(metadata):
    base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    base.prepare()

    AutobaseSingleton.set_autobase(base)


def get_relationships_from_data_dict(data_dict: dict) -> list:
    relationships = data_dict["relationships"]

    return relationships

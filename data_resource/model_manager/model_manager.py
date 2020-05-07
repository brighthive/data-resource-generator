from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine, MetadataSingleton
from sqlalchemy.orm import relationship, mapper

# from sqlalchemy.ext.declarative import declarative_base


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


def construct_many_to_many_assoc(metadata: "MetaData", relationship: list) -> None:
    """Given a single many to many, creates it."""

    # create many to many association table
    relationship.sort()

    association = Table(
        f"assoc_{relationship[0].lower()}_{relationship[1].lower()}",
        metadata,
        Column("left", Integer, ForeignKey(f"{relationship[0]}.id"), primary_key=True),
        Column("right", Integer, ForeignKey(f"{relationship[1]}.id"), primary_key=True),
    )

    # assign reference item to both tables
    # tbl1 = get_table(relationship[0])
    # tbl2 = get_table(relationship[1])

    # add_mn_reference_column(tbl1, association)
    # add_mn_reference_column(tbl2, association)

    return association


# def add_assoc_ref_to_table(METADATA, many_to_many_relationships, association_table):
#     # get table


def add_foreign_keys_to_tables(METADATA, many_to_many_relationships):
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
            ForeignKey(f"{many_to_many_relationships[1]}.id"),
        ),
        extend_existing=True,
    )

    Table(
        f"{many_to_many_relationships[1]}",
        METADATA,
        Column(
            f"mn_reference_{many_to_many_relationships[0].lower()}",
            Integer,
            ForeignKey(f"{many_to_many_relationships[0]}.id"),
        ),
        extend_existing=True,
    )

from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine, MetadataSingleton


def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)

    try:
        storage = Storage(engine=engine)
        storage.create(table_names, descriptors)

        metadata = storage._Storage__metadata

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


def construct_many_to_many(metadata: "MetaData", relationship: list) -> None:
    """Given a single many to many, creates it."""

    # create many to many association table
    relationship.sort()

    association = Table(
        f"assoc_{relationship[0].lower()}_{relationship[1].lower()}",
        metadata,
        Column("left", Integer, ForeignKey("node.id"), primary_key=True),
        Column("right", Integer, ForeignKey("node.id"), primary_key=True),
    )

    # assign reference item to both tables
    # tbl1 = get_table(relationship[0])
    # tbl2 = get_table(relationship[1])

    # add_mn_reference_column(tbl1, association)
    # add_mn_reference_column(tbl2, association)

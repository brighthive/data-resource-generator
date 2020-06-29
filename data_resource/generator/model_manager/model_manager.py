from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine
from sqlalchemy.ext.automap import automap_base
from data_resource.logging import LogFactory


logger = LogFactory.get_console_logger("generator:model-manager")


# main
def create_models(data_catalog: list) -> None:
    """Given the data portion of a data catalog, Produce all the SQLAlchemy
    ORM."""
    # Create base items
    metadata = create_all_tables_from_schemas(data_catalog)

    relationships = get_relationships_from_data_dict(data_catalog)

    for relationship in relationships["oneToMany"]:
        add_foreign_keys_to_one_to_many_parent(metadata, relationship)

    for relationship in relationships["manyToMany"]:
        _ = construct_many_to_many_assoc(metadata, relationship)

    metadata.create_all()

    # Create ORM relationships
    base = automap_metadata(metadata)
    return base


# base
def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
    """Generates the tables from frictionless table schema (without
    relations)."""
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)

    try:
        storage = Storage(engine=engine)

        metadata = storage._Storage__metadata

        # Override create all so tableschema-sql won't handle table creation
        original_create_all = metadata.create_all
        metadata.create_all = lambda: None

        storage.create(table_names, descriptors)

        metadata.create_all = original_create_all  # Restore

        return metadata

    except ValidationError:
        logger.exception("Validation errors on tableschema.")
        raise


# base
def automap_metadata(metadata) -> "Base":
    """Given a complete set of tables with foreign keys setup correctly, this
    will produce python classes that contain methods that handle the magic of
    relationships."""
    base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    base.prepare()

    # For testing
    if base.metadata.is_bound() is True:
        base.metadata.drop_all()
        base.metadata.create_all()

    return base


# util
def get_table_names_and_descriptors(data_dict: list) -> (list, list):
    """Given a data catalog, this simply gets the table names and frictionless
    table schemas."""
    data_dict = data_dict["dataDictionary"]

    table_names = []
    descriptors = []

    table_names = [schema["name"].lower() for schema in data_dict]
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
            ForeignKey(f"{relationship[0].lower()}.id"),
            primary_key=True,
        ),
        Column(
            f"{relationship[1].lower()}",
            Integer,
            ForeignKey(f"{relationship[1].lower()}.id"),
            primary_key=True,
        ),
    )

    return str(association)


# one to many
def add_foreign_keys_to_one_to_many_parent(metadata, one_to_many_relationships):
    """Given a single one to many relationship, extends the existing child
    table with the correct foreign key information."""
    parent_table = one_to_many_relationships[0].lower()
    child_table = one_to_many_relationships[1].lower()

    Table(
        f"{child_table}",
        metadata,
        Column(
            f"om_reference_{parent_table}",
            Integer,
            ForeignKey(f"{parent_table}.id"),  # lookup their primary key? TODO?
        ),
        extend_existing=True,
    )

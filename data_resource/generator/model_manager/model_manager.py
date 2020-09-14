import os
from sqlalchemy import exc
from tableschema_sql import Storage
from tableschema.exceptions import ValidationError
from sqlalchemy import Table, Integer, ForeignKey, Column
from data_resource.db import engine
from sqlalchemy.ext.automap import automap_base
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.crypto import AES_GCM_Engine, AWS_AES_Engine
from sqlalchemy import MetaData

logger = LogFactory.get_console_logger("generator:model-manager")

# main
def create_models(data_resource_schema: list, touch_database: bool = True) -> None:
    """Given the data portion of a data catalog, Produce all the SQLAlchemy
    ORM."""
    # Create base items
    metadata = create_all_tables_from_schemas(data_resource_schema)

    try:
        relationships = data_resource_schema["relationships"]
        for relationship in relationships["manyToMany"]:
            _ = construct_many_to_many_assoc(metadata, relationship)
    except KeyError:
        pass

    if touch_database:
        try:
            metadata.create_all()
        except exc.SQLAlchemyError:
            logger.exception("Failed to create all models in database.")

    # Create ORM relationships
    base = automap_metadata(metadata)
    return base


# base
def create_all_tables_from_schemas(table_schemas: list) -> "Metadata":
    """Generates the tables from frictionless table schema (without
    relations)."""
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)
    encrypted_defintions = get_encryption_definitions(table_schemas)

    try:
        storage = Storage(engine=engine)

        # Override the reflection and capture reference to orm
        metadata = storage._Storage__metadata = MetaData(
            bind=engine
        )  # , schema="generated"

        # Override create all so tableschema-sql won't handle table creation
        original_create_all = metadata.create_all
        metadata.create_all = lambda: None

        storage.create(
            table_names, descriptors, encrypted_definitions=encrypted_defintions
        )

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

    return base


# util
def get_encryption_definitions(table_schemas: list) -> (list, list):
    """Given a table schemas, this simply create the encryption defintion for
    the ORM."""
    data_dict = table_schemas["dataDictionary"]
    encryption_definitions = dict()

    # goes through schema and create encryption defintion
    for schema in data_dict:
        table_encryption_definitions = {}
        table_name = schema["name"].lower()

        # goes through table schema and sets engine and key
        try:
            for en_schema_key in schema["encryptionSchema"].keys():
                en_schema = schema["encryptionSchema"][en_schema_key]

                if en_schema["type"] == "AES_256_GCM":
                    table_encryption_definitions[en_schema_key] = {
                        "key": os.getenv(en_schema["key"], en_schema["key"]),
                        "engine": AES_GCM_Engine,
                    }
                    encryption_definitions[table_name] = table_encryption_definitions

                if en_schema["type"] == "AWS_AES_Engine":
                    table_encryption_definitions[en_schema_key] = {
                        "key": os.getenv(en_schema["key"], en_schema["key"]),
                        "engine": AWS_AES_Engine,
                    }
                    encryption_definitions[table_name] = table_encryption_definitions

        except KeyError:
            pass  # if encryption schema does exist fail gracefully

    return encryption_definitions


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


# mn
def construct_many_to_many_assoc(metadata: "MetaData", relationship: list) -> str:
    """Given a single many to many relationship, creates the required
    association table."""

    relationship.sort()

    association = Table(
        f"{relationship[0].lower()}/{relationship[1].lower()}",
        metadata,
        Column(
            f"{relationship[0].lower()}_id",
            Integer,
            ForeignKey(f"{relationship[0].lower()}.id"),
            primary_key=True,
        ),
        Column(
            f"{relationship[1].lower()}_id",
            Integer,
            ForeignKey(f"{relationship[1].lower()}.id"),
            primary_key=True,
        ),
    )

    return str(association)

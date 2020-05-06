from tableschema_sql import Storage
import tableschema
from data_resource.db import engine


def create_all_tables_from_schemas(table_schemas):
    table_names, descriptors = get_table_names_and_descriptors(table_schemas)

    try:
        storage = Storage(engine=engine)
        storage.create(table_names, descriptors)
    except tableschema.exceptions.ValidationError as e:
        print(e.errors)
        raise


def get_table_names_and_descriptors(table_schemas: list) -> (list, list):
    table_names = []
    descriptors = []

    table_names = [schema["name"] for schema in table_schemas]
    descriptors = [schema["tableSchema"] for schema in table_schemas]

    return table_names, descriptors

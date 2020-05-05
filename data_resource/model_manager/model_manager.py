from tableschema_sql import Storage
import tableschema
from data_resource.db import engine


def convert_table_schema_to_database(table_name, descriptor):
    try:
        storage = Storage(engine=engine)
        storage.create(table_name, descriptor)
    except tableschema.exceptions.ValidationError as e:
        print(e.errors)
        raise

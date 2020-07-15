"""Storage Manager."""

import os
import json


class StorageManager:
    """Storage Manager Class."""

    def __init__(self, config):
        self.config = config
        self.SCHEMA_STORAGE_TYPE = self.config.SCHEMA_STORAGE_TYPE
        self.SCHEMA_STORAGE_TYPE = self.config.SCHEMA_STORAGE_TYPE
        print(self.SCHEMA_STORAGE_TYPE)

    def data_resource_schema_exists(self):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            return os.path.exists("./static/data_resource_schema.json")

    def get_data_resource_schema_data(self):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            with open("./static/data_resource_schema.json") as json_file:
                data_resource_schema = json.load(json_file)
                return data_resource_schema

    def save_data_resource_schema_data(self, data_resource_schema):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            if not os.getenv("APP_ENV", "TEST") == "TEST":
                with open("./static/data_resource_schema.json", "w") as outfile:
                    json.dump(data_resource_schema, outfile)

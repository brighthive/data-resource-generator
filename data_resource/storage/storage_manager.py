"""Storage Manager."""

import os
import json

from data_resource.storage.aws_s3 import (
    aws_s3_upload_file,
    aws_s3_object_exists,
    aws_s3_get_data,
    aws_s3_put_data,
)


class StorageManager:
    """Storage Manager Class."""

    def __init__(self, config):
        self.config = config
        self.SCHEMA_STORAGE_TYPE = self.config.SCHEMA_STORAGE_TYPE
        self.DEFAULT_LOCAL_SCHEMA_PATH = self.config.DEFAULT_LOCAL_SCHEMA_PATH
        self.AWS_S3_STORAGE_BUCKET_NAME = self.config.AWS_S3_STORAGE_BUCKET_NAME
        self.AWS_S3_STORAGE_OBJECT_NAME = self.config.AWS_S3_STORAGE_OBJECT_NAME

    # will check if schema exists
    def data_resource_schema_exists(self):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            return os.path.exists(self.DEFAULT_LOCAL_SCHEMA_PATH)
        elif self.SCHEMA_STORAGE_TYPE == "S3":
            return aws_s3_object_exists(
                self.AWS_S3_STORAGE_BUCKET_NAME, self.AWS_S3_STORAGE_OBJECT_NAME
            )

    # will use env to grab schema
    def get_data_resource_schema_data(self):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            with open(self.DEFAULT_LOCAL_SCHEMA_PATH) as json_file:
                data_resource_schema = json.load(json_file)
                return data_resource_schema
        elif self.SCHEMA_STORAGE_TYPE == "S3":
            data_resource_schema = aws_s3_get_data(
                self.AWS_S3_STORAGE_BUCKET_NAME, self.AWS_S3_STORAGE_OBJECT_NAME
            )
            return json.loads(data_resource_schema)

    # will use schema data
    def save_data_resource_schema_data(self, data_resource_schema):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            if not os.getenv("APP_ENV", "TEST") == "TEST":
                with open(self.DEFAULT_LOCAL_SCHEMA_PATH, "w") as outfile:
                    json.dump(data_resource_schema, outfile)
        elif self.SCHEMA_STORAGE_TYPE == "S3":
            if not aws_s3_object_exists(
                self.AWS_S3_STORAGE_BUCKET_NAME, self.AWS_S3_STORAGE_OBJECT_NAME
            ):
                aws_s3_put_data(
                    data_resource_schema,
                    self.AWS_S3_STORAGE_BUCKET_NAME,
                    self.AWS_S3_STORAGE_OBJECT_NAME,
                )

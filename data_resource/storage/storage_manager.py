"""Storage Manager."""

import os
import json

from data_resource.config import ConfigurationFactory
from data_resource.storage.aws_s3 import S3Manager


class StorageManager:
    """Storage Manager Class."""

    def __init__(self, config):
        self.config = config
        self.SCHEMA_STORAGE_TYPE = self.config.SCHEMA_STORAGE_TYPE
        self.DEFAULT_LOCAL_GENERATION_PAYLOAD_PATH = (
            self.config.DEFAULT_LOCAL_GENERATION_PAYLOAD_PATH
        )

        if self.SCHEMA_STORAGE_TYPE == "S3":
            self.s3manager = S3Manager(config)
            self.AWS_S3_STORAGE_BUCKET_NAME = self.config.AWS_S3_STORAGE_BUCKET_NAME
            self.AWS_S3_STORAGE_OBJECT_NAME = self.config.AWS_S3_STORAGE_OBJECT_NAME

    # will check if schema exists
    def data_resource_generation_payload_exists(self):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            return os.path.exists(self.DEFAULT_LOCAL_GENERATION_PAYLOAD_PATH)
        elif self.SCHEMA_STORAGE_TYPE == "S3":
            return self.s3manager.aws_s3_object_exists(
                self.AWS_S3_STORAGE_BUCKET_NAME, self.AWS_S3_STORAGE_OBJECT_NAME
            )

    # will use env to grab schema
    def get_data_resource_generation_payload_data(self):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            with open(self.DEFAULT_LOCAL_GENERATION_PAYLOAD_PATH) as json_file:
                data_resource_generation_payload = json.load(json_file)
                return data_resource_generation_payload
        elif self.SCHEMA_STORAGE_TYPE == "S3":
            data_resource_generation_payload = self.s3manager.aws_s3_get_data(
                self.AWS_S3_STORAGE_BUCKET_NAME, self.AWS_S3_STORAGE_OBJECT_NAME
            )
            return json.loads(data_resource_generation_payload)

    # will use schema data
    def save_data_resource_generation_payload_data(
        self, data_resource_generation_payload
    ):
        if self.SCHEMA_STORAGE_TYPE == "LOCAL":
            if not os.getenv("APP_ENV", "TEST") == "TEST":
                with open(self.DEFAULT_LOCAL_GENERATION_PAYLOAD_PATH, "w") as outfile:
                    json.dump(data_resource_generation_payload, outfile)
        elif (
            self.SCHEMA_STORAGE_TYPE == "S3"
            and not self.s3manager.aws_s3_object_exists(
                self.AWS_S3_STORAGE_BUCKET_NAME, self.AWS_S3_STORAGE_OBJECT_NAME
            )
        ):
            self.s3manager.aws_s3_put_data(
                data_resource_generation_payload,
                self.AWS_S3_STORAGE_BUCKET_NAME,
                self.AWS_S3_STORAGE_OBJECT_NAME,
            )

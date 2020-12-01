import os
import logging
import boto3
import json
from botocore.exceptions import ClientError


class S3Manager:
    """S3Manager Manager Class."""

    def __init__(self, config):
        self.config = config
        self.aws_iam_role = self.config.AWS_IAM_ROLE
        self.aws_access_key_id = self.config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = self.config.AWS_SECRET_ACCESS_KEY
        self.region_name = self.config.AWS_S3_REGION

        if (
            self.aws_access_key_id == None
            or self.aws_secret_access_key == None
            or self.region_name == None
        ):
            if self.aws_iam_role == False:
                raise RuntimeError("Invalid AWS S3 Configuration")

    def _required_env_check(self):
        if self.config.ENV != "PRODUCTION":
            raise RuntimeError(
                "AWS S3 storage manager are not allowed in testing environment"
            )

    def get_s3_client(self):
        self._required_env_check()
        if self.aws_iam_role:
            return boto3.client(
                "s3",
                region_name=self.region_name,
            )
        else:
            return boto3.client(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name,
            )

    def get_s3_resource(self):
        self._required_env_check()
        if self.aws_iam_role:
            return boto3.resource(
                "s3",
                region_name=self.region_name,
            )
        else:
            return boto3.resource(
                "s3",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name,
            )

    # will upload a file from volume to a s3 bucket
    def aws_s3_upload_file(self, file_name, bucket, object_name=None):
        if object_name is None:
            object_name = file_name

        try:
            s3_client = self.get_s3_client()
            _ = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    # will check if s3 object exist in s3
    def aws_s3_object_exists(self, bucket, object_name):
        try:
            s3_resource = self.get_s3_resource()
            s3_resource.Object(bucket, object_name).load()
        except ClientError as e:
            logging.error(e)
            return int(e.response["Error"]["Code"]) != 404
        return True

    # will get uploaded dat from s3 bucket object (utf-8 decoding)
    def aws_s3_get_data(self, bucket, object_name):
        try:
            s3 = self.get_s3_resource()
            obj = s3.Object(bucket, object_name)
            data = obj.get()["Body"].read().decode("UTF-8")
            return data
        except ClientError as e:
            logging.error(e)
            return None

    # will upload json_data to a bucket with object name (utf-8 encoding)
    def aws_s3_put_data(self, json_data, bucket, object_name):
        try:
            s3 = self.get_s3_resource()
            obj = s3.Object(bucket, object_name)
            obj.put(Body=(bytes(json.dumps(json_data).encode("UTF-8"))))
            return True
        except ClientError as e:
            logging.error(e)
            return False

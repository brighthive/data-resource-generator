"""Storage Manager Unit Test."""

import pytest
from data_resource.config import ConfigurationFactory
from data_resource.storage.aws_s3 import S3Manager
from data_resource.storage.storage_manager import StorageManager
from unittest.mock import patch

# Mock S3Manager class for unit tests
class MockS3Manager:
    def aws_s3_object_exists_true(self, bucket, object_name):
        return True

    def aws_s3_object_exists_false(self, bucket, object_name):
        return False

    def aws_s3_get_data(self, bucket, object_name):
        return "{}"

    def aws_s3_put_data(self, json_data, bucket, object_name):
        self.json_data = json_data
        self.bucket = bucket
        self.object_name = object_name


in_mock_s3_manager = MockS3Manager()


def base_s3_test_configs():
    configs = ConfigurationFactory.get_config("TEST")

    # set random value to pass check.
    configs.SCHEMA_STORAGE_TYPE = "S3"
    configs.AWS_S3_REGION = "test-region"
    configs.AWS_ACCESS_KEY_ID = "test-key"
    configs.AWS_SECRET_ACCESS_KEY = "test-access"
    configs.AWS_S3_STORAGE_BUCKET_NAME = "my-bucket-name"
    configs.AWS_S3_STORAGE_OBJECT_NAME = "my-object-name"

    return configs


@pytest.mark.unit
def test_load_configuration_from_env_for_storage_manager():
    """Ensure that a configuration object can be pulled from the environment
    and has the default configs."""

    configuration = ConfigurationFactory.get_config("TEST")
    assert hasattr(configuration, "SCHEMA_STORAGE_TYPE")
    assert hasattr(configuration, "DEFAULT_LOCAL_SCHEMA_PATH")
    assert hasattr(configuration, "AWS_S3_REGION")
    assert hasattr(configuration, "AWS_S3_STORAGE_BUCKET_NAME")
    assert hasattr(configuration, "AWS_S3_STORAGE_OBJECT_NAME")


@pytest.mark.unit
def test_s3_manager_config_check_failure():
    """Ensure that the s3 manager will throw a RuntimeError when AWS configs
    not found."""
    with pytest.raises(RuntimeError):
        s3manager = S3Manager(ConfigurationFactory.get_config("TEST"))


@pytest.mark.unit
def test_s3_manager_config_check_success():
    """Ensure that the s3 manager will init correctly with required envs:

    - AWS_S3_REGION
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    """
    configs = base_s3_test_configs()

    s3manager = S3Manager(configs)


@pytest.mark.unit
def test_s3_manager_config_required_env_check():
    """Ensures the AWS SDK is not triggered when running in the testing
    environment."""
    configs = base_s3_test_configs()

    s3manager = S3Manager(configs)

    with pytest.raises(RuntimeError):
        s3manager.get_s3_client()


@pytest.mark.unit
@patch(
    "data_resource.storage.aws_s3.S3Manager.aws_s3_object_exists",
    new=in_mock_s3_manager.aws_s3_object_exists_true,
)
def test_s3_store_manager_data_resource_schema_exists():
    """Ensuring the S3 Manager is receiving the correct parameters
    "aws_s3_object_exists" for the AWS API (boto3)"""
    configs = base_s3_test_configs()

    manager = StorageManager(configs)

    assert manager.data_resource_schema_exists() == True


@pytest.mark.unit
@patch(
    "data_resource.storage.aws_s3.S3Manager.aws_s3_get_data",
    new=in_mock_s3_manager.aws_s3_get_data,
)
def test_s3_store_manager_data_resource_get_schema():
    """Ensuring the S3 Manager is receiving the correct parameters
    "aws_s3_get_data" for the AWS API (boto3)"""
    configs = base_s3_test_configs()

    manager = StorageManager(configs)

    assert manager.get_data_resource_schema_data() == {}


@pytest.mark.unit
@patch(
    "data_resource.storage.aws_s3.S3Manager.aws_s3_put_data",
    new=in_mock_s3_manager.aws_s3_put_data,
)
@patch(
    "data_resource.storage.aws_s3.S3Manager.aws_s3_object_exists",
    new=in_mock_s3_manager.aws_s3_object_exists_false,
)
def test_s3_store_manager_data_resource_get_schema():
    """Ensuring the S3 Manager is receiving the correct parameters
    "aws_s3_put_data" for the AWS API (boto3)"""
    configs = base_s3_test_configs()
    manager = StorageManager(configs)
    manager.save_data_resource_schema_data("{}")

    assert in_mock_s3_manager.json_data == "{}"
    assert in_mock_s3_manager.bucket == configs.AWS_S3_STORAGE_BUCKET_NAME
    assert in_mock_s3_manager.object_name == configs.AWS_S3_STORAGE_OBJECT_NAME

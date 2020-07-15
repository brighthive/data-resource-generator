"""Application Configuration Objects and Factory."""

import os
from brighthive_authlib import AuthLibConfiguration, OAuth2ProviderFactory
import json
import boto3
from botocore.exceptions import ClientError
from data_resource.shared_utils.log_factory import LogFactory

logger = LogFactory.get_console_logger("configuration-factory")


class InvalidConfigurationError(Exception):
    """Invalid configuration factory object exception."""

    pass


class Config:
    """Base configuration class.

    Class Attributes:     RELATIVE_PATH (str): The configuration file's
    relative location on disk.     ABSOLUTE_PATH (str): The
    configuration file's absolute path on disk.     ROOT_PATH (str): The
    application's root location on disk derived from subtracting this
    file's         relative path from it's absolute path. SLEEP_INTERVAL
    (int): The number of seconds to sleep between checking the status of
    data resources.
    """

    dirname, _ = os.path.split(os.path.abspath(__file__))
    STATIC_FOLDER = os.path.abspath(os.path.join(dirname, "../../"))
    SKIP_AUTH_CHECK = False

    RELATIVE_PATH = os.path.dirname(os.path.relpath(__file__))
    ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    ROOT_PATH = ABSOLUTE_PATH.split(RELATIVE_PATH)[0]
    MIGRATION_HOME = os.getenv("MIGRATION_HOME", os.path.join(ROOT_PATH, "migrations"))
    DATA_RESOURCE_SLEEP_INTERVAL = os.getenv("DATA_RESOURCE_SLEEP_INTERVAL", 60)
    DATA_MODEL_SLEEP_INTERVAL = os.getenv("DATA_MODEL_SLEEP_INTERVAL", 30)

    # Database Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    POSTGRES_USER = "test_user"
    POSTGRES_PASSWORD = "test_password"  # nosec
    POSTGRES_DATABASE = "data_resource_dev"
    POSTGRES_HOSTNAME = "localhost"
    POSTGRES_PORT = 5432
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE,
    )

    # OAuth 2.0 Settings
    OAUTH2_PROVIDER = os.getenv("OAUTH2_PROVIDER", "AUTH0")
    OAUTH2_URL = os.getenv("OAUTH2_URL", "https://brighthive-test.auth0.com")
    OAUTH2_JWKS_URL = "{}/.well-known/jwks.json".format(OAUTH2_URL)
    OAUTH2_AUDIENCE = os.getenv("OAUTH2_AUDIENCE", "http://localhost:8000")
    OAUTH2_ALGORITHMS = ["RS256"]

    # Secret Manager
    SECRET_MANAGER = None

    # AWS S3 Schema Store
    SCHEMA_STORAGE_TYPE = "LOCAL"

    @staticmethod
    def get_oauth2_provider():
        """Retrieve the OAuth 2.0 Provider.

        Return:
            object: The OAuth 2.0 Provider.
        """
        auth_config = AuthLibConfiguration(
            provider=Config.OAUTH2_PROVIDER,
            base_url=Config.OAUTH2_URL,
            jwks_url=Config.OAUTH2_JWKS_URL,
            algorithms=Config.OAUTH2_ALGORITHMS,
            audience=Config.OAUTH2_AUDIENCE,
        )
        oauth2_provider = OAuth2ProviderFactory.get_provider(
            Config.OAUTH2_PROVIDER, auth_config
        )
        return oauth2_provider


class TestConfig(Config):
    """Unit testing configuration class."""

    def __init__(self):
        super().__init__()

    # os.environ["FLASK_ENV"] = "testing"
    # POSTGRES_PORT = 5433
    # CONTAINER_NAME = "postgres-test"
    # IMAGE_NAME = "postgres"
    # IMAGE_VERSION = "11.1"
    # POSTGRES_DATABASE = "data_resource_test"
    # SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    #     Config.POSTGRES_USER,
    #     Config.POSTGRES_PASSWORD,
    #     Config.POSTGRES_HOSTNAME,
    #     POSTGRES_PORT,
    #     POSTGRES_DATABASE,
    # )

    SKIP_AUTH_CHECK = True
    POSTGRES_USER = "test_user"
    POSTGRES_PASSWORD = "test_password"  # nosec
    POSTGRES_DATABASE = "data_resource_dev"
    POSTGRES_HOSTNAME = "localhost"
    POSTGRES_PORT = 5433
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE,
    )


# class IntegrationTestConfig(Config):
#     """Integration testing configuration class."""

#     def __init__(self):
#         super().__init__()


# class DevelopmentConfig(Config):
#     """Development configuration class."""

#     def __init__(self):
#         super().__init__()


# class SandboxConfig(Config):
#     """Sandbox deployment configuration class."""

#     def __init__(self):
#         super().__init__()

#     # Database Settings
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     PROPAGATE_EXCEPTIONS = True
#     POSTGRES_USER = os.getenv("POSTGRES_USER")
#     POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
#     POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
#     POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME", "localhost")
#     POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
#     SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
#         POSTGRES_USER,
#         POSTGRES_PASSWORD,
#         POSTGRES_HOSTNAME,
#         POSTGRES_PORT,
#         POSTGRES_DATABASE,
#     )


class ProductionConfig(Config):
    """Production deployment configuration class."""

    def __init__(self):
        super().__init__()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    is_aws_sm = bool(int(os.getenv("AWS_SM_ENABLED", "0")))
    if is_aws_sm:
        secret_name = os.getenv("AWS_SM_NAME", "")
        region_name = os.getenv("AWS_SM_REGION", "us-west-1")

        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                raise e
            elif e.response["Error"]["Code"] == "InternalServiceErrorException":
                raise e
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                raise e
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                raise e
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise e
        else:
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
                creds = json.loads(secret)
                POSTGRES_USER = creds["username"]
                POSTGRES_PASSWORD = creds["password"]
                POSTGRES_DATABASE = os.getenv("AWS_SM_DBNAME")
                POSTGRES_HOSTNAME = creds["host"]
                POSTGRES_PORT = int(creds["port"])
                SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
                    POSTGRES_USER,
                    POSTGRES_PASSWORD,
                    POSTGRES_HOSTNAME,
                    POSTGRES_PORT,
                    POSTGRES_DATABASE,
                )
    else:
        POSTGRES_USER = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
        POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME", "localhost")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            POSTGRES_USER,
            POSTGRES_PASSWORD,
            POSTGRES_HOSTNAME,
            POSTGRES_PORT,
            POSTGRES_DATABASE,
        )


class ConfigurationFactory:
    """A factory for handling configuration object creation."""

    @staticmethod
    def get_config(config_type: str):
        """Retrieve a configuration factory based on a configuration type.

        Args:
            config_type (str): Configuration type to return factory for.
                Possible values are `TEST`, `DEVELOPMENT`, `SANDBOX`, `INTEGRATION`, and `PRODUCTION`.
                Default value is `TEST`

        Returns:
            Config: A configuration object of the specified type.

        Raises:
            InvalidConfigurationError
        """

        config_type = config_type.upper()
        if config_type == "TEST":
            return TestConfig()
        elif config_type == "PRODUCTION":
            return ProductionConfig()
        else:
            raise InvalidConfigurationError(
                "Invalid configuration type `{}` specified.".format(config_type)
            )

    @staticmethod
    def from_env():
        """Retrieve a configuration object from the environment.

        Notes:
            Provides a configuration object based on the `APP_ENV` environment variable. Defaults to the development
            environment if the variable is left unset.

        Returns:
            Config: Configuration object based on the configuration environment supplied in the `APP_ENV` environment variable.
        """
        app_env = os.getenv("APP_ENV", "TEST")
        return ConfigurationFactory.get_config(app_env)

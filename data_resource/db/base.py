"""Database and ORM Fixtures."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Works with docker-compose -- hostname and hostport

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

engine = create_engine(SQLALCHEMY_DATABASE_URI)

# from sqlalchemy.schema import CreateSchema
# if not engine.dialect.has_schema(engine, "managed"):
#     engine.execute(CreateSchema("managed"))

Session = sessionmaker(bind=engine)


class MetadataSingleton:
    __slots__ = (
        []
    )  # prevents additional attributes from being added to instances and same-named attributes from shadowing the class's attributes
    metadata = None

    @classmethod
    def instance(cls):
        if cls.metadata is None:
            raise RuntimeError("No MetaData reference was found stored in the .")
        return cls.metadata

    @classmethod
    def set_metadata(cls, metadata):
        cls.metadata = metadata

    @classmethod
    def _clear(cls):
        """This method is for use in unit tests."""
        cls.metadata = None

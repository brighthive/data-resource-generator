"""Database and ORM Fixtures."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from data_resource.config import ConfigurationFactory
from data_resource.shared_utils.log_factory import LogFactory

logger = LogFactory.get_console_logger("database")


data_resource_config = ConfigurationFactory.from_env()

logger.info(f"Connecting to DB at '{data_resource_config.SQLALCHEMY_DATABASE_URI}'...")

engine = create_engine(
    data_resource_config.SQLALCHEMY_DATABASE_URI, pool_size=40, max_overflow=0
)  # TODO tests max the pool size out for some reason

from sqlalchemy.schema import CreateSchema  # noqa: E402

if not engine.dialect.has_schema(engine, "admin"):
    engine.execute(CreateSchema("admin"))

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

admin_base = declarative_base(metadata=MetaData(bind=engine, schema="admin"))

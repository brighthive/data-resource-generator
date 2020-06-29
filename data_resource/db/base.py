"""Database and ORM Fixtures."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from data_resource.config import ConfigurationFactory


data_resource_config = ConfigurationFactory.from_env()
engine = create_engine(
    data_resource_config.SQLALCHEMY_DATABASE_URI, pool_size=20, max_overflow=0
)

from sqlalchemy.schema import CreateSchema  # noqa: E402

if not engine.dialect.has_schema(engine, "admin"):
    engine.execute(CreateSchema("admin"))

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

admin_base = declarative_base(metadata=MetaData(bind=engine, schema="admin"))

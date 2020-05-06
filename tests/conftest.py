import pytest
from data_resource.db import engine, Session, MetadataSingleton
from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text


class Database:
    def ping(self):
        try:
            session = Session()
            session.query("1").all()
            return True
        except OperationalError:
            raise

    # def table_count(self, table_name):
    #     session = Session()
    #     result = session.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")
    #     for _r in result:
    #         print(_r)

    # def table_fields(self, table_name):
    #     session = Session()
    #     s = text("SELECT * FROM information_schema.COLUMNS WHERE TABLE_NAME = :tblname")
    #     result = session.execute(s, tblname=table_name)
    #     for _r in result:
    #         print(_r)

    def destory_db(self):
        session = Session()
        session.execute("drop schema public cascade")
        session.execute("create schema public")
        session.commit()


class SqlalchemyMetadata:
    def table_count(self):
        metadata = MetadataSingleton.instance()
        return len(metadata.sorted_tables)


@pytest.fixture(autouse=True, scope="session")
def auto_run_empty_database():
    db = Database()
    db.destory_db()


@pytest.fixture(scope="function")
def database():
    db = Database()
    yield db


@pytest.fixture(scope="module")
def sqlalchemy_metadata():
    sql_metadata = SqlalchemyMetadata()
    yield sql_metadata

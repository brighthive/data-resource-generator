import pytest
from data_resource.db import engine, Session, MetadataSingleton
from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

# from app.app import run

DATA_DICTIONARY = {
    "@id": "https://mydatatrust.brighthive.io/dr1",
    "@type": "dataResource",
    "name": "2020 Census Data",
    "description": "Description of data resource",
    "owner": "org",
    "pointOfContact": "Tim the Pointman",  # probably a person node
    "published": True,
    "dateCreated": "date",
    "dateUpdated": "date",
    "privacyRegulations": ["https://datatrust.org/privacyregulations/HIPAA"],
    "category": "https://datatrust.org/catagory/external",
    "url": "https://mydatatrust.brighthive.io/dr1",
    "data": {
        "dataDictionary": [
            {
                "@id": "https://mydatatrust.brighthive.io/dr1/People",
                "@type": "table",
                "name": "People",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "id",
                            "title": "Person ID",
                            "type": "integer",
                            "description": "A unique identifer for person.",
                            "constraints": {},
                        },
                        {
                            "name": "name",
                            "title": "Person's Name",
                            "type": "string",
                            "description": "The name that a Person goes by. This is left intentionally generic.",
                            "constraints": {},
                        },
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            },
            {
                "@id": "https://mydatatrust.brighthive.io/dr1/Team",
                "@type": "table",
                "name": "Team",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "id",
                            "title": "Team ID",
                            "type": "integer",
                            "description": "A unique identifer for team.",
                            "constraints": {},
                        },
                        {
                            "name": "name",
                            "title": "Team Name",
                            "type": "string",
                            "description": "The name that a Team goes by.",
                            "constraints": {},
                        },
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            },
            {
                "@id": "https://mydatatrust.brighthive.io/dr1/Order",
                "@type": "table",
                "name": "Order",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "id",
                            "title": "Order ID",
                            "type": "integer",
                            "description": "Unique identifer for an Order.",
                            "constraints": {},
                        },
                        {
                            "name": "items",
                            "title": "Items in Order",
                            "type": "string",
                            "description": "Textual list of items in order.",
                            "constraints": {},
                        },
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            },
        ],
        "relationships": {
            # "oneToOne": [["People", "haveA", "Passport"],
            "oneToMany": [["People", "Order"]],
            "manyToMany": [["People", "Team"]],
        },
        "databaseSchema": "url-to-something",
        "databaseType": "https://datatrust.org/databaseType/rdbms",
    },
    "api": {
        "apiType": "https://datatrust.org/apiType/rest",
        "apiSpec": "url-to-swagger-or-json-swagger",
    },
}


@pytest.fixture
def VALID_DATA_DICTIONARY():
    return DATA_DICTIONARY


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


@pytest.fixture(scope="function")
def empty_database():
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


@pytest.fixture(scope="session")
def api():
    return run(actually_run=False).test_client()

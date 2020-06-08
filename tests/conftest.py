import pytest
from sqlalchemy.exc import OperationalError
from data_resource import start
from data_resource.db import db_session
from data_resource.generator.app import start_data_resource_generator
from data_resource.generator.model_manager.model_manager import create_models
from flask_restful import Api
from flask import Flask


data_dict = [
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
    {
        "@id": "https://mydatatrust.brighthive.io/dr1/Order",
        "@type": "table",
        "name": "Required",
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
                    "name": "required",
                    "title": "Required item",
                    "type": "integer",
                    "description": "A required field.",
                    "constraints": {"required": True},
                },
                {
                    "name": "optional",
                    "title": "Optional item",
                    "type": "integer",
                    "description": "Optional field.",
                    "constraints": {},
                },
            ],
            "primaryKey": "id",
            "missingValues": [],
        },
    },
]

people_descriptor = {
    "api": {
        "resource": "peoples",
        "methods": [
            {
                "get": {"enabled": True, "secured": False, "grants": ["get:users"]},
                "post": {"enabled": True, "secured": False, "grants": []},
                "put": {"enabled": True, "secured": False, "grants": []},
                "patch": {"enabled": True, "secured": False, "grants": []},
                "delete": {"enabled": True, "secured": False, "grants": []},
            }
        ],
    },
    "datastore": {
        "tablename": "peoples",
        "restricted_fields": [],
        "schema": {
            "fields": [
                {
                    "name": "id",
                    "title": "Person ID",
                    "type": "integer",
                    "description": "A unique identifer for person.",
                    "required": False,
                },
                {
                    "name": "name",
                    "title": "Person's Name",
                    "type": "string",
                    "description": "The name that a Person goes by. This is left intentionally generic.",
                    "required": False,
                },
            ],
            "primaryKey": "id",
        },
    },
}

# print(json.dumps(convert_descriptor_to_swagger([people_descriptor]), indent=4))

api_dict = {
    "openapi": "3.0.0",
    "info": {
        "title": "Swagger Data Resource",
        "description": "Autogenerated Data Resource API swagger file.  You can find\nout more about Swagger at\n[http://swagger.io](http://swagger.io) or on\n[irc.freenode.net, #swagger](http://swagger.io/irc/).\n",
        "termsOfService": "http://swagger.io/terms/",
        "contact": {"email": "engineering@brighthive.io"},
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
        },
        "version": "1.0.0",
    },
    "servers": [{"description": "Local server.", "url": "http://localhost:8000"}],
    "components": {
        "parameters": {
            "offsetParam": {
                "name": "offset",
                "in": "query",
                "description": "the offset",
                "required": False,
                "style": "form",
                "explode": True,
                "schema": {"type": "integer", "default": 0},
            },
            "limitParam": {
                "name": "limit",
                "in": "query",
                "description": "the limit",
                "required": False,
                "style": "form",
                "explode": True,
                "schema": {"type": "integer", "minimum": 0, "default": 100},
            },
        },
        "schemas": {
            "Links": {
                "type": "object",
                "properties": {
                    "rel": {
                        "type": "string",
                        "description": "...",
                        "example": "first",
                        "enum": ["self", "first", "prev", "next", "last"],
                    },
                    "href": {
                        "type": "string",
                        "description": "...",
                        "example": "/credentials?offset=0&limit=20",
                    },
                },
                "description": "...",
            },
            "Created": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "...",
                        "example": "Successfully added new resource.",
                    },
                    "id": {
                        "type": "integer",
                        "description": "...",
                        "format": "int64",
                        "example": 1,
                    },
                },
            },
            "People": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int64",
                        "description": "Person ID - A unique identifer for person.",
                    },
                    "name": {
                        "type": "string",
                        "description": "Person's Name - The name that a Person goes by. This is left intentionally generic.",
                    },
                },
                "description": "...",
            },
            "AllPeoples": {
                "type": "object",
                "properties": {
                    "peoples": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/People"},
                    },
                    "links": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Links"},
                    },
                },
                "description": "...",
            },
        },
        "responses": {
            "Created": {
                "description": "...",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Created"}
                    }
                },
            },
            "AllPeoples": {
                "description": "...",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/AllPeoples"}
                    }
                },
            },
        },
        "requestBodies": {
            "People": {
                "description": "Pet object that needs to be added to the store",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/People"}
                    }
                },
                "required": True,
            }
        },
    },
    "tags": [
        {
            "name": "peoples",
            "description": "...",
            "externalDocs": {
                "description": "Find out more",
                "url": "http://swagger.io",
            },
        }
    ],
    "paths": {
        "/peoples": {
            "get": {
                "operationId": "get_people",
                "tags": ["peoples"],
                "summary": "Get all items",
                "parameters": [
                    {"$ref": "#/components/parameters/offsetParam"},
                    {"$ref": "#/components/parameters/limitParam"},
                ],
                "responses": {"200": {"$ref": "#/components/responses/AllPeoples"}},
            },
            "post": {
                "operationId": "post_people",
                "tags": ["peoples"],
                "summary": "Create an item",
                "requestBody": {"$ref": "#/components/requestBodies/People"},
                "responses": {"201": {"$ref": "#/components/responses/Created"}},
            },
        },
        "/peoples/{id}": {
            "get": {
                "operationId": "get_people_id",
                "tags": ["peoples"],
                "summary": "Get one item",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "style": "simple",
                        "explode": False,
                        "schema": {"type": "integer", "format": "int64"},
                    }
                ],
                "responses": {"200": {"description": "ok"}},
            },
            "put": {
                "operationId": "put_people_id",
                "tags": ["peoples"],
                "summary": "Put one item",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "style": "simple",
                        "explode": False,
                        "schema": {"type": "integer", "format": "int64"},
                    }
                ],
                "requestBody": {"$ref": "#/components/requestBodies/People"},
                "responses": {"200": {"description": "ok"}},
            },
            "delete": {
                "operationId": "delete_people_id",
                "tags": ["peoples"],
                "summary": "Get one item",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "style": "simple",
                        "explode": False,
                        "schema": {"type": "integer", "format": "int64"},
                    }
                ],
                "responses": {"200": {"description": "ok"}},
            },
            "patch": {
                "operationId": "patch_people_id",
                "tags": ["peoples"],
                "summary": "Get one item",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "User ID",
                        "required": True,
                        "style": "simple",
                        "explode": False,
                        "schema": {"type": "integer", "format": "int64"},
                    }
                ],
                "requestBody": {"$ref": "#/components/requestBodies/People"},
                "responses": {"200": {"description": "ok"}},
            },
        },
    },
}


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
        "dataDictionary": data_dict,
        "relationships": {
            # "oneToOne": [["People", "haveA", "Passport"],
            "oneToMany": [["People", "Order"]],
            "manyToMany": [["People", "Team"]],
        },
        "databaseSchema": "url-to-something",
        "databaseType": "https://datatrust.org/databaseType/rdbms",
    },
    "api": {"apiType": "https://datatrust.org/apiType/rest", "apiSpec": api_dict},
}


@pytest.fixture
def VALID_DATA_DICTIONARY():
    return DATA_DICTIONARY


class Database:
    def ping(self):
        try:
            db_session.query("1").all()
            return True
        except OperationalError:
            raise

    def destory_db(self):
        try:
            db_session.execute("drop schema admin cascade")
            db_session.execute("create schema admin")
            db_session.execute("drop schema public cascade")
            db_session.execute("create schema public")
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()


@pytest.fixture(scope="function")
def empty_database():
    db = Database()
    db.destory_db()


@pytest.fixture
def valid_base(VALID_DATA_DICTIONARY, empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]
    base = create_models(table_descriptors)
    return base


@pytest.fixture
def valid_people_orm(valid_base):
    return getattr(valid_base.classes, "People")


@pytest.fixture
def valid_orm_with_required_field(valid_base):
    return getattr(valid_base.classes, "Required")


@pytest.fixture(scope="function")
def database():
    db = Database()
    yield db


@pytest.fixture(scope="function")
def admin_e2e(empty_database):
    app = start(actually_run=False)
    return app.test_client()


@pytest.fixture(scope="function")
def generated_e2e(empty_database):
    # start the app
    app = start(actually_run=False)

    api = app.config["api"]

    # skip generation process -- inject the data dict
    start_data_resource_generator(DATA_DICTIONARY, api)

    return app.test_client()


@pytest.fixture(scope="function")
def empty_api():
    app = Flask("what")
    api = Api(app)
    return api

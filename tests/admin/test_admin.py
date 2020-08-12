import json
from pytest_mock import mocker
import pytest


tableschema_1 = {
    "tableschema": {
        "api": {
            "resource": "peoples",
            "methods": [
                {
                    "get": {"enabled": True, "secured": False, "grants": ["get:users"]},
                    "post": {"enabled": True, "secured": False},
                    "put": {"enabled": True, "secured": False},
                    "patch": {"enabled": True, "secured": False},
                    "delete": {"enabled": True, "secured": False},
                }
            ],
        },
        "datastore": {
            "tablename": "peoples",
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
}
tableschema_2 = {
    "tableschema": {
        "api": {
            "resource": "teams",
            "methods": [
                {
                    "get": {"enabled": True, "secured": False, "grants": ["get:users"]},
                    "post": {"enabled": True, "secured": False},
                    "put": {"enabled": True, "secured": False},
                    "patch": {"enabled": True, "secured": False},
                    "delete": {"enabled": True, "secured": False},
                }
            ],
        },
        "datastore": {
            "tablename": "teams",
            "schema": {
                "fields": [
                    {
                        "name": "id",
                        "title": "Team ID",
                        "type": "integer",
                        "description": "A unique identifer for team.",
                        "required": False,
                    },
                    {
                        "name": "name",
                        "title": "Team Name",
                        "type": "string",
                        "description": "The name that a Team goes by.",
                        "required": False,
                    },
                ],
                "primaryKey": "id",
            },
        },
    }
}
data_resource_schema = {
    "data_resource_schema": {
        "@id": "https://mydatatrust.brighthive.io/dr1",
        "@type": "dataResource",
        "name": "2020 Census Data",
        "description": "Description of data resource",
        "owner": "org",
        "pointOfContact": "Tim the Pointman",
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
                                "title": "Person's name",
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
            "relationships": {"manyToMany": [["People", "Team"]]},
            "databaseSchema": "url-to-something",
            "databaseType": "https://datatrust.org/databaseType/rdbms",
        },
        "api": {
            "apiType": "https://datatrust.org/apiType/rest",
            "apiSpec": {
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
                "servers": [
                    {"description": "Local server.", "url": "http://localhost:8000"}
                ],
                "components": {
                    "parameters": {
                        "offsetParam": {
                            "name": "offset",
                            "in": "query",
                            "description": "the offset",
                            "required": False,
                            "style": "form",
                            "explode": True,
                            "schema": {"type": "integer"},
                        },
                        "limitParam": {
                            "name": "limit",
                            "in": "query",
                            "description": "the limit",
                            "required": False,
                            "style": "form",
                            "explode": True,
                            "schema": {"type": "integer"},
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
                        "Team": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "format": "int64",
                                    "description": "Team ID - A unique identifer for team.",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Team Name - The name that a Team goes by.",
                                },
                            },
                            "description": "...",
                        },
                        "AllTeams": {
                            "type": "object",
                            "properties": {
                                "teams": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Team"},
                                },
                                "links": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Links"},
                                },
                            },
                            "description": "...",
                        },
                        "Order": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "format": "int64",
                                    "description": "Order ID - Unique identifer for an Order.",
                                },
                                "items": {
                                    "type": "string",
                                    "description": "Items in Order - Textual list of items in order.",
                                },
                            },
                            "description": "...",
                        },
                        "AllOrders": {
                            "type": "object",
                            "properties": {
                                "orders": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Order"},
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
                                    "schema": {
                                        "$ref": "#/components/schemas/AllPeoples"
                                    }
                                }
                            },
                        },
                        "AllTeams": {
                            "description": "...",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AllTeams"}
                                }
                            },
                        },
                        "AllOrders": {
                            "description": "...",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AllOrders"}
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
                        },
                        "Team": {
                            "description": "Pet object that needs to be added to the store",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Team"}
                                }
                            },
                            "required": True,
                        },
                        "Order": {
                            "description": "Pet object that needs to be added to the store",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Order"}
                                }
                            },
                            "required": True,
                        },
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
                    },
                    {
                        "name": "teams",
                        "description": "...",
                        "externalDocs": {
                            "description": "Find out more",
                            "url": "http://swagger.io",
                        },
                    },
                    {
                        "name": "orders",
                        "description": "...",
                        "externalDocs": {
                            "description": "Find out more",
                            "url": "http://swagger.io",
                        },
                    },
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
                            "responses": {
                                "200": {"$ref": "#/components/responses/AllPeoples"}
                            },
                        },
                        "post": {
                            "operationId": "post_people",
                            "tags": ["peoples"],
                            "summary": "Create an item",
                            "requestBody": {
                                "$ref": "#/components/requestBodies/People"
                            },
                            "responses": {
                                "201": {"$ref": "#/components/responses/Created"}
                            },
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
                            "requestBody": {
                                "$ref": "#/components/requestBodies/People"
                            },
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
                            "requestBody": {
                                "$ref": "#/components/requestBodies/People"
                            },
                            "responses": {"200": {"description": "ok"}},
                        },
                    },
                    "/teams": {
                        "get": {
                            "operationId": "get_team",
                            "tags": ["teams"],
                            "summary": "Get all items",
                            "parameters": [
                                {"$ref": "#/components/parameters/offsetParam"},
                                {"$ref": "#/components/parameters/limitParam"},
                            ],
                            "responses": {
                                "200": {"$ref": "#/components/responses/AllTeams"}
                            },
                        },
                        "post": {
                            "operationId": "post_team",
                            "tags": ["teams"],
                            "summary": "Create an item",
                            "requestBody": {"$ref": "#/components/requestBodies/Team"},
                            "responses": {
                                "201": {"$ref": "#/components/responses/Created"}
                            },
                        },
                    },
                    "/teams/{id}": {
                        "get": {
                            "operationId": "get_team_id",
                            "tags": ["teams"],
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
                            "operationId": "put_team_id",
                            "tags": ["teams"],
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
                            "requestBody": {"$ref": "#/components/requestBodies/Team"},
                            "responses": {"200": {"description": "ok"}},
                        },
                        "delete": {
                            "operationId": "delete_team_id",
                            "tags": ["teams"],
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
                            "operationId": "patch_team_id",
                            "tags": ["teams"],
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
                            "requestBody": {"$ref": "#/components/requestBodies/Team"},
                            "responses": {"200": {"description": "ok"}},
                        },
                    },
                    "/orders": {
                        "get": {
                            "operationId": "get_order",
                            "tags": ["orders"],
                            "summary": "Get all items",
                            "parameters": [
                                {"$ref": "#/components/parameters/offsetParam"},
                                {"$ref": "#/components/parameters/limitParam"},
                            ],
                            "responses": {
                                "200": {"$ref": "#/components/responses/AllOrders"}
                            },
                        },
                        "post": {
                            "operationId": "post_order",
                            "tags": ["orders"],
                            "summary": "Create an item",
                            "requestBody": {"$ref": "#/components/requestBodies/Order"},
                            "responses": {
                                "201": {"$ref": "#/components/responses/Created"}
                            },
                        },
                    },
                    "/orders/{id}": {
                        "get": {
                            "operationId": "get_order_id",
                            "tags": ["orders"],
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
                            "operationId": "put_order_id",
                            "tags": ["orders"],
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
                            "requestBody": {"$ref": "#/components/requestBodies/Order"},
                            "responses": {"200": {"description": "ok"}},
                        },
                        "delete": {
                            "operationId": "delete_order_id",
                            "tags": ["orders"],
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
                            "operationId": "patch_order_id",
                            "tags": ["orders"],
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
                            "requestBody": {"$ref": "#/components/requestBodies/Order"},
                            "responses": {"200": {"description": "ok"}},
                        },
                    },
                },
            },
        },
    }
}


@pytest.mark.requiresdb
def test_admin_api(admin_e2e, mocker):
    m = mocker.patch(
        "data_resource.generator.app.start_data_resource_generator", return_value=None
    )
    api = admin_e2e

    # put tableschema
    response = api.put("/tableschema/1", json=tableschema_1)
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["tableschema"]
    assert body["swagger"]

    # put tableschema
    response = api.put("/tableschema/2", json=tableschema_2)
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["tableschema"]
    assert body["swagger"]

    # get swagger
    # assert both tableschema
    response = api.get("/swagger")
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["swagger"]
    assert "/peoples" in body["swagger"]["paths"]
    assert "/teams" in body["swagger"]["paths"]

    # assert generator fn gets called?
    response = api.post("/generator", json=data_resource_schema)
    assert response.status_code == 204

    assert response.data == b""

    assert m.called_once()


@pytest.mark.requiresdb
def test_swagger_ui_exists(admin_e2e):
    api = admin_e2e

    response = api.get("/ui")

    # Should get 308 redirect to data['location']
    assert response.status_code in [200, 308]


@pytest.mark.requiresdb
def test_drg_schema_no_key_failure(admin_e2e):
    api = admin_e2e

    response = api.post("/generator", json={"this is invalid": {1: 2}})

    assert response.json == {
        "error": "Data Resource Schema should be placed inside root key 'data_resource_schema'."
    }
    assert response.status_code == 400


@pytest.mark.requiresdb
def test_drg_schema_failure(admin_e2e):
    api = admin_e2e

    response = api.post(
        "/generator", json={"data_resource_schema": {"this is invalid": {1: 2}}}
    )

    assert response.json == {
        "error": "Data Resource Schema validation failure",
        "errors": ["'data' is a required property", "'api' is a required property"],
    }
    assert response.status_code == 400

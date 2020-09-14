DATA_DICTIONARY = {
    "@context": ["https://schema.org", {"bh": "https://schema.brighthive.io/"}],
    "@type": "bh:DataResource",
    "@id": "https://mydatatrust.brighthive.io/dr1",
    "name": "2020 Census Data",
    "description": "Description of data resource",
    "ownerOrg": [
        {
            "@type": "Organization",
            "@id": "#brighthive-org",
            "name": "BrightHive",
            "contactPoint": [
                {
                    "@type": "ContactPoint",
                    "@id": "#matt",
                    "name": "Matt Gee",
                    "telephone": "555-555-5555",
                    "email": "matt@company.io",
                    "contactType": "Developer",
                }
            ],
        }
    ],
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
                "@type": "bh:table",
                "name": "people",
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
                "@type": "bh:table",
                "name": "team",
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
                "@type": "bh:table",
                "name": "order",
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
                "@id": "https://mydatatrust.brighthive.io/dr1/Required",
                "@type": "bh:table",
                "name": "required",
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
                "/people": {
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
                        "requestBody": {"$ref": "#/components/requestBodies/People"},
                        "responses": {
                            "201": {"$ref": "#/components/responses/Created"}
                        },
                    },
                },
                "/people/{id}": {
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
                "/people/query": {"get": {}, "post": {}},
                "/team": {"get": {}},
                "/team/{id}": {"get": {}, "put": {}},
                "/people/{id}/team": {"get": {}, "put": {}, "patch": {}},
                "/team/{id}/people": {"get": {}, "put": {}, "patch": {}},
            },
        },
    },
}

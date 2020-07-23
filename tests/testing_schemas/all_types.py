ALL_TYPES_DATA_DICTIONARY = {
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
                            "name": "name",
                            "title": "Person's Name",
                            "type": "string",
                            "description": "The name that a Person goes by. This is left intentionally generic.",
                            "constraints": {},
                        },
                        {
                            "name": "id",
                            "type": "integer",
                            "title": "id",
                            "constraints": {},
                        },
                        {
                            "name": "string",
                            "title": "string",
                            "type": "string",
                            "constraints": {},
                        },
                        {
                            "name": "number",
                            "title": "number",
                            "type": "number",
                            "constraints": {},
                        },
                        {
                            "name": "integer",
                            "title": "integer",
                            "type": "integer",
                            "constraints": {},
                        },
                        {
                            "name": "boolean",
                            "title": "boolean",
                            "type": "boolean",
                            "constraints": {},
                        },
                        {
                            "name": "object",
                            "title": "object",
                            "type": "object",
                            "constraints": {},
                        },
                        {
                            "name": "array",
                            "title": "array",
                            "type": "array",
                            "constraints": {},
                        },
                        {
                            "name": "date",
                            "title": "date",
                            "type": "date",
                            "constraints": {},
                        },
                        {
                            "name": "time",
                            "title": "time",
                            "type": "time",
                            "constraints": {},
                        },
                        {
                            "name": "datetime",
                            "title": "datetime",
                            "type": "datetime",
                            "constraints": {},
                        },
                        {
                            "name": "year",
                            "title": "year",
                            "type": "year",
                            "constraints": {},
                        },
                        {
                            "name": "yearmonth",
                            "title": "yearmonth",
                            "type": "yearmonth",
                            "constraints": {},
                        },
                        {
                            "name": "duration",
                            "title": "duration",
                            "type": "duration",
                            "constraints": {},
                        },
                        {
                            "name": "geopoint",
                            "title": "geopoint",
                            "type": "geopoint",
                            "constraints": {},
                        },
                        {
                            "name": "geojson",
                            "title": "geojson",
                            "type": "geojson",
                            "constraints": {},
                        },
                        {
                            "name": "any",
                            "title": "any",
                            "type": "any",
                            "constraints": {},
                        },
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            }
        ],
        "relationships": {
            # "oneToOne": [["People", "haveA", "Passport"],
            "manyToMany": []
        },
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
            },
        },
    },
}

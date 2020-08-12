from jsonschema import Draft7Validator
from data_resource.shared_utils.api_exceptions import ApiError


data_resource_schema_json_scehma = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "definitions": {
        "superTableSchema": {
            "properties": {
                "@id": {"type": "string"},
                "@type": {"type": "string"},
                "databaseSchema": {"type": "string"},
                "databaseType": {"type": "string"},
                "name": {"type": "string"},
                "relationships": {
                    "properties": {"manyToMany": {"type": "array"}},
                    "type": "object",
                },
                "tableSchema": {
                    "$ref": "https://specs.frictionlessdata.io/schemas/table-schema.json"
                },
            },
            "required": ["name", "tableSchema"],
        }
    },
    "description": "A Data Resource Schema for use with BrightHive Data Resource Generator",
    "properties": {
        "@id": {"type": "string"},
        "@type": {"type": "string"},
        "api": {
            "properties": {
                "apiSpec": {
                    "$ref": "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/schemas/v3.0/schema.json",
                    "description": "OpenAPI Spec 3.0 Document",
                },
                "apiType": {"type": "string"},
            },
            "required": ["apiSpec"],
            "type": "object",
        },
        "category": {"type": "string"},
        "data": {
            "properties": {
                "dataDictionary": {
                    "items": {"$ref": "#/definitions/superTableSchema"},
                    "type": "array",
                }
            },
            "required": ["dataDictionary"],
            "type": "object",
        },
        "dateCreated": {"type": "string"},
        "dateUpdated": {"type": "string"},
        "description": {"type": "string"},
        "name": {"type": "string"},
        "owner": {"type": "string"},
        "pointOfContact": {"type": "string"},
        "privacyRegulations": {
            "items": {"type": "string"},
            "minItems": 1,
            "type": "array",
            "uniqueItems": True,
        },
        "published": {"type": "boolean"},
        "url": {"type": "string"},
    },
    "required": ["data", "api"],
    "title": "Table Schema",
    "type": "object",
}


class DataResourceSchemaValidationError(Exception):
    pass


def validate_data_resource_schema(data_resource_schema):
    # validate(data_resource_schema, schema=data_resource_schema_json_scehma)
    v = Draft7Validator(data_resource_schema_json_scehma)

    errors = []
    for error in v.iter_errors(data_resource_schema):
        errors.append(error.message)

    if errors:
        raise ApiError("Data Resource Schema validation failure", errors=errors)

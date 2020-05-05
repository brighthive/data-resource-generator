import pytest
from data_resource.model_manager.model_manager import convert_table_schema_to_database


VALID_DATA_DICTIONARY = {
    "@id": "https://mydatatrust.brighthive.io/dr1",
    "@type": "dataResource",
    "name": "2020 Census Data",
    "description": "talk about the data",
    "owner": "org",
    "pointOfContact": "person",
    "published": True,
    "dateCreated": "date",
    "dateUpdated": "date",
    "privacyRegulations": ["https://datatrust.org/privacyregulations/HIPAA"],
    "category": "https://datatrust.org/catagory/external",
    "url": "https://mydatatrust.brighthive.io/dr1",
    "data": {
        "dataDictionary": [
            {
                "@id": "https://mydatatrust.brighthive.io/dr1/people",
                "@type": "table",
                "name": "people",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "asdf",
                            "title": "A nicer human readable label or title for the field",
                            "type": "boolean",
                            "description": "A data dict description for the field",
                            "constraints": {},
                        },
                        {
                            "name": "marked_present",
                            "title": "A nicer human readable label or title for the field",
                            "type": "boolean",
                            "description": "A data dict description for the field",
                            "constraints": {},
                        },
                    ],
                    "missingValues": [],
                },
            }
        ],
        "relationships": {
            "oneToOne": [["person", "hasA", "passport"], ["person", "hasA", "mother"]],
            "oneToMany": [["person", "caresFor", "pet"]],
            "manyToMany": [["person", "worksAt", "job"]],
        },
        "databaseSchema": "url-to-something",
        "databaseType": "https://datatrust.org/databaseType/rdbms",
    },
    "api": {
        "apiType": "https://datatrust.org/apiType/rest",
        "apiSpec": "url-to-swagger",
    },
}


@pytest.mark.requiresdb
def test_valid_descriptor_creates_databased(database, sqlalchemy_metadata):
    table_schema = VALID_DATA_DICTIONARY["data"]["dataDictionary"][0]["tableSchema"]
    table_name = "test"

    convert_table_schema_to_database("test", table_schema)

    # assert database.table_count("test") == 1
    assert sqlalchemy_metadata.table_count() == 1

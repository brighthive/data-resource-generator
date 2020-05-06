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
                "@id": "https://mydatatrust.brighthive.io/dr1/People",
                "@type": "table",
                "name": "People",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "person_id",
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
                    "primaryKey": "person_id",
                    "missingValues": [],
                },
            },
            {
                "@id": "https://mydatatrust.brighthive.io/dr1/GameConsole",
                "@type": "table",
                "name": "GameConsole",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "game_console_id",
                            "title": "Game Console ID",
                            "type": "integer",
                            "description": "Unique identifer for a Game Console.",
                            "constraints": {},
                        },
                        {
                            "name": "name",
                            "title": "Game Console Name",
                            "type": "string",
                            "description": "The name of the Game Console.",
                            "constraints": {},
                        },
                        {
                            "name": "producer_company",
                            "title": "Game Console Company",
                            "type": "string",
                            "description": "The name of the Company that created the Game Console.",
                            "constraints": {},
                        },
                        {
                            "name": "controller_ports_count",
                            "title": "Number of Controller Ports",
                            "type": "integer",
                            "description": "The maximum number of concurrent controllers supported.",
                            "constraints": {},
                        },
                    ],
                    "primaryKey": "game_console_id",
                    "missingValues": [],
                },
            },
        ],
        "relationships": {
            # "oneToOne": [["People", "haveA", "Passport"],
            "oneToMany": [["People", "playGameConsole", "GameConsole"]],
            "manyToMany": [["People", "friendsWith", "People"]],
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

import pytest
from data_resource.model_manager.model_manager import (
    create_all_tables_from_schemas,
    get_table_names_and_descriptors,
    main,
)
from data_resource.db.base import MetadataSingleton


VALID_DATA_DICTIONARY = {
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
                "@id": "https://mydatatrust.brighthive.io/dr1/GameConsole",
                "@type": "table",
                "name": "GameConsole",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "id",
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
                    "primaryKey": "id",
                    "missingValues": [],
                },
            },
        ],
        "relationships": {
            # "oneToOne": [["People", "haveA", "Passport"],
            # "oneToMany": [["People", "playGameConsole", "GameConsole"]],
            "manyToMany": [["People", "Team"]]
        },
        "databaseSchema": "url-to-something",
        "databaseType": "https://datatrust.org/databaseType/rdbms",
    },
    "api": {
        "apiType": "https://datatrust.org/apiType/rest",
        "apiSpec": "url-to-swagger-or-json-swagger",
    },
}


# TODO: Need to destroy db on this fn
@pytest.mark.unit
def test_main_creates_all_required_orm(empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]["dataDictionary"]
    MetadataSingleton._clear()

    # act
    main(table_descriptors)

    # assert
    metadata = MetadataSingleton.instance()

    # assert tables exist
    # assert people table
    # assert gameconsole table
    # assert assoc_gameconsole_people table

    # automap:
    # assert people.gameconsole exists
    # assert gameconsole.people exists


# def test_main_can_add_data_with_orm
# create orm
# add items to db via classes
# assert db has it


@pytest.mark.requiresdb
def test_valid_descriptor_creates_databased(empty_database, sqlalchemy_metadata):
    table_descriptors = VALID_DATA_DICTIONARY["data"]["dataDictionary"]

    create_all_tables_from_schemas(table_descriptors)

    # assert database.table_count("test") == 1
    assert sqlalchemy_metadata.table_count() == 3


@pytest.mark.unit
def test_get_table_names_and_descriptors():
    table_descriptors = VALID_DATA_DICTIONARY["data"]["dataDictionary"]

    table_names, descriptors = get_table_names_and_descriptors(table_descriptors)

    assert len(table_names) == 3
    assert table_names == ["People", "Team", "GameConsole"]
    assert len(descriptors) == 3

import pytest
from data_resource.model_manager.model_manager import (
    create_all_tables_from_schemas,
    get_table_names_and_descriptors,
    main,
    get_relationships_from_data_dict,
)
from data_resource.db.base import MetadataSingleton, AutobaseSingleton


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


@pytest.mark.unit  # Does this requiredb tho?
def test_main_creates_all_required_orm(empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]
    MetadataSingleton._clear()
    AutobaseSingleton._clear()

    main(table_descriptors)

    metadata = MetadataSingleton.instance()
    base = AutobaseSingleton.instance()
    assert "People" in metadata.tables
    assert "Team" in metadata.tables
    assert "Order" in metadata.tables
    assert "assoc_people_team" in metadata.tables

    # Assert that the auto mapped python classes exist!
    assert base.classes.People
    assert base.classes.Team


# def test_main_can_add_data_with_orm
# create orm
# add items to db via classes
# assert db has it


@pytest.mark.requiresdb
def test_valid_descriptor_creates_databased(empty_database, sqlalchemy_metadata):
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    create_all_tables_from_schemas(table_descriptors)

    # assert database.table_count("test") == 1
    assert sqlalchemy_metadata.table_count() == 3


@pytest.mark.unit
def test_get_table_names_and_descriptors():
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    table_names, descriptors = get_table_names_and_descriptors(table_descriptors)

    assert len(table_names) == 3
    assert table_names == ["People", "Team", "Order"]
    assert len(descriptors) == 3


@pytest.mark.unit
def test_get_relationships_from_data_dict():
    table_descriptors = VALID_DATA_DICTIONARY["data"]

    result = get_relationships_from_data_dict(table_descriptors)

    assert result == {
        # "oneToOne": [["People", "haveA", "Passport"],
        "oneToMany": [["People", "Order"]],
        "manyToMany": [["People", "Team"]],
    }

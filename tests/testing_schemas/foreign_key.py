_MISSING_FOREIGN_KEY_TABLE = {
    "ignore_validation": 1,
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
                "@id": "https://mydatatrust.brighthive.io/dr1/fk_relation",
                "@type": "bh:table",
                "name": "fk_relation",
                "tableSchema": {
                    "fields": [
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
                    ],
                    "foreignKeys": [
                        {
                            "fields": "fk_field",
                            "reference": {"resource": "fk_table", "fields": "id"},
                        }
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            }
        ],
        "databaseSchema": "url-to-something",
        "databaseType": "https://datatrust.org/databaseType/rdbms",
    },
    "api": {"apiType": "https://datatrust.org/apiType/rest", "apiSpec": {}},
}


_VALID_FOREIGN_KEY = {
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
                "@id": "https://mydatatrust.brighthive.io/dr1/fk_relation",
                "@type": "bh:table",
                "name": "fk_relation",
                "tableSchema": {
                    "fields": [
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
                            "name": "fk_field",
                            "type": "integer",
                            "title": "fk_field",
                            "constraints": {},
                        },
                    ],
                    "foreignKeys": [
                        {
                            "fields": "fk_field",
                            "reference": {"resource": "fk_table", "fields": "id"},
                        }
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            },
            {
                "@id": "https://mydatatrust.brighthive.io/dr1/fk_table",
                "@type": "bh:table",
                "name": "fk_table",
                "tableSchema": {
                    "fields": [
                        {
                            "name": "id",
                            "type": "integer",
                            "title": "id",
                            "constraints": {},
                        }
                    ],
                    "primaryKey": "id",
                    "missingValues": [],
                },
            },
        ],
        "databaseSchema": "url-to-something",
        "databaseType": "https://datatrust.org/databaseType/rdbms",
    },
    "api": {"apiType": "https://datatrust.org/apiType/rest", "apiSpec": {}},
}

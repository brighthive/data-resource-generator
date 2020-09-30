# Data Resource Generator

![Maintenance](https://img.shields.io/maintenance/yes/2020)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/brighthive/data-resource-generator)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/brighthive/data-resource-generator)
![GitHub](https://img.shields.io/github/license/brighthive/data-resource-generator)

<!-- ![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/brighthive/data-resource-generator) -->
<!-- ![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/brighthive/data-resource-generator/v1.1.1) -->
<!-- ![CircleCI](https://img.shields.io/circleci/build/github/brighthive/data-resource-generator) -->
<!-- ![Coveralls github](https://img.shields.io/coveralls/github/brighthive/data-resource-generator) -->

![Twitter Follow](https://img.shields.io/twitter/follow/brighthiveio?style=social)

An elegant, opinionated framework for deploying BrightHive Data Resources (declarative database and API) with zero coding.

## Motivation

[BrightHive](https://brighthive.io) is in the business of building **Data Trusts**, which are *legal, technical, and governance frameworks that enable networks of organizations to securely and responsibly share and collaborate with data, generating new insights and increasing their combined impact.*

## Features

Simply provide the application a declarative database and API specification via API and it will automatically stand up a RESTful database and API!

- Declarative database with RESTful API using frictionless table schema and swagger

    - Dynamically generates SQLAlchemy ORM

    - Dynamically generates RESTful routing

- Column level encryption

<!--
### Supported -- tested
- Generate database from table schema
- Many to many
- Many to one
- Automatic REST API

### Assumed supported -- untested
- one to one ?

### Not supported yet
- many to many self-referential

### Future
- Enable/disable HTTP routes -->

## How to use Data Resource Generator

See "basic usage" in the docs.

### Column Level Encryption

DRG supports column level encryption (CLE) using the `sqlalchemy_utils` -> `EncryptedType`. The encryption engine is derived from the base class `EncryptionDecryptionBaseEngine`. To enable CLE please set the `protected` field within the table schema to `true`.

```bash
{
      "name":"password",
      "title":"Person's Password",
      "type":"string",
      "description":"This is left intentionally generic.",
      "constraints":{ },
      "protected": true
}
```

If the `protected` field is defined within the schema, the `encryptionSchema` field must be defined within the table schema itself or at the root level of the JSON object. If the DRG cannot find the `encryptionSchema` within the schema, it will error out during the generator process. Depending on placement within the schema, the `encryptionSchema` will allow wildcard engine/key for the whole DB, wildcard for a table, and individual engine/key for each column. The `encryptionSchema` has two required fields: `type` and `key`. The `type` is one of the supported engines below and `key` is the environment variable where the raw key or AWS ARN is defined.

##### Supported Engines

- `AES_GCM_Engine`
- `AWS_AES_Engine`

##### Example

The example below demonstrates an `encryptionSchema` where the table has a defined wildcard and a column specific engine/key. In this case, if there were two `protected` fields (password, ssn) then the password column would be protected with AWS KMS, and ssn would use the wildcard.

```bash
{
	"encryptionSchema": {
	    "*": {
	        "key": "DB_TABLE_PEOPLE_WILDCARD",
	        "type": "AES_256_GCM"
	    },
	    "password" : {
	        "key": "DB_PEOPLE_KMS_ARN",
	        "type": "AWS_AES_Engine"
	    }
	}
}
```


## How to develop Data Resource Generator

Please see https://data-resource-generator.readthedocs.io/en/latest/ for docs.

> We welcome code contributions, suggestions, and reports! Please report bugs and make suggestions using Github issues. The BrightHive team will triage and prioritize your issue as soon as possible.

[For development this application uses pre-commit hooks](https://pre-commit.com/). When you make a commit the modified files will be put through a series of tests. If all tests pass then you will be able to make a commit, otherwise corrections will either automatically be made or need to be manually corrected. [Please see pre-commit hooks website for instructions](https://pre-commit.com/) and [reference the pre-commit yaml file to see the tests that are run](.pre-commit-config.yaml).

1. Install pipenv.
1. Install docker and docker-compose.
1. Clone the repo.
1. Install production and development packages

    ```bash
    pipenv install --dev
    ```

1. Install pre-commit hooks,

    ```bash
    pipenv run pre-commit install
    ```

### Quick note about pre-commit hooks

In the event that you want to run pre-commit hooks over the entire application use the following,

```bash
pipenv run pre-commit run --all-files
```

### Testing

Some tests require that a database (Postgres) is running. We use docker to handle this for us. We have included a docker-compose file that allows you to easily run Postgres.

For developers to run the test suite,

1. First install the required packages

    ```bash
    pipenv install --dev
    ```

1. Stand up the database

    ```bash
    docker-compose -f test-database-docker-compose.yml up -d
    ```
    <!-- docker run --name data_resource_test_database -e POSTGRES_PASSWORD=test_password -e POSTGRES_USER=test_user -e POSTGRES_DATABASE=data_resource_dev -d postgres -->

1. Run the tests with the following command,

    ```bash
    pipenv run pytest
    ```

## Team

- Logan Ripplinger (Software Engineer)
- Gregory Mundy (VP of Engineering)
- John O'Sullivan (Software Engineer)

## License

[MIT](LICENSE)

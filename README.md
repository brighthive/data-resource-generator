# Data Resource Generator

![Maintenance](https://img.shields.io/maintenance/yes/2020)

<!-- ![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/brighthive/data-resource) -->
<!-- ![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/brighthive/data-resource-api/v1.1.1) -->

<!-- ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/brighthive/data-resource) -->

<!-- ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/brighthive/data-resource) -->

<!-- ![CircleCI](https://img.shields.io/circleci/build/github/brighthive/data-resource) -->

<!-- ![GitHub](https://img.shields.io/github/license/brighthive/data-resource) -->

<!-- ![Coveralls github](https://img.shields.io/coveralls/github/brighthive/data-resource) -->

![Twitter Follow](https://img.shields.io/twitter/follow/brighthiveio?style=social)

An elegant, opinionated framework for deploying BrightHive Data Resources (declarative database and API) with zero coding.

## Motivation

[BrightHive](https://brighthive.io) is in the business of building **Data Trusts**, which are *legal, technical, and governance frameworks that enable networks of organizations to securely and responsibly share and collaborate with data, generating new insights and increasing their combined impact.*

**Data Resources** are a core element of Data Trusts and may be loosely defined as *data that is owned by or stewarded over by members of Data Trusts.*

From the technical perspective, a BrightHive Data Resource is an entity comprised of the following elements:

- **Data Model** - The data model consists of one or more database tables and associated Object Relational Mapping (ORM) objects for communicating with these tables.
- **RESTful API** - Data managed by Data Resources are accessed via RESTful API endpoints. These endpoints support standard operations (i.e. **GET**, **POST**, **PUT**, **PATCH**, **DELETE**).
- **Data Resource Schemas** - Data Resource Schemas are JSON documents that define the data model, API endpoints, and security constraints placed on the specific Data Resource. These schemas are what allow for new Data Resources to be created without new code being written.

## Features

Simply provide the application a declarative database and API specification and it will automatically stand up a RESTful database and API!

- Declarative Database using frictionless table schema
- Generates SQLAlchemy ORM (including many to many)

<!--
### Supported -- tested
- Generate database from table schema
- Many to many
- Many to one

### Assumed supported -- untested
- one to one ?

### Not supported yet
- many to many self-referential

### Future
- Automatic REST API
- Enable/disable HTTP routes -->

## How to use Data Resource Generator

### Definitions

Data Resource Descriptor: BrightHive specification. Includes an API definition and a tableschema to describe the database. Please see [BrightHive Data Resource API](https://github.com/brighthive/data-resource-api).

Data Catalog: BrightHive specification. JSONLD document Please see [specification in progress](example.com) for more information.

### Start the application

1. Restart the database to clear the data.

```bash
docker-compose -f test-database-docker-compose.yml down && docker-compose -f test-database-docker-compose.yml up -d
```

1. To run the application,

```bash
pipenv run python run.py
```

### Generate Data Resources

Interact with the "Admin" routes to generate Data Resources.

- `PUT /tableschema/1` Put Data Resource Descriptor to this route.
- `GET /tableschema` Get all Data Resource Descriptors you have posted.
- `GET /swagger` Generate a swagger file from all the Data Resource Descriptors you have submitted.
- `POST /generator` Given a Data Catalog, this will generate all of the described Data Resources.

### Interacting with Generated Data Resources

An interactive API (using Swagger UI) is generated at `/ui`.

The following are the API routes that you can interact with for each of your generated resources:

- `GET resource`
- `GET resource/1`
- `POST resource`
- `PUT resource/1`
- `DELETE resource/1`

## How to develop Data Resource Generator

> We welcome code contributions, suggestions, and reports! Please report bugs and make suggestions using Github issues. The BrightHive team will triage and prioritize your issue as soon as possible.

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

## Testing

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

## License

[MIT](LICENSE)

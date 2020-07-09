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

Simply provide the application a declarative database and API specification via API and it will automatically stand up a RESTful database and API!

- Declarative Database using frictionless table schema using RESTful API
- Dynamically generates SQLAlchemy ORM
- Dynamically generates RESTful routing

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

### Definitions

Data Resource Descriptor: BrightHive specification. Includes an API definition and a tableschema to describe the database. Please see [BrightHive Data Resource API](https://github.com/brighthive/data-resource-api).

Data Resource Schema: BrightHive specification. JSONLD document. Please see [specification in progress](example.com) for more information.

### Start the application

There are two ways to run the application. Using docker is highly preferred.

#### Using Docker

To run via docker, first build image:

```bash
docker build -t brighthive/data-resource-generator .
```

then run:

```###bash
docker-compose up
```

To use AWS Secret Manager set environment variable `AWS_SM_ENABLED` to `1` (default 0). This will enabled the feature but will require the following environment variables to initialize correctly:

```bash
export AWS_SM_ENABLED=1
export AWS_SM_NAME=<aws-secet-name> ex. my-data-secrets
export AWS_SM_REGION=<aws-region> ex. us-west-1
export AWS_SM_DBNAME=<rds-database-name> ex. postgres
export AWS_ACCESS_KEY_ID=<aws-key-id>
export AWS_SECRET_ACCESS_KEY=<aws-secret>
```
For more information about AWS SM and how to setup on AWS console please visit: <a href="https://aws.amazon.com/secrets-manager/">AWS SM Docs</a>

#### Using python

1. Restart the database to clear the data.

```bash
docker-compose -f test-database-docker-compose.yml down && docker-compose -f test-database-docker-compose.yml up -d
```

1. To run the application,

```bash
pipenv run python wsgi.py
```

##### AWS Secret Manager Integration

To use AWS Secret Manager set environment variable `AWS_SM_ENABLED` to `1` (default 0). This will enabled the feature but will require the following environment variables to initialize correctly:

```bash
export AWS_SM_ENABLED=1
export AWS_SM_NAME=<aws-secet-name> ex. my-data-secrets
export AWS_SM_REGION=<aws-region> ex. us-west-1
export AWS_SM_DBNAME=<rds-database-name> ex. postgres
export AWS_ACCESS_KEY_ID=<aws-key-id>
export AWS_SECRET_ACCESS_KEY=<aws-secret>
```

For more information about AWS SM and how to setup on AWS console please visit: [https://aws.amazon.com/secrets-manager/](AWS SM Docs)

### Generate Data Resources

In production mode all generated routes will be secured by default.

#### Utilities to help create a Data Resource Schema

(You can Interact with the "Admin" routes to generate Data Resources. These provide a utility to help generate a swagger spec using https://github.com/brighthive/convert_descriptor_to_swagger

- `PUT /tableschema/1` Put Data Resource Descriptor to this route.
- `GET /tableschema` Get all Data Resource Descriptors you have posted.
- `GET /swagger` Generate a swagger file from all the Data Resource Descriptors you have submitted.

#### Submit a Data Resource Schema

Once you have your table schema files and swagger API you will need to convert them into a Data Resource Schema.

- `POST /generator` Given a Data Resource Schema, this trigger the generation of all of the described Data Resources.

### Interacting with Generated Data Resources

An interactive API (using Swagger UI) is generated at `/ui`.

The following are the API routes that you can interact with for each of your generated resources (see the docs for more information):

- `GET resource`
- `GET resource/1`
- `POST resource/query`
- `POST resource`
- `PUT resource/1`
- `DELETE resource/1`

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

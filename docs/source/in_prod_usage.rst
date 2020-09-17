.. _in-prod-usage:

In-production Usage Guide
=========================

To use the application in production we recommend deploying it as a Docker image.

However you want to set up, deploy and use your docker environment is up to you. You can use simpler tools such as Docker Swarm or more advanced tools such as Kubernetes (k8s).

Because you are leveraging docker images, deployment to production is greatly streamlined and behaves very similarly to running the application locally with docker-compose.


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

1. To run the application in production mode,

```bash
pipenv run python wsgi.py
```

Or to run in testing mode with flask,

```bash
pipenv run flask run
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

### Storage Manager

The storage manager is responsible for the storage and retrieval of the data resource generation payload from different sources depending on the deployment environment.

- **LOCAL** (Default) - Will store the data resource api schema on the local volume of the deployment. (If you require multiple instance of the same data resource API please use a cloud storage option ex. AWS S3) `export SCHEMA_STORAGE_TYPE=LOCAL`
- **AWS S3** - Will store the data resource api schema within a define bucket and object. `export SCHEMA_STORAGE_TYPE=S3`

```bash
export SCHEMA_STORAGE_TYPE=S3
export AWS_S3_REGION=<aws-region> ex. us-west-1
export AWS_S3_STORAGE_OBJECT_NAME=<object-name> ex. my-schema.json
export AWS_S3_STORAGE_BUCKET_NAME=<bucket-name>
export AWS_ACCESS_KEY_ID =<aws-key-id>
export AWS_SECRET_ACCESS_KEY=<aws-secret>
```

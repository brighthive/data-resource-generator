Architectural design
====================

Overview
--------

Given a configuration file VIA REST the Data Resource Generator (DRG) will dynamically generate:

1. Database tables with relationships

    1. SQLAlchemy Object Relation Mappings (ORM)

    1. Run database migrations

1. RESTful API

    1. Running Flask application

    1. Open API Specification 3.0

The application is built with Python and primarly leverages Flask.

We leverage two core open specifications, Tableschema and Swagger. By embeding these two core documents, a tableschema and swagger definition, along with metadata you have a Data Resource Schema.

The Data Resource Schema is sent embeded inside a Data Resource Generation Payload to the DRG generation route. This triggers the generation of Data Resources.

The application will stand up as a flask API. This API has a generation route that holds a reference to the flask object.

Upon a Data Resource Generation Payload being sent, the application then generates:
- relevant ORM models based on your tableschema document
- relevant REST routes based on your swagger document

Generating ORM and Tables
-------------------------

By leveraging tooling around the tableschema specification we produce a SQLAlchemy ORM. This ORM is used to generate and run the proper DDL commands on the connected database to produce and save the database tables.

This process looks like this:

Database Table Definition Document -> SQLAlchemy ORM -> Database Tables

Generating API Routes
---------------------

By leveraging tooling around the swagger we dynamically produce restful flask routing.

The generation process holds a reference to the flask application. After the application generates the ORM models it will leverage the swagger document as a RESTful route whitelist. By omitting the present of a REST route from your swagger document you can effecitvely disable that RESTful verb route.

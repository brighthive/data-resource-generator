Architectural design
====================

Overview
--------

Given a configuration file VIA REST the Data Resource Generator (DRG) will dynamically generate:

#. Database tables with relationships
    * SQLAlchemy Object Relation Mappings (ORM)
    * Generate and run database migrations
#. RESTful API
    * Running Flask application
    * Open API Specification 3.0

The application is built with Python and primarily leverages Flask.

We leverage two core open specifications, Table Schema and Swagger. By embedding these two core documents, a table schema and swagger definition, along with metadata you have a Data Resource Schema.

The Data Resource Schema is sent embedded inside a Data Resource Generation Payload to the DRG generation route. This triggers the generation of Data Resources.

The application will stand up as a Flask API. This API has a generation route that holds a reference to the Flask object.

Upon a Data Resource Generation Payload being sent, the application then generates:

* relevant ORM models based on your table schema document
* relevant REST routes based on your swagger document

Application Paradigm
--------------------

"Declarative setup - imperative changes."

Upon initialization of your database and API the DRG uses a declarative method. If you wish to introduce changes to that declarative baseline, you are expected to do it imperatively.

Concretely what this means is you will use a configuration file that will generate the required "stuff" to create your database and API. If you want to modify that initial configuration you will have to do so manually. The DRG, as a matter of principal, does not support migrations and modifications as such.

The DRG, on startup, deterministically expects a specific state of your database tables based on the provided configuration file. Therefore, you will need to update the state of your database to match the state present in your new configuration file.

Generating ORM and Tables
-------------------------

By leveraging tooling around the table schema specification we produce a SQLAlchemy ORM. This ORM is used to generate and run the proper DDL commands on the connected database to produce and save the database tables.

This process looks like this:

Database Table Definition Document -> SQLAlchemy ORM -> Database Tables

Generating API Routes
---------------------

By leveraging tooling around the swagger we dynamically produce restful Flask routing.

The generation process holds a reference to the Flask application. After the application generates the ORM models it will leverage the swagger document as a RESTful route whitelist. By omitting the present of a REST route from your swagger document you can effectively disable that RESTful verb route.

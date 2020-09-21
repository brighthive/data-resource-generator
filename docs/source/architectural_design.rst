.. _drg-arch:

Architectural design
====================

Overview
--------

BrightHive built the DRG with Python and several other libraries. These include:

Table Schema and Swagger. These open data specifications provide the backbone of a Data Resource Schema, which embeds table schema, descriptors, a swagger specification, and metadata.
Flask. The DRG application itself is a Flask API. The API has a generation route that holds a reference to the Flask object.

Application Paradigm
--------------------

*Declarative setup - imperative changes.*

Upon initialization of your database and API the DRG uses a declarative method. If you wish to introduce changes to that declarative baseline, you are expected to do it imperatively.

What does this mean? You use a configuration file to generate the required "stuff" to create a database and API. If you want to modify the initial configuration, then you have to do so manually. The DRG, as a matter of principal, does not support migrations and modifications as such.

The DRG, on startup, deterministically expects a specific state of your database tables based on the provided configuration file. Therefore, you will need to update the state of your database to match the state present in your new configuration file.

Generating ORM and Tables
-------------------------

The DRG produces a SQLAlchemy ORM. This ORM is used to generate and run the proper DDL commands on the connected database to produce and save the database tables.

To elaborate, the DRG takes a configuration file that defines the structure of a database. The DRG converts this document into SQLAlchemy ORM. Then SQLAlchemy generates the Data Definition Language (DDL) commands required by the database to create the given structure. The DDL commands are issued and the required components are created in the database (tables, sequences. Dynamically created database and ORM!

Generating API Routes
---------------------

By leveraging tooling around the swagger we dynamically produce restful Flask routing.

The generation process holds a reference to the Flask application. After the application generates the ORM models it will leverage the swagger document as a RESTful route whitelist. By omitting the present of a REST route from your swagger document you can effectively disable that RESTful verb route.

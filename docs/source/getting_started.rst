Getting Started
===============

The Data Resource Generator (DRG) is a database and API as configuration application.

Definitions
-----------

Data Resource
    An entity that stores and handles data. In the context of the BrightHive DRG, a Data Resource is a relational database with a RESTful API.

**Data Resources** are a core element of Data Trusts and may be loosely defined as *data that is owned by or stewarded over by members of Data Trusts.*

From the technical perspective, a BrightHive Data Resource is an entity comprised of the following elements:

- **Data Model** - The data model consists of one or more database tables and associated Object Relational Mapping (ORM) objects for communicating with these tables.
- **RESTful API** - Data managed by Data Resources are accessed via RESTful API endpoints. These endpoints support standard operations (i.e. **GET**, **POST**, **PUT**, **PATCH**, **DELETE**).
- **Data Resource Schemas** - Data Resource Schemas are JSON documents that define the data model, API endpoints, and security constraints placed on the specific Data Resource. These schemas are what allow for new Data Resources to be created without new code being written.


Data Resource Descriptor: BrightHive specification. Includes an API definition and a tableschema to describe the database. Please see [BrightHive Data Resource API](https://github.com/brighthive/data-resource-api).

Data Resource Schema: BrightHive specification. JSONLD document. Please see [specification in progress](example.com) for more information.

Data Resource Generation Payload: This is simply the JSON body that includes a nested Data Resource Schema that is used to generate the application. Additional properties can be included as top level keys to affect generation in a number of ways.


Data Resource Schema
    A file that defines the database and API specs.

Steps to Standup a DRG
----------------------

You can easily standup a DRG in four easy steps!

#. Create a Data Resource Schema :ref:`basic usage<basic-usage>`
#. Run the Data Resource Generator :ref:`basic usage<basic-usage>` and :ref:`running the application<in-prod-usage>`
#. Generate your Data Resources :ref:`basic usage<basic-usage>`
#. Interact with your generated Data Resources :ref:`basic usage<basic-usage>`

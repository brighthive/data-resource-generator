Getting Started
===============

The Data Resource Generator (DRG) is a database and API as configuration application.

Definitions
-----------

Data Trust
    Legal, technical, and governance frameworks that enable networks of organizations to securely and responsibly share and collaborate with data, generating new insights and increasing their combined impact.

Data Resource
    Loosely defined as data that is owned by or stewarded over by members of Data Trusts. These are core elements of a Data Trust. In the context of the DRG, a Data Resource is a relational database with a RESTful API. 

From the technical perspective, a BrightHive Data Resource is an entity comprised of the following elements:

Data Model
    The data model consists of one or more database tables and associated Object Relational Mapping (ORM) objects for communicating with these tables.

RESTful API
    Data managed by Data Resources are accessed via RESTful API endpoints. These endpoints support standard operations (i.e. **GET**, **POST**, **PUT**, **PATCH**, **DELETE**).

Data Resource Schema
    A JSON document (Loosely a JSON-LD document) that defines the data models, API endpoints, and security constraints placed on the specific Data Resources. In conjunction with the DRG, these schemas are what allow for new Data Resources to be created without the need for code to be written.

To generate Data Resources you will construct the following:

Data Resource Generation Payload
    This is simply a JSON body that includes a nested Data Resource Schema that is used to generate the application. Additional properties can be included as top level keys to affect generation process in a number of ways.

Steps to Standup a DRG
----------------------

You can easily standup a DRG in four easy steps!

#. Create a Data Resource Schema :ref:`basic usage<basic-usage>`
#. Run the Data Resource Generator :ref:`basic usage<basic-usage>` and :ref:`running the application<in-prod-usage>`
#. Generate your Data Resources :ref:`basic usage<basic-usage>`
#. Interact with your generated Data Resources :ref:`basic usage<basic-usage>`

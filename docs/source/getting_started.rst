Getting Started
===============

The Data Resource Generator (DRG) helps you easily configure and create a RESTful API supported by a relational database without writing any code. In other words, it is a database and API as configuration.

The DRG comes to life when a user or client sends a Data Resource Schema, embedded inside a Data Resource Generation Payload, to the DRG generation route. Upon receiving a Data Resource Generation Payload, the application then generates:

* Relevant ORM models based on your table schema document
* Relevant REST routes based on your swagger document

Definitions
-----------

Data Trust
    Legal, technical, and governance frameworks that enable networks of organizations to securely and responsibly share and collaborate with data, generating new insights and increasing their combined impact.

Data Resource
    The core element of a BrightHive Data Trust. Members of a Data Trust can own, manage, or oversee data resources. In the context of the DRG, a Data Resource is a relational database with a RESTful API.

**From the technical perspective, a BrightHive Data Resource is an entity comprised of the following elements:**

RESTful API
    Data managed by Data Resources are accessed via RESTful API endpoints. These endpoints support standard operations (i.e. **GET**, **POST**, **PUT**, **PATCH**, **DELETE**).

Data Resource Schema
    A JSON document (loosely a JSON-LD document) that defines the data models, API endpoints, and security constraints placed on the specific Data Resources. In conjunction with the DRG, these schemas are what allow for new Data Resources to be created without the need for code to be written.

Data Resource Generation Payload
    A JSON body that includes a nested "Data Resource Schema" (see above) used to generate the application. Additional properties can be included as top level keys to affect generation process in a number of ways.

Next Steps
----------

Are you ready to stand up a Data Resource Generator? Then, read :ref:`step-by-step instructions for running and using the DRG <step-by-step-instr>`. Otherwise, learn more about :ref:`DRG use cases <use-cases>` and the :ref:`DRG Architecture <drg-arch>`.

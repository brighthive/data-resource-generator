.. _basic-usage:

Basic Usage
===========

.. note::
    In production mode all routes will be secured by default. This means you will need to configure an OAUTH provider in the config.

Utilities to help create a Data Resource Schema
-----------------------------------------------

The DRG is coupled with a few helpful routes to aid you in generating your Data Resource Schema. These routes are automatically running when the application starts.

Provided is a utility that takes tables schema definitions of tables and generates swagger specification using https://github.com/brighthive/convert_descriptor_to_swagger

* **PUT /tableschema/1** - PUT your table schema descriptor to this route. When the generation runs it will use all submitted table schemas so make sure you PUT to different numbers at the end of the URI or you will overwrite your previously submitted table schema.
* **GET /tableschema** - Displays all of the table schemas that have been PUT via the route above.
* **GET /swagger** - Trigger the swagger generation based on all of the table schemas that have been PUT via the route above.

Generating Data Resources
-------------------------

In order to generate Data Resources you will need to submit a Data Resource Generation Payload. This consists simply of a JSON file with a nested Data Resource Schema and other top level keys that can affect the generation process (i.e., do not run validation).

Once you have your collection of table schema descriptors and swagger specification you will need to convert them into a Data Resource Schema and nest them inside the Data Resource Generation Payload. Nest the Data Resource Schema under a top-level key with the value:

.. code-block:: JSON
    :caption: Data Resource Generation Payload
    :emphasize-lines: 2

    {
        "data_resource_schema": {}
    }

The Data Resource Schema consists of your table schema descriptors and swagger specification along with additional metadata. Currently there is not a utility to help you automatically generate these so this needs to be done manually.

Please see :ref:`data resource schema reference<data-resource-schema>` for more information on creating your Data Resource Schema.

* **POST /generator** - Given a Data Resource Generation Payload (and thus a nested Data Resource Schema), this trigger the generation of all of the described Data Resources.

See `starting the application <starting-the-app>`_ for more information.

Interacting with Generated Data Resources
-----------------------------------------

An interactive API (using Swagger UI) is generated at **/ui**.

The following are the API routes that you can interact with for each of your generated resources (see the docs for more information):

* **GET resource**
* **GET resource/1**
* **POST resource/query**
* **POST resource**
* **PUT resource/1**
* **DELETE resource/1**

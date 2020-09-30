.. _basic-usage:

Creating and Using a Data Resource Schema
=========================================

.. note::
    In production mode all routes will be secured by default. This means you will need to configure an OAUTH provider in the config.

.. _data-resource-schema:

Data Resource Schema Reference
------------------------------

.. note::
    This reference is a stub and is intended to be expanded on.

Data Resource Generator uses `tableschema <https://specs.frictionlessdata.io/table-schema/>`_ to define its tables. It takes this information and generates the required database tables.

Examples can be found in the Data Resource Generator repository test section.

Utilities to help create a Data Resource Schema
-----------------------------------------------

The DRG is coupled with a few helpful routes to aid you in generating your Data Resource Schema. These routes are automatically running when the application starts.

Provided is a utility that takes tables schema definitions of tables and generates swagger specification using https://github.com/brighthive/convert_descriptor_to_swagger

* **PUT /tableschema/1** - PUT your table schema descriptor to this route. When the generation runs it will use all submitted table schemas so make sure you PUT to different numbers at the end of the URI or you will overwrite your previously submitted table schema.
* **GET /tableschema** - Displays all of the table schemas that have been PUT via the route above.
* **GET /swagger** - Trigger the swagger generation based on all of the table schemas that have been PUT via the route above.

.. _generating-data-resources:

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

See :ref:`starting the application <starting-the-app>` for more information.

See :ref:`interacting with generated Data Resources <interacting-with-generated-routes>` to learn how to interact with the Data Resources once they are generated.

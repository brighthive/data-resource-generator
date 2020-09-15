Configuration
=============

Application / System Configuration
----------------------------------

This section covers configuration that is needed to run or start the application on your system.

Configuration occurs with the ConfigFactory.

Given an environmental variable for APP_ENV (default TEST) the application will select specific variables.

These variables are mostly for connecting to the database in different environments. However, if your deployment is unique you can extend the config factory to include the variables you need.

Database and API configuration
------------------------------

Data Resource Generator uses `tableschema <https://specs.frictionlessdata.io/table-schema/>`_ and `Open API Spec 3.0 <https://swagger.io/specification/>`_ as the basis for database and API configuration.

You will need to create a Data Resource Schema that defines your tables in table schema and your API in Open API 3.0.

The Data Resource Generator repository includes a JSONSchema document that defines the requirements for a Data Resource Schema.

Database Configuration
^^^^^^^^^^^^^^^^^^^^^^

Data Resource Generator uses `tableschema <https://specs.frictionlessdata.io/table-schema/>`_ to define its tables. It takes this information and generates the required database tables.

Examples can be found in the Data Resource Generator repository test section.

API Configuration
^^^^^^^^^^^^^^^^^

A swagger file is used to configure the API. Only HTTP verbs present under routes will be enabled.

Because of this it also means that the three main routes for each resource,

* GET ALL
* GET ID
* POST QUERY

If these paths are not included in the swagger spec then they will not be added to the API routing. See `Routes -> Enabling and disabling routes` for more information.

Examples can be found in the Data Resource Generator repository test section.

Configuration
=============

There are two types of configurations: Application or system configurations that are used to run the Data Resource Generator and the configuration files that define the database and API.

Application configurations are required at initialization and are generally passed through environmental variables and may require that you change the configuration python file and build your own docker image.

Once the application is running you will pass the database and API configurations via an HTTP API. This was a core motivation for the Data Resource Generator as it facilitates automation.

Application / System Configuration
----------------------------------

This section covers configuration that is needed to run or start the application on your system.

Configuration occurs with the ConfigFactory.

Given an environmental variable for APP_ENV (default TEST) the application will select specific variables.

These variables are mostly for connecting to the database in different environments. However, if your deployment is unique you can extend the config factory to include the variables you need.

Database and API configuration
------------------------------

Data Resource Generator uses `table schema <https://specs.frictionlessdata.io/table-schema/>`_ and `Open API Spec 3.0 <https://swagger.io/specification/>`_ as the basis for database and API configuration. You will create two documents and embed them with additional metadata into a Data Resource Schema.

The Data Resource Generator repository includes a JSONSchema document that defines the requirements for a Data Resource Schema. JSONSchema defines the required schema for a document. When you submit your Data Resource Schema to the generator it will be validated against that JSONSchema document.

Database Configuration
^^^^^^^^^^^^^^^^^^^^^^

You will use `frictionless table schema <https://specs.frictionlessdata.io/table-schema/>`_. You will define your tables and relationships using table schema.

Please see :ref:`Data Resource Schema<data-resource-schema>` for more information.

API Configuration
^^^^^^^^^^^^^^^^^

A swagger file is used to configure the API. Only HTTP verbs present under routes will be enabled.

Because of this it also means that the three main routes for each resource,

* GET ALL
* GET ID
* POST QUERY

If these paths are not included in the swagger spec then they will not be added to the API routing. See `Routes -> Enabling and disabling routes` for more information.

Examples can be found in the Data Resource Generator repository test section.

Your swagger file will be embedded within the Data Resource Schema.

Please see :ref:`Data Resource Schema<data-resource-schema>` for more information.
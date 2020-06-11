Configuration
=============

Application Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

Configuration occurs with the ConfigFactory.

Given an environmental variable for APP_ENV (default TEST) the application will select specific variables.

These variables are mostly for connecting to the database in different environments. However, if your deployment is unique you can extend the config factory to include the variables you need.

Database Configuration
^^^^^^^^^^^^^^^^^^^^^^

Data Resource Generator uses table schema as the basis for database configuration.

API Configuration
^^^^^^^^^^^^^^^^^

A swagger file is used to configure the API. Only HTTP verbs present under routes will be enabled.

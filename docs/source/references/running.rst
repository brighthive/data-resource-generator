.. _running-the-app:

Successfully Running the DRG
============================

Steps to Use the DRG
--------------------

.. _step-by-step-instr:

You can easily standup a DRG in four easy steps!

#. Create a Data Resource Schema -- see :ref:`basic usage<basic-usage>`
#. Run the Data Resource Generator -- see :ref:`basic usage<basic-usage>` and :ref:`running the application<in-prod-usage>`
#. Generate your Data Resources -- see :ref:`basic usage<basic-usage>`
#. Interact with your generated Data Resources -- see :ref:`basic usage<basic-usage>`

Running the application
-----------------------

Running with Docker is the preferred method. We recommend using docker-compose locally to run the application and using more advanced docker deployment tools such as Docker Swarm or k8s, depending on your needs. Advanced deployment is outside of the scope of this documentation however. Please see `in-production usage <in-prod-usage>`_ for more information.

Running Locally with Docker Compose
'''''''''''''''''''''''''''''''''''

To run locally via Docker Compose:

#. First build the docker image:

.. code-block:: bash

    docker build -t brighthive/data-resource-generator .

#. Then run the docker-compose.yml file (which will run brighthive/data-resource-generator:latest) with:

.. code-block:: bash

    docker-compose up

Running Locally with Python
'''''''''''''''''''''''''''

This method is sometimes useful for doing development work.

1. Restart the database to clear the data.

.. code-block:: bash

    docker-compose -f test-database-docker-compose.yml down && docker-compose -f test-database-docker-compose.yml up -d

1. To run the application in production mode,

.. code-block:: bash

    pipenv run python wsgi.py

Or to run in testing mode with flask,

.. code-block:: bash

    pipenv run flask run

.. _starting-the-app:

Starting the application
------------------------

There are two ways to run the application. With an empty database or an already existing database.

Generation Validation
'''''''''''''''''''''

Note that when the Data Resource Schema is submitted to the generation API the DRG will run validation against it and not build if the validation fails. If you wish to skip the validation process add a top level key "ignore_validation" as follows:

.. code-block:: JSON
    :caption: Data Resource Generation Payload
    :emphasize-lines: 2

    {
        "data_resource_schema": {},
        "ignore_validation": null
    }

.. warning::
    The value of "ignore_validation" will not be examined. The DRG is simply looking for the existence of the top level key "ignore_validation". Putting { "ignore_validation": False } will still trigger the validation to occur.

Empty database
''''''''''''''

In the case you want to generate a database, you will run the application with an empty database.

Making a call to the generation route will trigger the building of ORM, API, and modify the database.

Non-empty database
''''''''''''''''''

In the event your database is not empty, the generation process has already occurred and you have made changes to the Data Resource Schema then the DRG will not generate any database migrations. The DRG will expect you to POST a Data Resource Schema that matches the content of the database. An error will occur if the DRG attempts touch the database. Therefore you will need to add a top level key to the Data Resource Generation Payload to prevent running the generated DDL.

.. code-block:: JSON
    :caption: Data Resource Generation Payload
    :emphasize-lines: 2

    {
        "data_resource_schema": {},
        "touch_database": false
    }

This will allow the DRG to set itself up and assuming the state of the database is as described in the Data Resource Schema then the models and APIs will be built successfully.

Restarting the application
--------------------------

Restarting of the application is supported. In the event that your application has applied migrations to the database you simply need to ensure you have a saved data_resource_generation_payload.json file in the static folder.

On startup the application will attempt to load the ORM and API based on the data resource schema file. In this mode, the application will not apply any modifications to the database. You must ensure that the state of your database matches the state the data resource schema expects.

In other words, you cannot modify the data resource schema after running the generation and expect the application to handle the migrations.

Making changes to your database and API
---------------------------------------

In the event you require modifications to your database and API, this is supported by ensuring the state of your database matches the state that the data resource schema expects.

You must manually run migrations to your database and manually update your data resource schema. Then upon running the application, it will build the ORM and API deterministically and use the database expecting it to be in the correct state.

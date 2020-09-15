Running
=======

Starting the application
------------------------

There are two ways to run the application. With an empty database or an already existing database.

Empty database
^^^^^^^^^^^^^^

In the case you want to generate a database, you will run the application with an empty database.

Making a call to the generate route will trigger the building of ORM, API, and modify the database.

Non-empty database
^^^^^^^^^^^^^^^^^^

This application was not designed to be run on top of a database that already has tables in it (in other words, you can only run the generation process once). If you run the application in this mode it is expected that you have already gone through the generation process and have or intend to modify the database and/or API.

Restarting the application
--------------------------

Restarting of the application is supported. In the event that your application has applied migrations to the database you simply need to ensure you have a saved data_resource_generation_payload.json file in the static folder.

On startup the application will attempt to load the ORM and API based on the data resource schema file. In this mode, the application will not apply any modifications to the database. You must ensure that the state of your database matches the state the data resource schema expects.

In other words, you cannot modify the data resource schema after running the generation and expect the application to handle the migrations.

Making changes to your database and API
---------------------------------------

In the event you require modifications to your database and API, this is supported by ensuring the state of your database matches the state that the data resource schema expects.

You must manually run migrations to your database and manually update your data resource schema. Then upon running the application, it will build the ORM and API deterministically and use the database expecting it to be in the correct state.

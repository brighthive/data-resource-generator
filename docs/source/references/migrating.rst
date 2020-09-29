.. _migrating:

Migrating a live database
=========================

Once you have generated a set of Data Resources the database of the application will be modified. The application can only modify the database when it is working with a completely blank database.

If you want to modify your database and application there is a work around.

Please note! The DRG does not offer a universal database migration engine. Such a solution does not fit the needs or scope of BrightHive. Using a declarative setup and imperative changes accommodate the majority of potential use cases.

Modifying Generated Data Resources
-------------------------------------------------

You will need to manually migrate the database to match the state that the application expects based on your updates.

Additionally you will need to update your Data Resource Schema.

#. Modify Data Resource Schema

#. Tear down DRG

#. Manually migrate DB

#. Stand up DRG

#. Load application with DRG or run generation with the "touch_database: false" key.

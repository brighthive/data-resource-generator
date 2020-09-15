Migrating a live database
=========================

Once you have generated a set of Data Resources the database of the application will be modified.
The application can only modify the database when it is working with a completely blank database.
If you want to modify your database and applicaiton there is a work around.

Why
---

The original Data Resource API had the ability to dynamically update and modify the database as
you modified the declarative descriptor files. This led to a number of problems such as putting
the application and database into states where a human needs to intervene. A universal magical
database migration engine was not in scope for the project.

The lessons learned from that are a declarative setup and imperative modifications provided the
for the majority of use cases.

So how do I modified my generated Data Resources?
-------------------------------------------------

You will need to manually migrate the database to match the state that the application expects based on your updates.

Additionally you will need to update your Data Resource Schema.

1. Modify Data Resource Schema

2. Tear down DRG

3. Manually migrate DB

4. Stand up DRG

5. Load application with DRG or run generation with the "touch_database: false" key.

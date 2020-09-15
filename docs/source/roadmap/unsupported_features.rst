Roadmap
=======

Unsupported Features
--------------------

There are a number of features that will probably work out of the box but are not explicitly supported.

These features may or may not work. If they do work it is because of the use of the underlying libraries (SQLAlchemy, Tableschema-sql-py, Flask, etc.) however we have not set out to explicitly support these features. As a result we do not have a set of tests around these features and you may use at your own discretion (or contribute to get them working!).

Known Unsupported Features
^^^^^^^^^^^^^^^^^^^^^^^^^^

These features are known not to work and are not officially supported.

* Many to many relationships where either of the tables have a primary key named something other than 'id'.
* Tables with a primary key that is something other than 'id'.

Unknown Unsupported Features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These features may or may not work but are not officially supported.

* Tables with two or more primary keys

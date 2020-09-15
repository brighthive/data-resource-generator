What is unsupported
===================

There are a number of features that will probably work out of the box but are not explicilty supported.
These features may or may not work. If they do work it is because of the use of the underlying libraries (SQLAlchemy, Tableschema-sql-py, Flask, etc.) however
we have not set out to explicilty support these features. As a result we do not have a set of tests
around these features and you may use at your own discresion (or contribute to get them working!).


Features that may work but are not "officially" supported
----------------------------------------------------------------------

- Tables with two or more primary keys


Features that are known not to be supported
-------------------------------------------

- Many to many relationships where either of the tables have a primary key named something other than 'id'.
- Tables with a primary key that is something other than 'id'.

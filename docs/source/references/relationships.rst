Relationships
-------------

Relationships must be explicitly defined in the Data Resource Schema document.

Supported relationships
^^^^^^^^^^^^^^^^^^^^^^^

The following list of relationships are supported:

* One to Many (not self join)
* Many to Many

The following are not currently supported:

* One to Many (self join)

One to Many support
'''''''''''''''''''

You may define one to many relationships using tables schema foreign key in the Data Resource Schema document. Please see `tableschema's foreign key documentation <https://specs.frictionlessdata.io/table-schema/#foreign-keys>`_ for more information.

Once defined you may access the relationship as a field on your resource.

Standard relational database referential integrity still applies: If you reference a resource it must already exist or else the application will return an error.

Many to Many support
''''''''''''''''''''

There are limitations to many to many support:

* Both tables must contain a single primary key that is an integer.

The application will handle creating an association table.

An error will return if either the primary key IDs provided for the parent and children fail to resolve to existing data in the database.

In order for many to many to work both primary keys of the tables in the relationship need to "id".
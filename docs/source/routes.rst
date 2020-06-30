Routes
======

This section will cover the generated routes for the Data Resources and how to interact with them.
--------------------------------------------------------------------------------------------------

For each table schema you provide the following routes will be generated. There are two types of API routes:
- Resource routes
- Relationship based routes

Resource routes are the typical RESTful API routes that you might expect. Relationship based routes are simply the way you handle many to many relationships for resources.

Resource Routing
^^^^^^^^^^^^^^^^

Get Data
""""""""

- `GET /resource`

This will query for all resources and provide paging table links.

- `GET /resource/1`

This will allow you to query items by ID.

- `POST /resource/query`

This will allow you to search for all items in a resource that match the provided fields.

Insert / Update data
""""""""""""""""""""

- `POST /resource`

This will create a new resource. If there are any required fields that you did not provide then it will return an error.

- `PUT /resource/1`

Put will create a new resource if there does not exist a resource at the URI.

Deleting data
"""""""""""""

`DELETE` is intentionally not implemented. There are a number of unanswered questions around what it means to actually "delete" data from the trust and what implications that may have from a legal or governance standpoint.

- `DELETE resource/1`

The delete route exists but will return an unimplemented error.

Relationship Routing
^^^^^^^^^^^^^^^^^^^^

Relationships must be explicitly defined in the Data Resource Schema document.

Currently there are shortcuts being taken that limit the support of this many to many. Both tables must contain a single primary key that is an integer. The application will handle creating an association table.

An error will return if either the primary key IDs provided for the parent and children fail to resolve to existing data in the database.

Get Relationships
"""""""""""""""""

- `GET /parent/id/child`

This will return a list of primary keys, as integers.

Set Relationships
"""""""""""""""""

- `PUT /parent/id/child`

Performing a PUT will replace the entire many to many association with your provided list. If you supply an empty list then it will act as a delete.

- `PATCH /parent/id/child`

Performing a PATCH will add the provided list of primary keys to the relationship.

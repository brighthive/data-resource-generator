Routes
======

Generated Routes and how to interact with them
----------------------------------------------

For each table schema you provide the following routes will be generated. There are two types of API routes:
* Resource routes
* Relationship based routes

Resource routes are the typical RESTful API routes that you might expect. Relationship based routes are simply the way you handle many to many relationships for resources.

Resource Routing
^^^^^^^^^^^^^^^^

Get Data
""""""""

* `GET /resource`

This will query for all resources and provide paging table links.

* `GET /resource/1`

This will allow you to query items by ID.

* `POST /resource/query`

This will allow you to search for all items in a resource that match the provided fields.

Insert / Update data
""""""""""""""""""""

* `POST /resource`

This will create a new resource. If there are any required fields that you did not provide then it will return an error.

* `PUT /resource/1`

Put will create a new resource if there does not exist a resource at the URI.

Deleting data
"""""""""""""

`DELETE` is intentionally not implemented. There are a number of unanswered questions around what it means to actually "delete" data from the trust and what implications that may have from a legal or governance standpoint.

* `DELETE /resource/1`

The delete route exists but will return an unimplemented error.

Relationship Routing
^^^^^^^^^^^^^^^^^^^^

Get Relationships
"""""""""""""""""

* `GET /parent/id/child`

This will return a list of primary keys, as integers.

Set Relationships
"""""""""""""""""

* `PUT /parent/id/child`

Performing a PUT will replace the entire many to many association with your provided list. If you supply an empty list then it will act as a delete.

* `PATCH /parent/id/child`

Performing a PATCH will add the provided list of primary keys to the relationship.

Enabling and disabling routes
------------------------------

To enable a route, include the route in your swagger API document.

To disable a route, do not include the route in your swagger API document.

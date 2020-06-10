Routes
======

This section will cover the generated routes for the Data Resources and how to interact with them.
--------------------------------------------------------------------------------------------------

For each table schema you provide the following routes will be generated. In later versions of the Data Resource Generator many-to-many routes will also be available.

Getting data
^^^^^^^^^^^^

- `GET resource`

This will query for all resources and provide paging table links.

- `GET resource/1`

This will allow you to query items by ID.

- `POST resource/query`

This will allow you to search for all items in a resource that match the provided fields.

Inserting data
^^^^^^^^^^^^^^

- `POST resource`

This will create a new resource. If there are any required fields that you did not provide then it will return an error.

Updating data
^^^^^^^^^^^^^

- `PUT resource/1`

Put will create a new resource if there does not exist a resource at the URI.

Deleting data
^^^^^^^^^^^^^

`DELETE` is intentionally not implemented. There are a number of unanswered questions around what it means to actually "delete" data from the trust and what implications that may have from a legal or governance standpoint.

- `DELETE resource/1`

The delete route exists but will return an unimplemented error.

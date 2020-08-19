from data_resource.shared_utils.log_factory import LogFactory


logger = LogFactory.get_console_logger("generator:resource-delete")


class ResourceDelete:
    def delete_one(self, id, data_resource):
        """Delete a single object from the data model based on it's primary
        key.

        Args:
            id (any): The primary key for the specific object.
            data_resource (object): SQLAlchemy ORM model.

        Return:
            dict, int: The response object and the HTTP status code.
        """
        pass

from data_resource.shared_utils.log_factory import LogFactory


logger = LogFactory.get_console_logger("generator:resource-delete")


class ResourceDelete:
    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def delete_one_secure(self, id, data_resource):
        """Wrapper method for delete one method.

        Args:
            id (any): The primary key for the specific object.
            data_model (object): SQLAlchemy ORM model.
            data_resource_name (str): Name of the data resource.
            table_schema (dict): The Table Schema object to use for validation.

        Return:
            function: The wrapped method.
        """
        return self.delete_one(id, data_resource)

    def delete_one(self, id, data_resource):
        """Delete a single object from the data model based on it's primary
        key.

        Args:
            id (any): The primary key for the specific object.
            data_model (object): SQLAlchemy ORM model.
            data_resource_name (str): Name of the data resource.
            table_schema (dict): The Table Schema object to use for validation.

        Return:
            dict, int: The response object and the HTTP status code.
        """
        # resource = (
        #     db_session.query(resource_orm).filter(resource_orm.id == id).one_or_none()
        # )
        # if resource is not None:
        #     logging.info("Deleting resource %s..", id)
        #     db_session.query(resource_orm).filter(resource_orm.id == id).delete()
        #     db_session.commit()
        #     return NoContent, 204
        # else:
        #     return NoContent, 404
        pass

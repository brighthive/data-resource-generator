# from tableschema import Schema, validate
from data_resource.db.base import db_session
from data_resource.generator.api_manager.v1_0_0.crud_functions.resource_create import (
    ResourceCreate,
)
from data_resource.shared_utils.api_exceptions import ApiError, ApiUnhandledError
from data_resource.shared_utils.log_factory import LogFactory


logger = LogFactory.get_console_logger("generator:resource-update")


class ResourceUpdate:
    def update_one(
        self, id=1, resource_name=None, resource_orm=None, request=None, mode="PUT"
    ):
        """Update a single object from the data model based on it's primary
        key.

        Args:
            id (int): PK ID of resource,
            resource_name (str): =None,
            resource_orm (SQLAlchemy ORM):
            request (Flask request?): =None,
            mode (str): Tells the function if this is a PUT or PATCH

        Return:
            dict, int: The response object and the HTTP status code.
        """
        try:
            request_obj = request.json
        except Exception:
            raise ApiError("No request body found.", 400)

        primary_key = "id"
        data_obj = (
            db_session.query(resource_orm)
            .filter(getattr(resource_orm, primary_key) == id)
            .first()
        )

        if mode == "PATCH" and data_obj is None:
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        if data_obj is None:
            return ResourceCreate().insert_one(
                resource_orm=resource_orm, request=request
            )

        try:
            for key, value in request_obj.items():
                setattr(data_obj, key, value)
            db_session.commit()
        except:
            raise ApiError("Failed to modify resource.")

        id_value = data_obj.id

        return {"message": "Successfully updated resource.", "id": id_value}, 200

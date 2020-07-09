from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_links,
    build_json_from_object,
)
from collections import OrderedDict
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import InternalServerError, ApiError
from data_resource.shared_utils import LogFactory


logger = LogFactory.get_console_logger("generator:resource-read")


class ResourceRead:
    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def get_all_secure(
    #     self, *args, **kwargs
    # ):
    #     # """Wrapper method for get_all method.

    #     # Return:
    #     #     function: The wrapped method.
    #     # """
    #     return self.get_all(
    #         *args, **kwargs
    #     )

    def get_all(
        self,
        resource_name: str = "resource",
        resource_orm: object = None,
        offset: int = 0,
        limit: int = 10,
    ):
        """Retrieve a paginated list of items.

        Args:
            resource_name (str): Name of the data resource.
            resource_orm (object): SQLAlchemy ORM model.
            offset (int): Pagination offset.
            limit (int): Result limit.

        Return:
            dict, int: The response object and associated HTTP status code.
        """
        response = OrderedDict()
        response[resource_name] = []
        restricted_fields = {}  # TODO
        response["links"] = []
        links = []

        try:
            results = db_session.query(resource_orm).limit(limit).offset(offset).all()
            for row in results:
                response[resource_name].append(
                    build_json_from_object(row, restricted_fields)
                )
            row_count = db_session.query(resource_orm).count()
            if row_count > 0:
                links = build_links(resource_name, offset, limit, row_count)
            response["links"] = links
        except Exception:
            db_session.rollback()
            raise InternalServerError()

        return response, 200

    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def get_one_secure(self, *args, **kwargs):
    #     # """Wrapper method for get one method.

    #     # Return:
    #     #     function: The wrapped method.
    #     # """
    #     return self.get_one(*args, **kwargs)

    def get_one(
        self,
        resource_name: str = "resource",
        resource_orm: object = None,
        id: int = None,
    ):
        """Retrieve a single object from the data model based on it's primary
        key.

        Args:
            resource_name (str): Name of the data resource.
            resource_orm (object): SQLAlchemy ORM model.
            offset (int): Pagination offset.
            limit (int): Result limit.

        Return:
            dict, int: The response object and the HTTP status code.
        """
        try:
            # primary_key = table_schema["primaryKey"] # TODO
            primary_key = "id"
            result = (
                db_session.query(resource_orm)
                .filter(getattr(resource_orm, primary_key) == id)
                .first()
            )
        except Exception:
            db_session.rollback()
            raise InternalServerError()

        if result is None:
            db_session.rollback()
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        response = build_json_from_object(result)
        return response, 200

from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_links,
    build_json_from_object,
)
from collections import OrderedDict
from data_resource.db.base import db_session
import flask
import logging


def InternalServerError(*args, **kwarg):
    return


class ResourceGet:
    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def get_all_secure(
        self, data_model, data_resource_name, restricted_fields, offset=0, limit=1
    ):
        # """Wrapper method for get_all method.

        # Args:
        #     data_model (object): SQLAlchemy ORM model.
        #     data_resource_name (str): Name of the data resource.
        #     offset (int): Pagination offset.
        #     limit (int): Result limit.

        # Return:
        #     function: The wrapped method.
        # """
        return self.get_all(
            data_model, data_resource_name, restricted_fields, offset, limit
        )

    def get_all(
        self,
        resource_name="resource",
        resource_orm=None,
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
        restricted_fields = {}  # FIX
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
            # raise InternalServerError()
            raise

        return response, 200

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def get_one_secure(self, id, data_model, data_resource_name, table_schema):
        # """Wrapper method for get one method.

        # Args:
        #     id (any): The primary key for the specific object.
        #     data_model (object): SQLAlchemy ORM model.
        #     data_resource_name (str): Name of the data resource.
        #     table_schema (dict): The Table Schema object to use for validation.

        # Return:
        #     function: The wrapped method.
        # """
        return self.get_one(id, data_model, data_resource_name, table_schema)

    def get_one(self, resource_name="resource", resource_orm=None, id: int = None):
        # """Retrieve a single object from the data model based on it's primary
        # key.

        # Args:
        #     id (any): The primary key for the specific object.
        #     data_model (object): SQLAlchemy ORM model.
        #     data_resource_name (str): Name of the data resource.
        #     table_schema (dict): The Table Schema object to use for validation.

        # Return:
        #     dict, int: The response object and the HTTP status code.
        # """
        try:
            # primary_key = table_schema["primaryKey"]
            primary_key = "id"
            result = (
                db_session.query(resource_orm)
                .filter(getattr(resource_orm, primary_key) == id)
                .first()
            )
            if result is None:
                return {"error": f"Resource with id '{id}' not found."}, 404

            response = build_json_from_object(result)
            return response, 200
        except Exception:
            # raise ApiUnhandledError(f"Resource with id '{id}' not found.", 404)
            raise

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def get_many_one_secure(self, id: int, parent: str, child: str):
        # """Wrapper method for get many method.

        # Args:
        #     id (int): Given ID of type parent
        #     parent (str): Type of parent
        #     child (str): Type of child

        # Return:
        #     function: The wrapped method.
        # """
        return self.get_many_one(id, parent, child)

    def get_many_one(self, id: int, parent: str, child: str):
        # """Retrieve the many to many relationship data of a parent and child.

        # Args:
        #     id (int): Given ID of type parent
        #     parent (str): Type of parent
        #     child (str): Type of child
        # """
        join_table = JuncHolder.lookup_table(parent, child)

        # This should not be reachable
        # if join_table is None:
        # return {'error': f"relationship '{child}' of '{parent}' not found."}
        try:
            session = Session()
            parent_col_str = f"{parent}_id"
            child_col_str = f"{child}_id"

            cols = {parent_col_str: id}
            query = session.query(join_table).filter_by(**cols).all()

            children = []
            for row in query:
                # example - {'programs_id': 2, 'credentials_id': 3}
                row_dict = row._asdict()
                children.append(row_dict[child_col_str])

        except Exception:
            raise InternalServerError()

        finally:
            session.close()

        return {f"{child}": children}, 200

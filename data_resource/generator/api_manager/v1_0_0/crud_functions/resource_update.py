# from tableschema import Schema, validate
from data_resource.db.base import db_session
from data_resource.generator.api_manager.v1_0_0.crud_functions.resource_create import (
    ResourceCreate,
)
from data_resource.logging.api_exceptions import ApiError, ApiUnhandledError
from data_resource.logging import LogFactory


logger = LogFactory.get_console_logger("generator:resource-update")


class ResourceUpdate:
    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def put_many_one_secure(self, id: int, parent: str, child: str, values):
    #     """Wrapper method for put many method.

    #     Args:
    #         id (int): Given ID of type parent
    #         parent (str): Type of parent
    #         child (str): Type of child

    #     Return:
    #         function: The wrapped method.
    #     """
    #     return self.put_many_one(self, id, parent, child, values)

    # def put_many_one(self, id: int, parent: str, child: str, values):
    #     """put data for a many to many relationship of a parent and child.

    #     Args:
    #         id (int): Given ID of type parent
    #         parent (str): Type of parent
    #         child (str): Type of child
    #     """
    #     try:
    #         session = Session()
    #         junc_table = JuncHolder.lookup_table(parent, child)

    #         # delete all relations
    #         parent_col = getattr(junc_table.c, f"{parent}_id")
    #         del_st = junc_table.delete().where(parent_col == id)

    #         _ = session.execute(del_st)

    #         # put the items
    #         many_query = []

    #         if junc_table is not None:
    #             if not isinstance(values, list):
    #                 values = [values]
    #             many_query.append([child, values, junc_table])

    #         for field, values, table in many_query:
    #             self.process_many_query(session, table, id, field, parent, values)

    #     except Exception:
    #         raise InternalServerError()

    #     finally:
    #         session.close()

    #     return self.get_many_one(id, parent, child)

    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def update_one_secure(
    #     self,
    #     id,
    #     data_model,
    #     data_resource_name,
    #     table_schema,
    #     restricted_fields,
    #     request_obj,
    #     mode="PATCH",
    # ):
    #     """Wrapper method for update one method.

    #     Args:
    #         id (any): The primary key for the specific object.
    #         data_model (object): SQLAlchemy ORM model.
    #         data_resource_name (str): Name of the data resource.
    #         table_schema (dict): The Table Schema object to use for validation.

    #     Return:
    #         function: The wrapped method.
    #     """
    #     return self.update_one(
    #         id,
    #         data_model,
    #         data_resource_name,
    #         table_schema,
    #         restricted_fields,
    #         request_obj,
    #         mode,
    #     )

    def update_one(
        self, id=1, resource_name=None, resource_orm=None, request=None, mode="PUT"
    ):
        """Update a single object from the data model based on it's primary
        key.

        Args:
            id (any): The primary key for the specific object.
            data_model (object): SQLAlchemy ORM model.
            data_resource_name (str): Name of the data resource.
            table_schema (dict): The Table Schema object to use for validation.

        Return:
            dict, int: The response object and the HTTP status code.
        """
        try:
            request_obj = request.json
        except Exception:
            db_session.rollback()
            raise ApiError("No request body found.", 400)

        try:
            # primary_key = table_schema["primaryKey"]
            primary_key = "id"
            data_obj = (
                db_session.query(resource_orm)
                .filter(getattr(resource_orm, primary_key) == id)
                .first()
            )

        except Exception:
            db_session.rollback()
            raise ApiUnhandledError("Unknown error", 500)

        if mode == "PATCH" and data_obj is None:
            db_session.rollback()
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        if data_obj is None:
            # data_obj = resource_orm() # do a post with ID?
            return ResourceCreate().insert_one(
                resource_orm=resource_orm, request=request
            )

        # _ = Schema(table_schema)
        # errors = []
        # accepted_fields = []

        # if validate(table_schema):
        #     for field in table_schema["fields"]:
        #         accepted_fields.append(field["name"])
        #     for field in request_obj.keys():
        #         if field not in accepted_fields:
        #             errors.append(f"Unknown field '{field}' found.")
        #         elif field in restricted_fields:
        #             errors.append(f"Cannot update restricted field '{field}'.")
        # else:
        #     session.close()
        #     raise ApiError("Data schema validation error.", 400)

        # if len(errors) > 0:
        #     session.close()
        #     raise ApiError("Invalid request body.", 400, errors)

        if mode == "PATCH":
            for key, value in request_obj.items():
                setattr(data_obj, key, value)
            db_session.commit()

        elif mode == "PUT":
            # for field in table_schema["fields"]:
            #     if field["required"] and field["name"] not in request_obj.keys():
            #         errors.append(f"Required field '{field['name']}' is missing.")

            # if len(errors) > 0:
            #     db_session.close()
            #     raise ApiError("Invalid request body.", 400, errors)

            for key, value in request_obj.items():
                setattr(data_obj, key, value)
            db_session.commit()

        id_value = data_obj.id

        return {"message": "Successfully updated resource.", "id": id_value}, 200

"""Generic Resource Handler."""
from brighthive_authlib import token_required
from collections import OrderedDict
from data_resource.generator.api_manager.v1_0_0.resource_get import ResourceGet
from data_resource.generator.api_manager.v1_0_0.resource_post import ResourcePost

# from data_resource.app.utils.exception_handler import (
#     ApiError,
#     ApiUnhandledError,
#     InternalServerError,
#     SchemaValidationFailure,
# ) # FIX
# from data_resource.config import ConfigurationFactory
# from data_resource.logging import LogFactory
from sqlalchemy import and_
from tableschema import Schema, validate

from data_resource.db.base import db_session
import flask
import logging


def ApiError(temp):
    return


def ApiUnhandledError(temp):
    return


def InternalServerError(temp):
    return


def SchemaValidationFailure(temp):
    return


class JuncHolder:
    def __init__(self, *args, **kwargs):
        return


class Session:
    pass


class ResourceHandler(ResourceGet, ResourcePost):
    def __init__(self):
        # self.logger = LogFactory.get_console_logger("resource-handler")
        self.logger = lambda x: x

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def query_secure(
        self,
        data_model,
        data_resource_name,
        restricted_fields,
        table_schema,
        request_obj,
    ):
        """Wrapper method for query."""
        return self.query(
            data_model, data_resource_name, restricted_fields, table_schema, request_obj
        )

    def query(
        self,
        data_model,
        data_resource_name,
        restricted_fields,
        table_schema,
        request_obj,
    ):
        """Query the data resource."""

        try:
            request_obj = request_obj.json
        except Exception:
            raise ApiError("No request body found.", 400)

        errors = []
        _ = Schema(table_schema)
        accepted_fields = []
        response = OrderedDict()
        response["results"] = []
        if validate(table_schema):
            for field in table_schema["fields"]:
                if field["name"] not in restricted_fields:
                    accepted_fields.append(field["name"])
            for field in request_obj.keys():
                if field not in accepted_fields:
                    errors.append(
                        "Unknown or restricted field '{}' found.".format(field)
                    )
            if len(errors) > 0:
                raise ApiUnhandledError("Invalid request body.", 400, errors)
            else:
                try:
                    session = Session()
                    results = session.query(data_model).filter_by(**request_obj)
                    for row in results:
                        response["results"].append(
                            build_json_from_object(row, restricted_fields)
                        )

                    if len(response["results"]) == 0:
                        return {"message": "No matches found"}, 404
                    else:
                        return response, 200
                except Exception:
                    raise ApiUnhandledError("Failed to create new resource.", 400)
                finally:
                    session.close()
        else:
            raise SchemaValidationFailure()

        return {"message": "querying data resource"}, 200

    def process_many_query(
        self,
        session: object,
        table,
        id_value: int,
        field: str,
        data_resource_name: str,
        values: list,
    ):
        """Iterates over values and adds the items to the junction table.

        Args:
            session (object): sqlalchemy session object
            id_value (int): Newly created resource of type data_resource_name
            field (str): This is the field name
            data_resource_name (str): This is the resource type (table name) of the given resource
            values (list): Holds data to be inserted into the junction table
        """
        parent_column = f"{data_resource_name}_id"
        relationship_column = f"{field}_id"

        for value in values:
            try:
                cols = {f"{parent_column}": id_value, f"{relationship_column}": value}

                insert = table.insert().values(**cols)
                session.execute(insert)
                session.commit()

            except Exception as e:
                # psycopg2.errors.UniqueViolation
                if e.code == "gkpj":
                    session.rollback()
                else:
                    raise InternalServerError()

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def put_many_one_secure(self, id: int, parent: str, child: str, values):
        """Wrapper method for put many method.

        Args:
            id (int): Given ID of type parent
            parent (str): Type of parent
            child (str): Type of child

        Return:
            function: The wrapped method.
        """
        return self.put_many_one(self, id, parent, child, values)

    def put_many_one(self, id: int, parent: str, child: str, values):
        """put data for a many to many relationship of a parent and child.

        Args:
            id (int): Given ID of type parent
            parent (str): Type of parent
            child (str): Type of child
        """
        try:
            session = Session()
            junc_table = JuncHolder.lookup_table(parent, child)

            # delete all relations
            parent_col = getattr(junc_table.c, f"{parent}_id")
            del_st = junc_table.delete().where(parent_col == id)

            _ = session.execute(del_st)

            # put the items
            many_query = []

            if junc_table is not None:
                if not isinstance(values, list):
                    values = [values]
                many_query.append([child, values, junc_table])

            for field, values, table in many_query:
                self.process_many_query(session, table, id, field, parent, values)

        except Exception:
            raise InternalServerError()

        finally:
            session.close()

        return self.get_many_one(id, parent, child)

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def patch_many_one_secure(self, id: int, parent: str, child: str, values):
        """Wrapper method for patch many method.

        Args:
            id (int): Given ID of type parent
            parent (str): Type of parent
            child (str): Type of child
            values (list or int): list of values to patch

        Return:
            function: The wrapped method.
        """
        return self.patch_many_one(id, parent, child, values)

    def patch_many_one(self, id: int, parent: str, child: str, values):
        """put data for a many to many relationship of a parent and child.

        Args:
            id (int): Given ID of type parent
            parent (str): Type of parent
            child (str): Type of child
            values (list or int): list of values to patch
        """
        try:
            session = Session()

            many_query = []
            junc_table = JuncHolder.lookup_table(parent, child)

            if junc_table is not None:
                if not isinstance(values, list):
                    values = [values]
                many_query.append([child, values, junc_table])

            for field, values, table in many_query:
                # TODO this should only insert when it doesnt already exist
                self.process_many_query(session, table, id, field, parent, values)

        except Exception:
            raise InternalServerError()

        finally:
            session.close()

        return self.get_many_one(id, parent, child)

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def update_one_secure(
        self,
        id,
        data_model,
        data_resource_name,
        table_schema,
        restricted_fields,
        request_obj,
        mode="PATCH",
    ):
        """Wrapper method for update one method.

        Args:
            id (any): The primary key for the specific object.
            data_model (object): SQLAlchemy ORM model.
            data_resource_name (str): Name of the data resource.
            table_schema (dict): The Table Schema object to use for validation.

        Return:
            function: The wrapped method.
        """
        return self.update_one(
            id,
            data_model,
            data_resource_name,
            table_schema,
            restricted_fields,
            request_obj,
            mode,
        )

    def update_one(
        self,
        id,
        data_model,
        data_resource_name,
        table_schema,
        restricted_fields,
        request_obj,
        mode="PATCH",
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
            request_obj = request_obj.json
        except Exception:
            raise ApiError("No request body found.", 400)

        try:
            primary_key = table_schema["primaryKey"]
            session = Session()
            data_obj = (
                session.query(data_model)
                .filter(getattr(data_model, primary_key) == id)
                .first()
            )
            if data_obj is None:
                session.close()
                raise ApiUnhandledError(f"Resource with id '{id}' not found.", 404)
        except Exception:
            raise ApiUnhandledError(f"Resource with id '{id}' not found.", 404)

        _ = Schema(table_schema)
        errors = []
        accepted_fields = []
        if validate(table_schema):
            for field in table_schema["fields"]:
                accepted_fields.append(field["name"])
            for field in request_obj.keys():
                if field not in accepted_fields:
                    errors.append(f"Unknown field '{field}' found.")
                elif field in restricted_fields:
                    errors.append(f"Cannot update restricted field '{field}'.")
        else:
            session.close()
            raise ApiError("Data schema validation error.", 400)

        if len(errors) > 0:
            session.close()
            raise ApiError("Invalid request body.", 400, errors)

        if mode == "PATCH":
            for key, value in request_obj.items():
                setattr(data_obj, key, value)
            session.commit()
        elif mode == "PUT":
            for field in table_schema["fields"]:
                if field["required"] and field["name"] not in request_obj.keys():
                    errors.append(f"Required field '{field['name']}' is missing.")

            if len(errors) > 0:
                session.close()
                raise ApiError("Invalid request body.", 400, errors)

            for key, value in request_obj.items():
                setattr(data_obj, key, value)
            session.commit()

        session.close()
        return {"message": f"Successfully updated resource '{id}'."}, 201

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

    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def delete_many_one_secure(self, id: int, parent: str, child: str, values):
        return self.delete_many_one(id, parent, child, values)

    def delete_many_one(self, id: int, parent: str, child: str, values):
        try:
            session = Session()
            junc_table = JuncHolder.lookup_table(parent, child)

            if not isinstance(values, list):
                values = [values]

            for value in values:
                parent_col = getattr(junc_table.c, f"{parent}_id")
                child_col = getattr(junc_table.c, f"{child}_id")
                del_st = junc_table.delete().where(
                    and_(parent_col == id, child_col == value)
                )

                res = session.execute(del_st)
                print(res)
                session.commit()

        except Exception:
            session.rollback()
            raise InternalServerError()

        finally:
            session.close()

        return self.get_many_one(id, parent, child)

"""Versioned Resource.

This class extends the Flask Restful Resource class with the ability to
look for the API version number in the request header.
"""

from data_resource.generator.api_manager.v1_0_0 import (
    ResourceHandler as V1_0_0_ResourceHandler,
)
from flask import request
from flask_restful import Resource
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.shared_utils.auth_util import check_auth


logger = LogFactory.get_console_logger("generator:versioned-resource")


class VersionedResourceParent(Resource):
    __slots__ = ["name", "resource_orm", "parent_orm", "child_orm"]

    def __init__(self):
        Resource.__init__(self)

    def get_api_version(self, headers):
        try:
            api_version = headers["X-Api-Version"]
        except KeyError:
            api_version = "1.0.0"
        return api_version

    def get_resource_handler(self, headers):
        if self.get_api_version(headers) == "1.0.0":
            return V1_0_0_ResourceHandler()
        else:
            return V1_0_0_ResourceHandler()


class VersionedResource(VersionedResourceParent):
    _query_route = "/query"

    @check_auth
    def get(self, id=None):
        # if self.api_schema["get"]["secured"]:

        # if not self.api_schema["get"]["enabled"]:
        #     raise MethodNotAllowed()
        # if request.path.endswith("/query"):
        #     raise MethodNotAllowed()

        offset = 0
        limit = 20
        try:
            offset = request.args["offset"]
        except KeyError:
            pass

        try:
            limit = request.args["limit"]
        except KeyError:
            pass

        if id is None:
            return self.get_resource_handler(request.headers).get_all(
                resource_name=self.name,
                resource_orm=self.resource_orm,
                offset=offset,
                limit=limit,
            )

        else:
            #     if self.api_schema["get"]["secured"]:
            #         return self.get_resource_handler(request.headers).get_one_secure(
            #             id, self.data_model, self.data_resource_name, self.table_schema
            #         )
            #     else:
            return self.get_resource_handler(request.headers).get_one(
                id=id, resource_name=self.name, resource_orm=self.resource_orm
            )

    @check_auth
    def post(self):
        # if self.api_schema["get"]["secured"]:

        # if not self.api_schema["post"]["enabled"]:
        #     raise MethodNotAllowed()

        # if self.api_schema["post"]["secured"]:
        if request.path.endswith("/query"):
            return self.get_resource_handler(request.headers).query_one(
                resource_orm=self.resource_orm, request=request
            )

        return self.get_resource_handler(request.headers).insert_one(
            resource_orm=self.resource_orm, request=request
        )

    @check_auth
    def put(self, id):
        # if self.api_schema["get"]["secured"]:
        # if not self.api_schema["put"]["enabled"]:
        #     raise MethodNotAllowed()
        # if request.path.endswith("/query"):
        #     raise MethodNotAllowed()

        # if self.api_schema["put"]["secured"]:
        #     return self.get_resource_handler(request.headers).update_one_secure(
        #         id,
        #         self.data_model,
        #         self.data_resource_name,
        #         self.table_schema,
        #         self.restricted_fields,
        #         request,
        #         mode="PUT",
        #     )
        # else:
        return self.get_resource_handler(request.headers).update_one(
            id=id,
            resource_name=self.name,
            resource_orm=self.resource_orm,
            request=request,
            mode="PUT",
        )

    @check_auth
    def patch(self, id):
        # if self.api_schema["get"]["secured"]:
        # if not self.api_schema["patch"]["enabled"]:
        #     raise MethodNotAllowed()
        # if request.path.endswith("/query"):
        #     raise MethodNotAllowed()

        # if self.api_schema["patch"]["secured"]:
        #     return self.get_resource_handler(request.headers).update_one_secure(
        #         id,
        #         self.data_model,
        #         self.data_resource_name,
        #         self.table_schema,
        #         self.restricted_fields,
        #         request,
        #         mode="PATCH",
        #     )
        # else:
        return self.get_resource_handler(request.headers).update_one(
            id=id,
            resource_name=self.name,
            resource_orm=self.resource_orm,
            request=request,
            mode="PATCH",
        )

    @check_auth
    def delete(self, id):
        # if self.api_schema["get"]["secured"]:
        # if self.api_schema["delete"]["enabled"]:
        #     raise MethodNotAllowed()

        # if self.api_schema["delete"]["secured"]:
        # return {"message": "Unimplemented secure delete"}, 405
        # else:
        return {"message": "Unimplemented unsecure delete"}, 405


class VersionedResourceMany(VersionedResourceParent):
    # def error_if_resource_is_disabled(self, verb: str, resource: str, api_schema: dict):
    #     """This will raise an exception that will return an error to the client
    #     if they attempt to access a disabled resource.

    #     Returns nothing.
    #     """
    #     enabled = False
    #     try:
    #         for custom_resource in api_schema["custom"]:
    #             if custom_resource["resource"] == resource:
    #                 for method in custom_resource["methods"]:
    #                     enabled = method[verb]["enabled"]
    #                     if not enabled:
    #                         raise MethodNotAllowed()

    #                     return

    #     except KeyError:
    #         raise MethodNotAllowed()

    # def is_secured(self, verb: str, resource: str, api_schema: dict):
    #     """Defaults to secured for security."""
    #     try:
    #         secured = False
    #         for custom_resource in api_schema["custom"]:
    #             if custom_resource["resource"] == resource:
    #                 # assert is bool?
    #                 for method in custom_resource["methods"]:
    #                     secured = method[verb]["secured"]

    #         return secured

    #     except KeyError:
    #         return True

    @check_auth
    def get(self, id=None):
        # route should be parent/<id>/child
        # paths = request.path.split("/")
        # parent, child = paths[1], paths[3]

        # resource = f"/{parent}/{child}"
        # self.error_if_resource_is_disabled("get", resource, self.api_schema)

        # if self.is_secured("get", resource, self.api_schema):
        #     return self.get_resource_handler(request.headers).get_many_one_secure(
        #         id, parent, child
        #     )
        # else:
        return self.get_resource_handler(request.headers).get_mn_one(
            id, self.parent_orm, self.child_orm
        )

    @check_auth
    def put(self, id=None):
        #     # Replaces all data
        #     paths = request.path.split("/")
        #     parent, child = paths[1], paths[3]

        #     resource = f"/{parent}/{child}"
        #     self.error_if_resource_is_disabled("put", resource, self.api_schema)

        #     value =
        #     if self.is_secured("put", resource, self.api_schema):
        #         return self.get_resource_handler(request.headers).put_many_one_secure(
        #             id, parent, child, value
        #         )
        #     else:
        body = request.json

        return self.get_resource_handler(request.headers).put_mn_one(
            id, body, self.parent_orm, self.child_orm
        )

    @check_auth
    def patch(self, id=None):
        #     paths = request.path.split("/")
        #     parent, child = paths[1], paths[3]

        #     resource = f"/{parent}/{child}"
        #     self.error_if_resource_is_disabled("patch", resource, self.api_schema)

        #     value = request.json[child]
        #     if self.is_secured("put", resource, self.api_schema):
        #         return self.get_resource_handler(request.headers).patch_many_one_secure(
        #             id, parent, child, value
        #         )
        #     else:
        body = request.json

        return self.get_resource_handler(request.headers).put_mn_one(
            id, body, self.parent_orm, self.child_orm, patch=True
        )

    # def delete(self, id=None):
    #     paths = request.path.split("/")
    #     parent, child = paths[1], paths[3]

    #     resource = f"/{parent}/{child}"
    #     self.error_if_resource_is_disabled("delete", resource, self.api_schema)

    #     value = request.json[child]  # Needs an except KeyError
    #     if self.is_secured("delete", resource, self.api_schema):
    #         return self.get_resource_handler(request.headers).delete_many_one_secure(
    #             id, parent, child, value
    #         )
    #     else:
    #         return self.get_resource_handler(request.headers).delete_many_one(
    #             id, parent, child, value
    #         )

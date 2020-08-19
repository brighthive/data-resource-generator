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
            return self.get_resource_handler(request.headers).get_one(
                id=id, resource_name=self.name, resource_orm=self.resource_orm
            )

    @check_auth
    def post(self):
        if request.path.endswith("/query"):
            return self.get_resource_handler(request.headers).query_one(
                resource_orm=self.resource_orm, request=request
            )

        return self.get_resource_handler(request.headers).insert_one(
            resource_orm=self.resource_orm, request=request
        )

    @check_auth
    def put(self, id):
        return self.get_resource_handler(request.headers).update_one(
            id=id,
            resource_name=self.name,
            resource_orm=self.resource_orm,
            request=request,
            mode="PUT",
        )

    @check_auth
    def patch(self, id):
        return self.get_resource_handler(request.headers).update_one(
            id=id,
            resource_name=self.name,
            resource_orm=self.resource_orm,
            request=request,
            mode="PATCH",
        )

    @check_auth
    def delete(self, id):
        return {"message": "Unimplemented unsecure delete"}, 405


class VersionedResourceMany(VersionedResourceParent):
    @check_auth
    def get(self, id=None):
        return self.get_resource_handler(request.headers).get_mn_one(
            id, self.parent_orm, self.child_orm
        )

    @check_auth
    def put(self, id=None):
        body = request.json

        return self.get_resource_handler(request.headers).put_mn_one(
            id, body, self.parent_orm, self.child_orm
        )

    @check_auth
    def patch(self, id=None):
        body = request.json

        return self.get_resource_handler(request.headers).put_mn_one(
            id, body, self.parent_orm, self.child_orm, patch=True
        )

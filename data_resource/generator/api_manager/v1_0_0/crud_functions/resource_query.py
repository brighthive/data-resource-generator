from data_resource.db.base import db_session
from flask import Request
from data_resource.logging.api_exceptions import ApiError, ApiUnhandledError
from data_resource.logging import LogFactory
from collections import OrderedDict
from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_json_from_object,
)

logger = LogFactory.get_console_logger("generator:resource-create")


class ResourceQuery:
    def query_one(self, resource_orm: object = None, request: Request = None):
        try:
            request_obj = request.json
        except Exception:
            raise ApiError("No request body found.", 400)

        if request_obj is None or len(request_obj) == 0:
            raise ApiError("No fields found in body.", 400)

        response = OrderedDict()
        response["results"] = []
        errors = []

        # Find invalid fields
        orm_fields = [field.name for field in resource_orm.__table__.columns]

        for key, _ in request_obj.items():
            if key not in orm_fields:
                errors.append(f"Unknown or restricted field '{key}' found.")

        if errors:
            raise ApiError("Invalid request body.", 400, errors)

        # Do the query
        try:
            results = db_session.query(resource_orm).filter_by(**request_obj)
            for row in results:
                response["results"].append(build_json_from_object(row, {}))

            if len(response["results"]) == 0:
                return {"message": "No matches found"}, 404
            else:
                return response, 200

        except Exception:
            raise ApiUnhandledError("Failed to create new resource.", 400)

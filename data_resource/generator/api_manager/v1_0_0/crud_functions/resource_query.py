from data_resource.db.base import db_session
from flask import Request
from data_resource.logging.api_exceptions import ApiError
from data_resource.logging import LogFactory

logger = LogFactory.get_console_logger("generator:resource-create")


class ResourceQuery:
    def query_one(self, resource_orm: object = None, request: Request = None):
        try:
            request_obj = request.json
        except Exception:
            raise ApiError("No request body found.", 400)

        if request_obj is None or len(request_obj) == 0:
            raise ApiError("No fields found in body.", 400)

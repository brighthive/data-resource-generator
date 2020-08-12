from flask_restful import Api, Resource
from flask import Blueprint, current_app, request
from data_resource.generator.app import start_data_resource_generator
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.shared_utils.auth_util import check_auth
from data_resource.shared_utils.api_exceptions import ApiError

generator_bp = Blueprint("generator_bp", __name__)
api = Api(generator_bp)
logger = LogFactory.get_console_logger("admin:route-generator")


class Generator(Resource):
    @check_auth
    def post(self):
        try:
            touch_database = request.json["touch_database"]
        except KeyError:
            touch_database = True

        if "ignore_validation" not in request.json:
            try:
                data_resource_schema = request.json["data_resource_schema"]
            except KeyError:
                raise ApiError(
                    "Data Resource Schema should be placed inside root key 'data_resource_schema'."
                )

        api = current_app.config["api"]

        start_data_resource_generator(
            data_resource_schema, api, touch_database=touch_database
        )

        logger.info("Data Resource(s) successfully generated.")

        return "OK", 204


api.add_resource(Generator, "/generator")

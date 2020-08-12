from flask_restful import Api, Resource
from flask import Blueprint, current_app, request
from data_resource.generator.app import start_data_resource_generator
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.shared_utils.auth_util import check_auth

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

        data_resource_schema = request.json["data_catalog"]

        # TODO should run a check on the catalog, fail if invalid

        api = current_app.config["api"]

        start_data_resource_generator(
            data_resource_schema, api, touch_database=touch_database
        )
        # TODO should log?

        return "OK", 204


api.add_resource(Generator, "/generator")

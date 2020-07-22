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
        data_catalog = request.json["data_catalog"]

        # TODO should run a check on the catalog, fail if invalid

        api = current_app.config["api"]
        start_data_resource_generator(
            data_catalog, api
        )  # TODO generator should generate to a subroute?

        # TODO should log?

        return "", 204


api.add_resource(Generator, "/generator")

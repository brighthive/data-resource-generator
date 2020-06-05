from flask_restful import Api, Resource
from flask import Blueprint, current_app, request
import logging
from data_resource.generator.app import start_data_resource_generator


generator_bp = Blueprint("generator_bp", __name__)
api = Api(generator_bp)

logging.basicConfig(level=logging.INFO)


class Generator(Resource):
    def post(self):
        data_catalog = request.json["data_catalog"]

        api = current_app.config["api"]
        start_data_resource_generator(
            data_catalog, api
        )  # TODO generator should generate to a subroute?

        return "", 204


api.add_resource(Generator, "/generator")

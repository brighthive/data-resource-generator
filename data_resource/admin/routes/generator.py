from flask_restful import Api, Resource
from flask import Blueprint, current_app, request
from data_resource.db import db_session
import connexion
import data_resource.admin.models as orm
import logging
from convert_descriptor_to_swagger import convert_descriptor_to_swagger
from data_resource.generator.app import start_data_resource_generator


generator_bp = Blueprint("generator_bp", __name__)
api = Api(generator_bp)

logging.basicConfig(level=logging.INFO)


class Generator(Resource):
    def post(self):
        data_catalog = request.json["data_catalog"]

        api = current_app.config["api"]
        start_data_resource_generator(data_catalog, api)

        return "", 204


api.add_resource(Generator, "/generator")

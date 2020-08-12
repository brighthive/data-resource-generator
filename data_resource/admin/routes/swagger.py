from flask_restful import Api, Resource
from flask import Blueprint, request
from data_resource.db import db_session
import data_resource.admin.models as orm
from convert_descriptor_to_swagger import convert_descriptor_to_swagger
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.shared_utils.auth_util import check_auth


def generate_all_swagger(descriptors):
    swagger = convert_descriptor_to_swagger(descriptors)
    return swagger


swagger_bp = Blueprint("swagger_bp", __name__)
api = Api(swagger_bp)
logger = LogFactory.get_console_logger("admin:route-swagger")


class Swagger(Resource):
    @check_auth
    def get(self):
        # relationship = request.json or []

        q = db_session.query(orm.TableSchema)
        all_tableschema = [p.tableschema for p in q]

        if all_tableschema:
            swagger = generate_all_swagger(all_tableschema)
        else:
            swagger = ""

        # TODO should log?

        return {"swagger": swagger}, 200


api.add_resource(Swagger, "/swagger")

from flask_restful import Api, Resource
from flask import Blueprint
from data_resource.db import db_session
import data_resource.admin.models as orm
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.shared_utils.auth_util import check_auth


tableschema_bp = Blueprint("tableschema_bp", __name__)
api = Api(tableschema_bp)
logger = LogFactory.get_console_logger("admin:route-tableschema")


class TableSchema(Resource):
    @check_auth
    def get(self, limit=100):
        q = db_session.query(orm.TableSchema)

        return [p.dump() for p in q][:limit]


api.add_resource(TableSchema, "/tableschema")

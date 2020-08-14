from flask_restful import Api, Resource
from flask import Blueprint, request
from data_resource.db import db_session
import data_resource.admin.models as orm
from tableschema import Schema
import json
from convert_descriptor_to_swagger import convert_descriptor_to_swagger
from data_resource.shared_utils.api_exceptions import ApiError
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.shared_utils.auth_util import check_auth


tableschema_id_bp = Blueprint("tableschema_id_bp", __name__)
api = Api(tableschema_id_bp)
logger = LogFactory.get_console_logger("admin:route-tableschema-id")


def generate_swagger(descriptor):
    logger.info(json.dumps(descriptor, indent=4))
    swagger = convert_descriptor_to_swagger([descriptor])
    return swagger


class TableSchemaID(Resource):
    @check_auth
    def get(self, _id):
        item = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        return item.dump() if item is not None else ("Not found", 404)

    @check_auth
    def put(self, _id):
        item = request.json
        try:
            delattr(item, "swagger")  # ??
        except AttributeError:
            pass

        try:
            json.dumps(item["tableschema"]["datastore"]["schema"])  # ??
        except KeyError:
            raise ApiError("Invalid JSON", 400)

        schema = Schema(descriptor=item["tableschema"]["datastore"]["schema"])

        if not schema.valid:
            raise ApiError(
                "Tableschema validation error.",
                errors=[str(e) for e in schema.errors],
                status_code=400,
            )

        p = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        item["id"] = _id
        item["swagger"] = generate_swagger(item["tableschema"])
        if p is not None:
            p.update(**item)
            entry = p
        else:
            # item['created'] = datetime.datetime.utcnow()
            entry = orm.TableSchema(**item)
            db_session.add(entry)
        db_session.commit()

        return (
            {"tableschema": entry.tableschema, "swagger": entry.swagger},
            (200 if entry is not None else 201),
        )

    @check_auth
    def delete(self, _id):
        item = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        if item is not None:
            db_session.query(orm.TableSchema).filter(orm.TableSchema.id == _id).delete()
            db_session.commit()
            return "", 204
        else:
            return "", 404


api.add_resource(TableSchemaID, "/tableschema/<int:_id>")

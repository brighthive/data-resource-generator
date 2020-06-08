from flask_restful import Api, Resource
from flask import Blueprint, request
from data_resource.db import db_session
import data_resource.admin.models as orm
from tableschema import Schema
import json
from convert_descriptor_to_swagger import convert_descriptor_to_swagger
from data_resource.logging.api_exceptions import ApiError
from data_resource.logging import LogFactory

tableschema_id_bp = Blueprint("tableschema_id_bp", __name__)
api = Api(tableschema_id_bp)
logger = LogFactory.get_console_logger("admin:route-tableschema-id")


def generate_swagger(descriptor):
    logger.info(json.dumps(descriptor, indent=4))
    swagger = convert_descriptor_to_swagger([descriptor])
    return swagger


class TableSchemaID(Resource):
    def get(self, _id):
        pet = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        return pet.dump() if pet is not None else ("Not found", 404)

    def put(self, _id):
        pet = request.json
        try:
            delattr(pet, "swagger")
        except AttributeError:
            pass

        try:
            json.dumps(pet["tableschema"]["datastore"]["schema"])
        except KeyError:
            raise ApiError("Invalid JSON", 400)

        schema = Schema(descriptor=pet["tableschema"]["datastore"]["schema"])

        if not schema.valid:
            raise ApiError([str(e) for e in schema.errors], 400)  # TODO unit test

        p = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        pet["id"] = _id
        pet["swagger"] = generate_swagger(pet["tableschema"])
        if p is not None:
            logger.info("Updating resource %s..", _id)  # TODO Needed?
            p.update(**pet)
            entry = p
        else:
            logger.info("Creating resource %s..", _id)  # TODO Needed?
            # pet['created'] = datetime.datetime.utcnow()
            entry = orm.TableSchema(**pet)
            db_session.add(entry)
        db_session.commit()

        return (
            {"tableschema": entry.tableschema, "swagger": entry.swagger},
            (200 if entry is not None else 201),
        )

    def delete(self, _id):
        pet = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        if pet is not None:
            logger.info("Deleting resource %s..", _id)  # TODO Needed?
            db_session.query(orm.TableSchema).filter(orm.TableSchema.id == _id).delete()
            db_session.commit()
            return "", 204
        else:
            return "", 404


api.add_resource(TableSchemaID, "/tableschema/<int:_id>")

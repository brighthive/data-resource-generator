from flask_restful import Api, Resource
from flask import Blueprint, current_app, request
from data_resource.db import db_session
import connexion
import data_resource.admin.models as orm
import logging
from tableschema import Schema
import json
from convert_descriptor_to_swagger import convert_descriptor_to_swagger


def generate_swagger(descriptor):
    logging.info("O WOW")
    logging.info(json.dumps(descriptor, indent=4))
    swagger = convert_descriptor_to_swagger([descriptor])
    return swagger


logging.basicConfig(level=logging.INFO)

tableschema_id_bp = Blueprint("tableschema_id_bp", __name__)
api = Api(tableschema_id_bp)


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
        except:
            return {"errors": "Invalid JSON"}, 400

        schema = Schema(descriptor=pet["tableschema"]["datastore"]["schema"])

        if not schema.valid:
            return {"errors": [str(e) for e in schema.errors]}, 400

        p = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        pet["id"] = _id
        pet["swagger"] = generate_swagger(pet["tableschema"])
        if p is not None:
            logging.info("Updating pet %s..", _id)
            p.update(**pet)
        else:
            logging.info("Creating pet %s..", _id)
            # pet['created'] = datetime.datetime.utcnow()
            db_session.add(orm.TableSchema(**pet))
        db_session.commit()

        return (
            {"tableschema": p.tableschema, "swagger": p.swagger},
            (200 if p is not None else 201),
        )

    def delete(self, _id):
        pet = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        if pet is not None:
            logging.info("Deleting pet %s..", _id)
            db_session.query(orm.TableSchema).filter(orm.TableSchema.id == _id).delete()
            db_session.commit()
            return "", 204
        else:
            return "", 404


api.add_resource(TableSchemaID, "/tableschema/<int:_id>")

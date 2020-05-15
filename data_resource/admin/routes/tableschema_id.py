from flask_restful import Api, Resource
from flask import Blueprint, current_app, request
from data_resource.db import db_session
import connexion
import data_resource.admin.models as orm
import logging


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
        print(request.json)
        pet = request.json
        print(pet)
        p = (
            db_session.query(orm.TableSchema)
            .filter(orm.TableSchema.id == _id)
            .one_or_none()
        )
        pet["id"] = _id
        if p is not None:
            logging.info("Updating pet %s..", _id)
            p.update(**pet)
        else:
            logging.info("Creating pet %s..", _id)
            # pet['created'] = datetime.datetime.utcnow()
            db_session.add(orm.TableSchema(**pet))
        db_session.commit()
        return None, (200 if p is not None else 201)

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
            return None, 204
        else:
            return None, 404


api.add_resource(TableSchemaID, "/tableschema/<int:_id>")

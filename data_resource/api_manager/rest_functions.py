import connexion
from connexion import NoContent
from data_resource.db.base import db_session
import flask


def dump(item):
    return {k: v for k, v in vars(item).items() if not k.startswith("_")}


# class OrmResource:
#     def __init__(self, orm, fn, orm_name):
#         self.orm = orm
#         self.fn = fn
#         self.orm_name = orm_name
#
#     def __call__(self):
#         self.fn(self)


def get_resources_closure(resource_orm):
    def get_resources(limit, offset):
        q = db_session.query(resource_orm)

        return [dump(p) for p in q][:limit]

    return get_resources


def get_resource_id_closure(resource_orm):
    def get_resource_id(**kwargs):
        id = kwargs["id"]

        resource = (
            db_session.query(resource_orm).filter(resource_orm.id == id).one_or_none()
        )
        return dump(resource) if resource is not None else ("Not found", 404)

    return get_resource_id


def put_resource_closure(resource_orm):
    def put_resource(**kwargs):
        resource_id = kwargs.get("id", None)
        # resource_id = connexion.request.json.get("id", None)
        resource = connexion.request.json

        p = (
            db_session.query(resource_orm)
            .filter(resource_orm.id == resource_id)
            .one_or_none()
        )

        resource["id"] = resource_id
        if p is not None:
            print("Updating pet %s..", resource_id)
            # logging.info("Updating pet %s..", resource_id)
            p.update(**resource)
        else:
            print("Creating pet %s..", resource_id)
            # logging.info("Creating pet %s..", resource_id)
            # resource['created'] = datetime.datetime.utcnow()
            db_session.add(resource_orm(**resource))
        db_session.commit()
        return NoContent, (200 if p is not None else 201)

    return put_resource


# def delete_pet(pet_id):
#     pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
#     if pet is not None:
#         logging.info('Deleting pet %s..', pet_id)
#         db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).delete()
#         db_session.commit()
#         return NoContent, 204
#     else:
#         return NoContent, 404

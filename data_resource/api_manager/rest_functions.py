import connexion
from connexion import NoContent
from data_resource.db.base import db_session
import flask

# def get_peoples_fn(orm_cls):
#     orm = orm_cls


def dump(item):
    return {k: v for k, v in vars(item).items() if not k.startswith("_")}


def get_people():
    limit = 100
    print(connexion.request.json)

    orm = flask.current_app.config["base"].classes

    q = db_session.query(orm.People)

    return [dump(p) for p in q][:limit]


def put_people(*args):
    print(connexion.request.json)

    people_id = connexion.request.json.get("id", None)
    people = connexion.request.json

    orm = flask.current_app.config["base"].classes

    p = db_session.query(orm.People).filter(orm.People.id == people_id).one_or_none()

    people["id"] = people_id
    if p is not None:
        print("Updating pet %s..", people_id)
        # logging.info("Updating pet %s..", people_id)
        p.update(**people)
    else:
        print("Creating pet %s..", people_id)
        # logging.info("Creating pet %s..", people_id)
        # people['created'] = datetime.datetime.utcnow()
        db_session.add(orm.People(**people))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


# def get_pet(pet_id):
#     pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
#     return pet.dump() if pet is not None else ('Not found', 404)


# def put_pet(pet_id, pet):
#     p = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
#     pet['id'] = pet_id
#     if p is not None:
#         logging.info('Updating pet %s..', pet_id)
#         p.update(**pet)
#     else:
#         logging.info('Creating pet %s..', pet_id)
#         pet['created'] = datetime.datetime.utcnow()
#         db_session.add(orm.Pet(**pet))
#     db_session.commit()
#     return NoContent, (200 if p is not None else 201)


# def delete_pet(pet_id):
#     pet = db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).one_or_none()
#     if pet is not None:
#         logging.info('Deleting pet %s..', pet_id)
#         db_session.query(orm.Pet).filter(orm.Pet.id == pet_id).delete()
#         db_session.commit()
#         return NoContent, 204
#     else:
#         return NoContent, 404

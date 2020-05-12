def get_pets(limit, animal_type=None):
    q = db_session.query(orm.Pet)
    if animal_type:
        q = q.filter(orm.Pet.animal_type == animal_type)
    return [p.dump() for p in q][:limit]


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

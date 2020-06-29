from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_links,
    build_json_from_object,
)
from collections import OrderedDict
from data_resource.db.base import db_session
from data_resource.logging.api_exceptions import InternalServerError, ApiError
from data_resource.logging import LogFactory


logger = LogFactory.get_console_logger("generator:mn-update")


class MnUpdate:
    def put_mn_one(self, id: int, body: list, parent_orm: object, child_orm: object):
        # """Retrieve the many to many relationship data of a parent and child.

        # Args:
        #     id (int): Given ID of type parent
        #     parent (str): Type of parent
        #     child (str): Type of child
        # """
        if id == 0:
            return {}, 200

        # try:
        # primary_key = "id"
        # result = (
        #     db_session.query(parent_orm)
        #     .filter(getattr(parent_orm, primary_key) == id)
        #     .first()
        # )
        # # except Exception:
        # #     db_session.rollback()
        # #     raise InternalServerError()

        # if result is None:
        #     db_session.rollback()
        #     raise ApiError(f"Resource with id '{id}' not found.", 404)

        # mn_list = getattr(result, f"{child_orm.__table__.name}_collection")
        # response = [item.id for item in mn_list]

        # # response = build_json_from_object(result)
        # return response, 200

        return [1], 200

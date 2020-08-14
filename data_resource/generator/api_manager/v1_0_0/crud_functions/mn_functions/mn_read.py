from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_links,
    build_json_from_object,
)
from collections import OrderedDict
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import InternalServerError, ApiError
from data_resource.shared_utils.log_factory import LogFactory


logger = LogFactory.get_console_logger("generator:mn-read")


class MnRead:
    def get_mn_one(self, id: int, parent_orm: object, child_orm: object):
        """GET M:N relationship data of a parent and child.

        Args:
            id (int): Given ID of type parent
            parent (str): Type of parent
            child (str): Type of child
        """
        if id == 0:
            return {}, 200

        primary_key = "id"
        result = (
            db_session.query(parent_orm)
            .filter(getattr(parent_orm, primary_key) == id)
            .first()
        )

        if result is None:
            db_session.rollback()
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        mn_list = getattr(result, f"{child_orm.__table__.name}_collection")

        response = [item.id for item in mn_list]

        return response, 200

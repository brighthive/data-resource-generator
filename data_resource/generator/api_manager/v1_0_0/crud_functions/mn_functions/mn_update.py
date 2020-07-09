from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_links,
    build_json_from_object,
)
from collections import OrderedDict
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import InternalServerError, ApiError
from data_resource.shared_utils.log_factory import LogFactory


logger = LogFactory.get_console_logger("generator:mn-update")


class MnUpdate:
    def put_mn_one(
        self,
        id: int,
        body: list,
        parent_orm: object,
        child_orm: object,
        patch: bool = False,
    ):
        # """Retrieve the many to many relationship data of a parent and child.

        # Args:
        #     id (int): Given ID of type parent
        #     parent (str): Type of parent
        #     child (str): Type of child
        # """
        if id == 0:
            return {}, 200

        # try:
        primary_key = "id"
        parent = (
            db_session.query(parent_orm)
            .filter(getattr(parent_orm, primary_key) == id)
            .first()
        )
        # except Exception:
        #     db_session.rollback()
        #     raise InternalServerError()

        if parent is None:
            db_session.rollback()
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        # TODO: check if all put body values exist?

        if type(body) is not list:
            body = [body]

        if not patch:
            # Remove all items from parent
            mn_list = getattr(parent, f"{child_orm.__table__.name}_collection")
            mn_list.clear()

        # Add items to parent
        for child_id in body:
            child = (
                db_session.query(child_orm)
                .filter(getattr(child_orm, primary_key) == child_id)
                .first()
            )

            if child is None:
                db_session.rollback()
                raise ApiError(f"Child with id '{child_id}' does not exist.")

            parent.team_collection.append(child)

        db_session.commit()

        # TODO this can be moved to a model class as its reused in GET
        mn_list = getattr(parent, f"{child_orm.__table__.name}_collection")
        response = [item.id for item in mn_list]

        # response = build_json_from_object(parent)
        return response, 200

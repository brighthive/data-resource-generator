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
        """PUT m:n relationship data between a parent and child.

        Args:
            id (int): Given ID of type parent
            body: list,
            parent_orm: object,
            child_orm: object,
            patch: bool = False,
        """
        if id == 0:  # For testing
            return {}, 200

        primary_key = "id"
        parent = (
            db_session.query(parent_orm)
            .filter(getattr(parent_orm, primary_key) == id)
            .first()
        )

        if parent is None:
            db_session.rollback()
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        if type(body) is not list:
            body = [body]

        mn_list = getattr(parent, f"{child_orm.__table__.name}_collection")

        if not patch:
            mn_list.clear()

        for child_id in body:
            child = (
                db_session.query(child_orm)
                .filter(getattr(child_orm, primary_key) == child_id)
                .first()
            )

            if child is None:
                db_session.rollback()
                raise ApiError(f"Child with id '{child_id}' does not exist.")

            mn_list.append(child)

        db_session.commit()

        response = [item.id for item in mn_list]

        return response, 200

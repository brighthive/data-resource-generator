from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_links,
    build_json_from_object,
)
from collections import OrderedDict
from data_resource.db.base import db_session
from data_resource.shared_utils.api_exceptions import InternalServerError, ApiError
from data_resource.shared_utils import LogFactory


logger = LogFactory.get_console_logger("generator:mn-read")


class MnRead:
    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def get_many_one_secure(self, id: int, parent: str, child: str):
    #     # """Wrapper method for get many method.

    #     # Args:
    #     #     id (int): Given ID of type parent
    #     #     parent (str): Type of parent
    #     #     child (str): Type of child

    #     # Return:
    #     #     function: The wrapped method.
    #     # """
    #     return self.get_many_one(id, parent, child)

    def get_mn_one(self, id: int, parent_orm: object, child_orm: object):
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
        result = (
            db_session.query(parent_orm)
            .filter(getattr(parent_orm, primary_key) == id)
            .first()
        )
        # except Exception:
        #     db_session.rollback()
        #     raise InternalServerError()

        if result is None:
            db_session.rollback()
            raise ApiError(f"Resource with id '{id}' not found.", 404)

        mn_list = getattr(result, f"{child_orm.__table__.name}_collection")
        response = [item.id for item in mn_list]

        # response = build_json_from_object(result)
        return response, 200

        # join_table = JuncHolder.lookup_table(parent, child)

        # # This should not be reachable
        # # if join_table is None:
        # # return {'error': f"relationship '{child}' of '{parent}' not found."}
        # try:
        #     session = Session()
        #     parent_col_str = f"{parent}_id"
        #     child_col_str = f"{child}_id"

        #     cols = {parent_col_str: id}
        #     query = session.query(join_table).filter_by(**cols).all()

        #     children = []
        #     for row in query:
        #         # example - {'programs_id': 2, 'credentials_id': 3}
        #         row_dict = row._asdict()
        #         children.append(row_dict[child_col_str])

        # except Exception:
        #     raise InternalServerError()

        # finally:
        #     session.close()

        # return {f"{child}": children}, 200

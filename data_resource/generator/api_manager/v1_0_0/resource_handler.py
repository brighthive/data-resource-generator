"""Generic Resource Handler."""
from data_resource.generator.api_manager.v1_0_0.crud_functions import (
    ResourceRead,
    ResourceCreate,
    ResourceUpdate,
    ResourceQuery,
)
from data_resource.generator.api_manager.v1_0_0.crud_functions.mn_functions import (
    MnRead,
    MnUpdate,
)

# from data_resource.config import ConfigurationFactory


class ResourceHandler(
    ResourceRead, ResourceCreate, ResourceUpdate, ResourceQuery, MnRead, MnUpdate
):

    # def process_many_query(
    #     self,
    #     session: object,
    #     table,
    #     id_value: int,
    #     field: str,
    #     data_resource_name: str,
    #     values: list,
    # ):
    #     """Iterates over values and adds the items to the junction table.

    #     Args:
    #         session (object): sqlalchemy session object
    #         id_value (int): Newly created resource of type data_resource_name
    #         field (str): This is the field name
    #         data_resource_name (str): This is the resource type (table name) of the given resource
    #         values (list): Holds data to be inserted into the junction table
    #     """
    #     parent_column = f"{data_resource_name}_id"
    #     relationship_column = f"{field}_id"

    #     for value in values:
    #         try:
    #             cols = {f"{parent_column}": id_value, f"{relationship_column}": value}

    #             insert = table.insert().values(**cols)
    #             session.execute(insert)
    #             session.commit()

    #         except Exception as e:
    #             # psycopg2.errors.UniqueViolation
    #             if e.code == "gkpj":
    #                 session.rollback()
    #             else:
    #                 raise InternalServerError()

    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def patch_many_one_secure(self, id: int, parent: str, child: str, values):
    #     """Wrapper method for patch many method.

    #     Args:
    #         id (int): Given ID of type parent
    #         parent (str): Type of parent
    #         child (str): Type of child
    #         values (list or int): list of values to patch

    #     Return:
    #         function: The wrapped method.
    #     """
    #     return self.patch_many_one(id, parent, child, values)

    # def patch_many_one(self, id: int, parent: str, child: str, values):
    #     """put data for a many to many relationship of a parent and child.

    #     Args:
    #         id (int): Given ID of type parent
    #         parent (str): Type of parent
    #         child (str): Type of child
    #         values (list or int): list of values to patch
    #     """
    #     try:
    #         session = Session()

    #         many_query = []
    #         junc_table = JuncHolder.lookup_table(parent, child)

    #         if junc_table is not None:
    #             if not isinstance(values, list):
    #                 values = [values]
    #             many_query.append([child, values, junc_table])

    #         for field, values, table in many_query:
    #             # TODO this should only insert when it doesnt already exist
    #             self.process_many_query(session, table, id, field, parent, values)

    #     except Exception:
    #         raise InternalServerError()

    #     finally:
    #         session.close()

    #     return self.get_many_one(id, parent, child)

    # # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    # def delete_many_one_secure(self, id: int, parent: str, child: str, values):
    #     return self.delete_many_one(id, parent, child, values)

    # def delete_many_one(self, id: int, parent: str, child: str, values):
    #     try:
    #         session = Session()
    #         junc_table = JuncHolder.lookup_table(parent, child)

    #         if not isinstance(values, list):
    #             values = [values]

    #         for value in values:
    #             parent_col = getattr(junc_table.c, f"{parent}_id")
    #             child_col = getattr(junc_table.c, f"{child}_id")
    #             del_st = junc_table.delete().where(
    #                 and_(parent_col == id, child_col == value)
    #             )

    #             res = session.execute(del_st)
    #             print(res)
    #             session.commit()

    #     except Exception:
    #         session.rollback()
    #         raise InternalServerError()

    #     finally:
    #         session.close()

    #     return self.get_many_one(id, parent, child)
    pass

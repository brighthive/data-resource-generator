from data_resource.api_manager.rest_functions import (
    put_resource_closure,
    get_resources_closure,
    get_resource_id_closure,
)


def resolver_stub(fn_name):
    """dynamic function resolver."""

    def get_stub():
        return {}, 200

    return get_stub

    # TODO add a route that triggers main ? is that a separate flask app?


def generate_fn_dict(base):

    fn_dict = {}

    all_resources = [c for c in base.classes]

    for index, orm_class in enumerate(all_resources):

        resource = orm_class.__name__.lower()

        fn_dict[f"get_{resource}"] = get_resources_closure(orm_class)
        fn_dict[f"get_{resource}_id"] = get_resource_id_closure(orm_class)
        fn_dict[f"post_{resource}"] = put_resource_closure(orm_class)
        fn_dict[f"put_{resource}_id"] = put_resource_closure(orm_class)
        fn_dict[f"delete_{resource}_id"] = lambda: None
        fn_dict[f"patch_{resource}_id"] = lambda: None

    return fn_dict


def fn_getter(base):
    fn_dict = generate_fn_dict(base)

    def get_fn_from_dict(function_name):
        try:
            return fn_dict[function_name]
        except KeyError as e:
            raise KeyError(f"Function '{str(e)}'not found in operationId.")

    return get_fn_from_dict

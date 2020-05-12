from data_resource.api_manager.rest_functions import get_people, put_people


def resolver_stub(fn_name):
    """dynamic function resolver."""

    def get_stub():
        return {}, 200

    return get_stub


fn_dict = {
    "get_people": lambda: get_people(),
    "get_people_id": lambda x: x,
    "post_people": lambda x, y: put_people(x, y),
    "put_people_id": lambda x: x,
    "delete_people_id": lambda x: x,
    "patch_people_id": lambda x: x,
}


def fn_getter(fn_dict):
    def get_fn_from_dict(function_name):
        try:
            return fn_dict[function_name]
        except KeyError as e:
            raise KeyError(f"Function '{str(e)}'not found in operationId.")

    return get_fn_from_dict

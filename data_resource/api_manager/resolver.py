from data_resource.api_manager.rest_functions import get_people, put_people


def resolver_stub(fn_name):
    """dynamic function resolver."""

    def get_stub():
        return {}, 200

    return get_stub


def generate_fn_dict(base):

    fn_dict = {}

    all_resources = [str(c.__name__) for c in base.classes]
    # ['People', 'Team', 'Order']

    for resource in all_resources:
        resource = resource.lower()
        fn_dict[f"get_{resource}"] = lambda: get_people()
        fn_dict[f"get_{resource}_id"] = lambda x: x
        fn_dict[f"post_{resource}"] = lambda *args: put_people(*args)
        fn_dict[f"put_{resource}_id"] = lambda x: x
        fn_dict[f"delete_{resource}_id"] = lambda x: x
        fn_dict[f"patch_{resource}_id"] = lambda x: x

    # fn_dict = {
    #     "get_people": lambda: get_people(),
    #     "get_people_id": lambda x: x,
    #     "post_people": lambda *args: put_people(*args),
    #     "put_people_id": lambda x: x,
    #     "delete_people_id": lambda x: x,
    #     "patch_people_id": lambda x: x,
    # }

    print(fn_dict)

    return fn_dict


def fn_getter(base):
    fn_dict = generate_fn_dict(base)

    def get_fn_from_dict(function_name):
        try:
            return fn_dict[function_name]
        except KeyError as e:
            raise KeyError(f"Function '{str(e)}'not found in operationId.")

    return get_fn_from_dict

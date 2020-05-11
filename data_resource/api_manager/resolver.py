def resolver_stub(fn_name):
    """dynamic function resolver."""

    def get_stub():
        return {}, 200

    return get_stub

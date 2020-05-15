from connexion.resolver import Resolver
from data_resource.generator.api_manager.resolver import fn_getter


def api_manager_run(
    base: dict = None,
    api_dict: dict = None,
    actually_run: bool = True,
    app: "Connexion Flask App" = None,
):
    _resolver = Resolver()
    _resolver.function_resolver = fn_getter(base)

    app.add_api(api_dict, resolver=_resolver)

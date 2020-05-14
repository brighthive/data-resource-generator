import connexion
from connexion.resolver import Resolver
from connexion import NoContent
from data_resource.api_manager import resolver_stub
from data_resource.api_manager.resolver import fn_getter


def api_manager_run(
    base: dict = None, api_dict: dict = None, actually_run: bool = True
):
    app = connexion.FlaskApp(__name__)

    app.app.config["base"] = base

    _resolver = Resolver()
    _resolver.function_resolver = fn_getter(base)

    # This should be run by route
    app.add_api(api_dict, resolver=_resolver)
    return app

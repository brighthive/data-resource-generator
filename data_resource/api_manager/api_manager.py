import connexion
from connexion.resolver import Resolver
from connexion import NoContent
from data_resource.api_manager import resolver_stub
from data_resource.api_manager.resolver import fn_getter


def run(base: dict = None, api_dict: dict = None, actually_run: bool = True):
    app = connexion.FlaskApp(__name__)

    app.app.config["base"] = base

    _resolver = Resolver()
    _resolver.function_resolver = fn_getter(base)

    app.add_api(api_dict, resolver=_resolver)
    return app

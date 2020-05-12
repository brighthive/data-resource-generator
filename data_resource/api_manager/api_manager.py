import connexion
from connexion.resolver import Resolver
from connexion import NoContent
from data_resource.api_manager import resolver_stub


def run(base: dict = None, api_dict: dict = None, actually_run: bool = True):
    app = connexion.FlaskApp(__name__)

    _resolver = Resolver()
    _resolver.function_resolver = resolver_stub

    app.add_api(api_dict, resolver=_resolver)
    return app

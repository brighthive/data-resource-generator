import connexion
from connexion.resolver import Resolver
from connexion import NoContent
from data_resource.api_manager import resolver_stub
from data_resource.api_manager.resolver import fn_getter


# Expects to have a data catalog when it starts...
# This should be triggered from a flask route once it has the items it needs
# This should trigger the data resource generator
def start_data_resource_generator(data_catalog, actually_run=False):
    data_dict = data_catalog["data"]
    api_dict = data_catalog["api"]["apiSpec"]

    # get models
    base = model_manager_run(data_dict)

    # make api
    app = api_manager_run(base=base, api_dict=api_dict)  # TODO refactor


# This adds the API -- TODO this should be called by admin
def api_manager_run(
    base: dict = None, api_dict: dict = None, actually_run: bool = True
):
    # app = connexion.FlaskApp(__name__)

    _resolver = Resolver()
    _resolver.function_resolver = fn_getter(base)

    # This should be run by route
    app.add_api(api_dict, resolver=_resolver)
    return app

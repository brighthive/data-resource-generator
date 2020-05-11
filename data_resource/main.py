import connexion
from connexion.resolver import Resolver


def run(api_dict: dict, actually_run=True):
    app = connexion.FlaskApp(__name__)

    _resolver = Resolver()
    _resolver.function_resolver = lambda x: lambda x: x

    # app.add_api('openapi.yaml', resolver=_resolver)
    app.add_api(api_dict, resolver=_resolver)
    application = app.app

    # @application.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()

    if actually_run:
        app.run(port=8081, use_reloader=False, threaded=False)
    else:
        return application

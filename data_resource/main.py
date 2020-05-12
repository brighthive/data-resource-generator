from data_resource.api_manager.api_manager import run
from data_resource.model_manager import model_manager_run
from data_resource.db.base import engine, Session


def start(data_catalog, actually_run=False):
    data_dict = data_catalog["data"]
    api_dict = data_catalog["api"]["apiSpec"]

    # get models
    base = model_manager_run(data_dict)

    # make api
    app = run(base=base, api_dict=api_dict)

    application = app.app

    @application.teardown_appcontext
    def shutdown_session(exception=None):
        pass

    if actually_run:
        app.run(port=8081, use_reloader=False, threaded=False)
    else:
        return application

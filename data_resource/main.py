from data_resource.api_manager.api_manager import run
from data_resource.model_manager import main
from data_resource.db.base import AutobaseSingleton


def start(data_catalog, actually_run=False):
    data_dict = data_catalog["data"]
    api_dict = data_catalog["api"]["apiSpec"]

    # get models
    main(data_dict)
    base = AutobaseSingleton.instance()

    # make api
    app = run(base=base, api_dict=api_dict, actually_run=False)

    application = app.app

    # @application.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()

    if actually_run:
        app.run(port=8081, use_reloader=False, threaded=False)
    else:
        return application

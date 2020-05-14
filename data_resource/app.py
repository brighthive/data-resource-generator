from data_resource.api_manager import api_manager_run
from data_resource.model_manager import model_manager_run
from data_resource.db import db_session


# Expects to have a data catalog when it starts...
# This should be triggered from a flask route once it has the items it needs
def start(data_catalog, actually_run=False):
    data_dict = data_catalog["data"]
    api_dict = data_catalog["api"]["apiSpec"]

    # get models
    base = model_manager_run(data_dict)

    # make api
    app = api_manager_run(base=base, api_dict=api_dict)

    application = app.app

    @application.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    if actually_run:
        app.run(debug=True, port=8081, use_reloader=False, threaded=False)
    else:
        return application

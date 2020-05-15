import connexion
from data_resource.admin.routes import tableschema_bp, tableschema_id_bp
from data_resource.db import db_session, admin_base, engine


def start(actually_run=False):
    app = connexion.FlaskApp(__name__)

    # register admin
    app.app.register_blueprint(tableschema_bp)
    app.app.register_blueprint(tableschema_id_bp)

    app.app.config["connexion_app"] = app
    application = app.app

    # import data_resource.admin.models
    # admin_base.metadata.create_all(engine)

    @application.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    if actually_run:
        app.run(debug=True, port=8081, use_reloader=False, threaded=False)
    else:
        return application

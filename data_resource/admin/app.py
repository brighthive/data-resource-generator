from data_resource.admin.routes import (
    tableschema_bp,
    tableschema_id_bp,
    swagger_bp,
    generator_bp,
)
from data_resource.db import db_session, admin_base, engine


def start(actually_run=True):
    app = connexion.FlaskApp(__name__)  # FIX

    # register admin
    app.app.register_blueprint(tableschema_bp)
    app.app.register_blueprint(tableschema_id_bp)
    app.app.register_blueprint(swagger_bp)
    app.app.register_blueprint(generator_bp)

    app.app.config["connexion_app"] = app  # FIX
    application = app.app  # FIX

    import data_resource.admin.models

    admin_base.metadata.create_all(engine)

    @application.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    if actually_run:
        app.run(port=8081, use_reloader=False, threaded=False)
    else:
        return app

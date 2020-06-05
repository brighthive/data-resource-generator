from data_resource.admin.routes import (
    tableschema_bp,
    tableschema_id_bp,
    swagger_bp,
    generator_bp,
)
from data_resource.db import db_session, admin_base, engine
from flask import Flask
from flask_restful import Api
from data_resource.logging.api_exceptions import handle_errors


def start(actually_run=True):
    app = Flask(__name__)
    api = Api(app)
    app.register_error_handler(Exception, handle_errors)

    # Register admin routes
    app.register_blueprint(tableschema_bp)
    app.register_blueprint(tableschema_id_bp)
    app.register_blueprint(swagger_bp)
    app.register_blueprint(generator_bp)

    # Save API to grab later at generation time
    app.config["api"] = api

    # Create the models
    import data_resource.admin.models  # noqa: F401

    admin_base.metadata.create_all(engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    if actually_run:
        app.run(port=8081, use_reloader=False, threaded=False)
    else:
        return app

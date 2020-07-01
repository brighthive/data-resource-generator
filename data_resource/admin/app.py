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
from flask_swagger_ui import get_swaggerui_blueprint
from data_resource.logging import LogFactory
import os
from data_resource.config import ConfigurationFactory


logger = LogFactory.get_console_logger("admin:app")


def create_app(actually_run=True):
    # TODO: this or env var
    dirname, _ = os.path.split(os.path.abspath(__file__))
    static_folder = os.path.abspath(
        os.path.join(dirname, "../../")
    )  # This should be the static folder at the root of the project folder

    app = Flask(__name__, static_url_path="", static_folder=static_folder)
    app.config.from_object(ConfigurationFactory.from_env())
    app.config["engine"] = engine

    app.register_error_handler(Exception, handle_errors)

    # SWAGGER UI
    SWAGGER_URL = "/ui"
    API_URL = "/static/swagger.json"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "BrightHive Data Resource"}
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    # Flask RESTFUL
    api = Api(app)

    # Register admin routes
    app.register_blueprint(tableschema_bp)
    app.register_blueprint(tableschema_id_bp)
    app.register_blueprint(swagger_bp)
    app.register_blueprint(generator_bp)

    # Save API to grab later at generation time
    app.config["api"] = api
    app.config["static_folder"] = static_folder  # TODO: this or env var

    # Create the models
    import data_resource.admin.models  # noqa: F401

    admin_base.metadata.create_all(engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.rollback()
        db_session.remove()

    if actually_run:
        app.run(host="0.0.0.0", port=8081, use_reloader=False, threaded=False)  # nosec
    else:
        return app

import os
import json
from data_resource.admin.routes import (
    tableschema_bp,
    tableschema_id_bp,
    swagger_bp,
    generator_bp,
)
from data_resource.db import db_session, admin_base, engine
from data_resource.logging.api_exceptions import handle_errors
from data_resource.logging import LogFactory
from data_resource.config import ConfigurationFactory
from data_resource.admin.safe_json_output import safe_json_dumps
from data_resource.generator.app import start_data_resource_generator
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, make_response
from flask_restful import Api


logger = LogFactory.get_console_logger("admin:app")


def create_app(actually_run=True):
    app = Flask(
        __name__,
        static_url_path="",
        static_folder=ConfigurationFactory.from_env().STATIC_FOLDER,
    )
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

    # Properly output all types
    @api.representation("application/json")
    def output_json(data, code, headers=None):
        resp = make_response(safe_json_dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

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
        db_session.rollback()
        db_session.remove()

    # Check if we need to turn on API/model already
    handle_existing_data_resource_schema(api)

    if actually_run:
        app.run(host="0.0.0.0", port=8081, use_reloader=False, threaded=False)  # nosec

    else:
        return app


def handle_existing_data_resource_schema(api: Api):
    if not os.path.exists("./static/data_resource_schema.json"):
        return

    logger.info("Found an existing data resource schema. Attempting to load it...")

    # TODO check for invalid doc
    with open("./static/data_resource_schema.json") as json_file:
        data_resource_schema = json.load(json_file)

    start_data_resource_generator(data_resource_schema, api, touch_database=False)

    logger.info("Loaded existing data resource schema.")

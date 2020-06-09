from data_resource.generator.api_manager import generate_api
from data_resource.generator.model_manager import create_models
from data_resource.logging import LogFactory
import json
from flask import current_app
import os


logger = LogFactory.get_console_logger("generator:app")


def save_swagger(swagger):
    static_folder = current_app.config["static_folder"]
    swagger_file = os.path.join(static_folder, "static/swagger.json")

    logger.info(swagger_file)
    with open(swagger_file, "w") as _file:
        _file.write(json.dumps(swagger))


def start_data_resource_generator(data_catalog, api):
    data_dict = data_catalog["data"]
    swagger = data_catalog["api"]["apiSpec"]

    # Generate ORM
    base = create_models(data_dict)

    # Generate APIs
    generate_api(base=base, swagger=swagger, api=api)

    save_swagger(swagger)

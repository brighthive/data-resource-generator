from data_resource.generator.api_manager import generate_api
from data_resource.generator.model_manager import create_models
from data_resource.shared_utils import LogFactory
import json
from flask import current_app
import os


logger = LogFactory.get_console_logger("generator:app")


def get_static_folder_from_app():
    static_folder = current_app.config["static_folder"]
    return static_folder


def save_swagger(swagger):
    static_folder = get_static_folder_from_app()
    swagger_file = os.path.join(static_folder, "static/swagger.json")

    logger.info(swagger_file)
    with open(swagger_file, "w") as _file:
        _file.write(json.dumps(swagger))


def start_data_resource_generator(data_catalog, api):
    data_dict = data_catalog["data"]
    try:
        relationships = data_catalog["data"]["relationships"]["manyToMany"]
    except KeyError:
        relationships = []

    swagger = data_catalog["api"]["apiSpec"]

    # Generate ORM
    base = create_models(data_dict)

    # Generate APIs
    generate_api(base=base, swagger=swagger, api=api, relationships=relationships)

    save_swagger(swagger)

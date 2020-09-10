from data_resource.config import ConfigurationFactory
from data_resource.generator.api_manager import generate_api
from data_resource.generator.model_manager import create_models
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.storage.storage_manager import StorageManager
from data_resource.shared_utils.validator import validate_data_resource_schema
import json
import os
from data_resource.shared_utils.api_exceptions import ApiError


logger = LogFactory.get_console_logger("generator:app")

storage = StorageManager(ConfigurationFactory.from_env())


def get_static_folder_from_app():
    static_folder = ConfigurationFactory.from_env().STATIC_FOLDER
    return static_folder


def save_swagger(swagger):
    static_folder = get_static_folder_from_app()
    swagger_file = os.path.join(static_folder, "static/swagger.json")

    logger.info(swagger_file)
    with open(swagger_file, "w") as _file:
        _file.write(json.dumps(swagger))


def start_data_resource_generator(full_schema, api, touch_database: bool = True):
    # Older versions used 'data_catalog'
    if "data_catalog" in full_schema:
        data_resource_schema = full_schema["data_catalog"]
    elif "data_resource_schema" in full_schema:
        data_resource_schema = full_schema["data_resource_schema"]
    else:
        raise ApiError(
            "Failed to load existing data resource schema. 'data_catalog' nor 'data_resource_schema' found at root."
        )

    if "ignore_validation" not in full_schema:
        validate_data_resource_schema(data_resource_schema)

    storage.save_data_resource_schema_data(full_schema)

    data_dict = data_resource_schema["data"]
    try:
        relationships = data_resource_schema["data"]["relationships"]["manyToMany"]
    except KeyError:
        relationships = []

    swagger = data_resource_schema["api"]["apiSpec"]

    # Generate ORM
    base = create_models(data_dict, touch_database=touch_database)

    # Generate APIs
    generate_api(base=base, swagger=swagger, api=api, relationships=relationships)

    save_swagger(swagger)

from data_resource.generator.api_manager import generate_api
from data_resource.generator.model_manager import create_models
from data_resource.logging import LogFactory
import json


logger = LogFactory.get_console_logger("generator:app")


def save_swagger(swagger):
    with open("./swagger.json", "w") as _file:
        _file.write(json.dumps(swagger))


def start_data_resource_generator(data_catalog, api):
    data_dict = data_catalog["data"]
    swagger = data_catalog["api"]["apiSpec"]

    # Generate ORM
    base = create_models(data_dict)

    # Generate APIs
    generate_api(base=base, swagger=swagger, api=api)

    save_swagger(swagger)

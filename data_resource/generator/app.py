from data_resource.generator.api_manager import generate_api
from data_resource.generator.model_manager import create_models


def start_data_resource_generator(data_catalog, app):
    data_dict = data_catalog["data"]
    api_dict = data_catalog["api"]["apiSpec"]

    # Generate ORM
    base = create_models(data_dict)

    # Generate APIs
    generate_api(base=base, api_dict=api_dict, app=app)

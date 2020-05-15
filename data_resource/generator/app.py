from data_resource.generator.api_manager import api_manager_run
from data_resource.generator.model_manager import create_models


def start_data_resource_generator(data_catalog, app):
    data_dict = data_catalog["data"]
    api_dict = data_catalog["api"]["apiSpec"]

    # get models
    base = create_models(data_dict)

    # add api
    api_manager_run(base=base, api_dict=api_dict, app=app)

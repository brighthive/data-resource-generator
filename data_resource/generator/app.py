from data_resource.generator.api_manager import generate_api
from data_resource.generator.model_manager import create_models


def start_data_resource_generator(data_catalog, api):
    data_dict = data_catalog["data"]
    data_resource_specs = data_catalog["api"]["apiSpec"]

    # Generate ORM
    base = create_models(data_dict)

    # Generate APIs
    generate_api(
        base=base, data_resource_specs=data_resource_specs, swagger=None, api=api
    )

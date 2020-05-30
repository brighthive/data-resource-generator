from data_resource.generator.api_manager import VersionedResource
from flask_restful import Api
from sqlalchemy.ext.declarative import DeclarativeMeta


def generate_api(base=None, data_resource_specs=None, swagger=None, api=None) -> None:
    # Generate REST API for resources
    for resource_orm in base.classes:
        generate_rest_api_routes(api, resource_orm)

    # Generate x:x REST API


def generate_rest_api_routes(api: Api, resource_orm: DeclarativeMeta) -> None:
    resource_name = resource_orm.__name__
    resources = [
        f"/{resource_name}",
        f"/{resource_name}/<int:id>",
        f"/{resource_name}/query",
    ]

    resource_api = VersionedResource(name=resource_name, resource_orm=resource_orm)

    for idx, route in enumerate(resources):
        api.add_resource(resource_api, route, endpoint=f"{resource_name}_ep_{idx}")

    return resources

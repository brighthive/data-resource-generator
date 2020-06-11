from data_resource.generator.api_manager import VersionedResource
from flask_restful import Api
from sqlalchemy.ext.declarative import DeclarativeMeta
from data_resource.logging import LogFactory
import re


logger = LogFactory.get_console_logger("generator:api-generator")


def convert_swagger_bracket_to_flask(route):
    """This will convert the swagger format of 'route/{id}' to the flask python
    format of 'route/<int:id>'."""
    output = re.sub(r"\{(.*)}", "<int:" + r"\1" + ">", route)
    return output


def get_enabled_routes_for_orm(resource_orm: object, swagger: dict) -> dict:
    """Given a resource orm (name) and a swagger spec, get all enabled
    routes."""
    routes = [route for route in swagger["paths"]]

    enabled_routes = {}

    for route in routes:
        verbs = [k for k, v in swagger["paths"][route].items()]
        verbs.sort()
        enabled_routes[convert_swagger_bracket_to_flask(route)] = verbs

    return enabled_routes


def generate_api(base=None, swagger: dict = None, api=None) -> None:
    # Generate REST API for resources
    for resource_orm in base.classes:
        enabled_routes = get_enabled_routes_for_orm(resource_orm, swagger)
        generate_rest_api_routes(api, resource_orm)

    # TODO Generate x:x REST API


def generate_rest_api_routes(api: Api, resource_orm: DeclarativeMeta) -> None:
    resource_name = resource_orm.__name__.lower()
    resources = [
        f"/{resource_name}",
        f"/{resource_name}/<int:id>",
        f"/{resource_name}/query",
    ]

    resource_api = type(
        resource_name,
        (VersionedResource,),
        {"name": resource_name, "resource_orm": resource_orm},
    )

    for idx, route in enumerate(resources):
        api.add_resource(resource_api, route, endpoint=f"{resource_name}_ep_{idx}")

    return resources

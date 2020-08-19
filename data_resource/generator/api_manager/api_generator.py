from data_resource.generator.api_manager import VersionedResource, VersionedResourceMany
from flask_restful import Api
from sqlalchemy.ext.declarative import DeclarativeMeta
from data_resource.shared_utils.log_factory import LogFactory
import re


logger = LogFactory.get_console_logger("generator:api-generator")


# util
def convert_swagger_bracket_to_flask(route):
    """This will convert the swagger format of 'route/{id}' to the flask python
    format of 'route/<int:id>'."""
    output = re.sub(r"\{(.*)}", "<int:" + r"\1" + ">", route)
    return output


# util
def get_enabled_routes_for_orm(swagger: dict) -> dict:
    """Given a resource orm (name) and a swagger spec, get all enabled
    routes."""
    routes = [route for route in swagger["paths"]]

    enabled_routes = {}

    for route in routes:
        verbs = [k for k, v in swagger["paths"][route].items()]
        verbs.sort()
        enabled_routes[convert_swagger_bracket_to_flask(route)] = verbs

    return enabled_routes


def generate_resource_based_routes(base, api: Api, enabled_routes) -> None:
    # Generate REST API for resources
    for resource_orm in base.classes:
        generate_rest_api_routes(api, resource_orm, enabled_routes)


def generate_relationship_based_routes(
    base, api: Api, relationships: dict, enabled_routes
) -> None:
    # Generate m:n REST API
    orm_relationships = generate_orm_relationship_list(base, relationships)

    for relationship in orm_relationships:
        generate_relationship_rest_api_routes(api, enabled_routes, relationship)

        reverse_relationship = reverse_relationship_orm_list(relationship)
        generate_relationship_rest_api_routes(api, enabled_routes, reverse_relationship)


def generate_api(
    base=None, swagger: dict = None, api: Api = None, relationships: list = []
) -> None:
    """Generates all routes."""
    enabled_routes = get_enabled_routes_for_orm(swagger)

    generate_resource_based_routes(base, api, enabled_routes)
    generate_relationship_based_routes(base, api, relationships, enabled_routes)


def generate_rest_api_routes(
    api: Api, resource_orm: DeclarativeMeta, enabled_routes: dict
) -> None:
    """Adds singular resource routes to API."""
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
        try:
            methods = enabled_routes[route]
        except KeyError:
            logger.warning(
                f"Route '{route}' not found in swagger. Therefore it is disabled. This may cause errors."
            )
            continue

        api.add_resource(
            resource_api, route, endpoint=f"{resource_name}_ep_{idx}", methods=methods
        )


def generate_relationship_rest_api_routes(
    api: Api, enabled_routes: dict, relationship: list
) -> None:
    """Adds relationship based routes to API."""
    first_orm = relationship[0]
    second_orm = relationship[1]
    first_orm_name = first_orm.__table__.name
    second_orm_name = second_orm.__table__.name

    resource_name = f"{first_orm_name}_{second_orm_name}"

    resource = [f"/{first_orm_name}/<int:id>/{second_orm_name}"]

    resource_api = type(
        resource_name,
        (VersionedResourceMany,),
        {"name": resource_name, "parent_orm": first_orm, "child_orm": second_orm},
    )

    for idx, route in enumerate(resource):
        try:
            methods = enabled_routes[route]
        except KeyError:
            logger.warning(
                f"Route '{route}' not found in swagger. Therefore it is disabled. This may cause errors."
            )
            continue

        api.add_resource(
            resource_api, route, endpoint=f"{resource_name}_ep_{idx}", methods=methods
        )


# util
def generate_orm_relationship_list(base, relationships: list) -> list:
    result = []

    for relationship in relationships:
        try:
            first_orm = getattr(base.classes, relationship[0].lower())
            second_orm = getattr(base.classes, relationship[1].lower())
        except AttributeError:
            logger.exception(
                "A referenced ORM within a relationship does not exist in base."
            )

        result.append([first_orm, second_orm])

    return result


# util
def reverse_relationship_orm_list(relationship: list) -> list:
    return sorted(relationship, key=lambda orm: str(orm.__table__.name), reverse=True)

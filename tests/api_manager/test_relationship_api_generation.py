from data_resource.generator.api_manager.api_generator import (
    generate_relationship_rest_api_routes,
    generate_relationship_based_routes,
    generate_orm_relationship_list,
    reverse_relationship_orm_list,
    generate_relationship_rest_api_routes,
)
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Table, MetaData


# Test util func
def convert_methods_to_test_format(item: dict) -> list:
    item.remove("OPTIONS")
    item.remove("HEAD")
    output = list(item)
    output.sort()
    return output


@pytest.mark.unit
def test_generate_relationship_rest_api_routes(
    empty_api, valid_people_orm, valid_orm_with_required_field
):
    relationships = [valid_people_orm, valid_orm_with_required_field]

    enabled_routes = {
        "/people/<int:id>/required": ["DELETE", "GET", "PATCH", "POST", "PUT"]
    }

    generate_relationship_rest_api_routes(empty_api, enabled_routes, relationships)

    result = {
        str(r): convert_methods_to_test_format(r.methods)
        for r in empty_api.app.url_map.iter_rules()
    }

    del result["/static/<path:filename>"]

    assert result == enabled_routes


@pytest.mark.unit
def test_generate_relationship_based_routes(valid_base, empty_api):
    relationships = [["people", "required"]]
    enabled_routes = {
        "/people/<int:id>/required": ["DELETE", "GET", "PATCH", "POST", "PUT"],
        "/required/<int:id>/people": ["DELETE", "GET", "PATCH", "POST", "PUT"],
    }

    generate_relationship_based_routes(
        valid_base, empty_api, relationships, enabled_routes
    )

    result = {
        str(r): convert_methods_to_test_format(r.methods)
        for r in empty_api.app.url_map.iter_rules()
    }

    del result["/static/<path:filename>"]

    assert result == enabled_routes


def test_generate_orm_relationship_list(
    valid_base, valid_people_orm, valid_orm_with_required_field
):
    relationships = [["people", "required"]]

    relationships_thing = [[valid_people_orm, valid_orm_with_required_field]]

    result = generate_orm_relationship_list(valid_base, relationships)

    assert result == relationships_thing


def test_reverse_orm_relationship_list(valid_people_orm, valid_orm_with_required_field):
    relationships = [valid_people_orm, valid_orm_with_required_field]
    relationships_reversed = [valid_orm_with_required_field, valid_people_orm]

    result = reverse_relationship_orm_list(relationships)

    assert result == relationships_reversed

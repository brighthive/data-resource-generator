from data_resource.generator.api_manager.api_generator import (
    generate_rest_api_routes,
    get_enabled_routes_for_orm,
    convert_swagger_bracket_to_flask,
)
from data_resource.generator.app import start_data_resource_generator, save_swagger
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer


@pytest.mark.unit
def test_generate_rest_api_routes(empty_api):
    test_base = declarative_base()
    enabled_routes = {
        "/team": ["DELETE", "GET", "PATCH", "POST", "PUT"],
        "/team/<int:id>": ["GET", "PATCH", "POST", "PUT"],
        "/team/query": ["GET", "POST", "PUT"],
    }

    class Team(test_base):
        __tablename__ = "it reads class name not tablename"
        id = Column(Integer, primary_key=True)

    generate_rest_api_routes(empty_api, Team, enabled_routes)

    def convert_methods_to_test_format(item: dict) -> list:
        item.remove("OPTIONS")
        item.remove("HEAD")
        output = list(item)
        output.sort()
        return output

    result = {
        str(r): convert_methods_to_test_format(r.methods)
        for r in empty_api.app.url_map.iter_rules()
    }

    del result["/static/<path:filename>"]

    assert result == enabled_routes


@pytest.mark.unit
def test_generate_saves_swagger_file(valid_base, empty_api, mocker):
    mocked_file = mocker.patch("data_resource.generator.app.open", mocker.mock_open())
    mocker.patch("os.path.join").return_value = "test"

    save_swagger({"hello": True})

    mocked_file.assert_called_once_with("test", "w")
    mocked_file().write.assert_called_once_with('{"hello": true}')


@pytest.mark.unit
def test_generate_serves_swagger_ui(valid_base, empty_api, mocker):
    create_models = mocker.patch("data_resource.generator.app.create_models")
    create_models.return_value = None
    generate_api = mocker.patch("data_resource.generator.app.generate_api")
    save_swagger = mocker.patch("data_resource.generator.app.save_swagger")

    start_data_resource_generator(
        {
            "ignore_validation": 1,
            "data_resource_schema": {"data": {}, "api": {"apiSpec": {}}},
        },
        {},
    )

    create_models.assert_called_once_with({}, touch_database=True)
    generate_api.assert_called_once_with(
        api={}, base=None, swagger={}, relationships=[]
    )
    save_swagger.assert_called_once_with({})


@pytest.mark.unit
def test_get_enabled_routes_for_orm():
    fake_swagger = {
        "paths": {
            "/test": {"GET": {}, "POST": {}, "PUT": {}, "PATCH": {}, "DELETE": {}},
            "/test/{id}": {"GET": {}, "POST": {}, "PUT": {}, "PATCH": {}},
            "/test/query": {"GET": {}, "POST": {}, "PUT": {}},
            "/people/{id}/test": {"GET": {}, "POST": {}},
            "/test/{id}/people": {"GET": {}, "POST": {}},
        }
    }
    expected_result = {
        "/test": ["DELETE", "GET", "PATCH", "POST", "PUT"],
        "/test/<int:id>": ["GET", "PATCH", "POST", "PUT"],
        "/test/query": ["GET", "POST", "PUT"],
        "/people/<int:id>/test": ["GET", "POST"],
        "/test/<int:id>/people": ["GET", "POST"],
    }

    result = get_enabled_routes_for_orm(fake_swagger)

    assert result == expected_result


@pytest.mark.unit
def test_convert_swagger_bracket_to_flask():
    result = convert_swagger_bracket_to_flask("/test/{id}")

    assert result == "/test/<int:id>"

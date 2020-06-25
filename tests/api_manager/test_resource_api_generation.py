from data_resource.generator.api_manager.api_generator import (
    generate_rest_api_routes,
    get_enabled_routes_for_orm,
    convert_swagger_bracket_to_flask,
)
from data_resource.generator.app import start_data_resource_generator, save_swagger
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Table, MetaData


# Given a tableschema assert the correct flask restful routes are generated
# use declarative base/table for ease instead of DeclarativeMeta
# TODO test the e2e case where the top level routes are not present in swagger.
@pytest.mark.unit
def test_generate_rest_api_routes(empty_api):
    test_base = declarative_base()
    enabled_routes = {
        "/team": ["DELETE", "GET", "PATCH", "POST", "PUT"],
        "/team/<int:id>": ["GET", "PATCH", "POST", "PUT"],
        "/team/query": ["GET", "POST", "PUT"],
    }

    class team(test_base):
        __tablename__ = "it reads class name not tablename"
        id = Column(Integer, primary_key=True)

    generate_rest_api_routes(empty_api, team, enabled_routes)

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

    # assert len(empty_api.endpoints) == 3
    # assert "team_ep_0" in empty_api.endpoints
    # assert "team_ep_1" in empty_api.endpoints
    # assert "team_ep_2" in empty_api.endpoints

    # # Assert all http verbs are present

    # for rule in empty_api.app.url_map.iter_rules():
    #     if "static" in repr(rule):
    #         continue

    #     assert all(
    #         [
    #             http_verb in rule.methods
    #             for http_verb in ["GET", "POST", "PATCH", "DELETE", "PUT"]
    #         ]
    #     )

    # Assert that all urls are correct
    # import pdb; pdb.set_trace()
    # url_for(rules)
    #         (Pdb) url_for(rule)
    # *** RuntimeError: Attempted to generate a URL without the application context being pushed. This has to be executed when application context is available.


@pytest.mark.unit
def test_generate_saves_swagger_file(valid_base, empty_api, mocker):
    mocker.patch("data_resource.generator.app.current_app")
    static_folder = mocker.patch(
        "data_resource.generator.app.get_static_folder_from_app"
    )
    static_folder.return_value = ""
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

    start_data_resource_generator({"data": {}, "api": {"apiSpec": {}}}, {})

    create_models.assert_called_once_with({})
    generate_api.assert_called_once_with(api={}, base=None, swagger={})
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

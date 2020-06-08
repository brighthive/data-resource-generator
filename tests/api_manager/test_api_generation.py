from data_resource.generator.api_manager.api_generator import generate_rest_api_routes
from data_resource.generator.app import start_data_resource_generator, save_swagger
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer


# Given a tableschema assert the correct flask restful routes are generated
# use declarative base/table for ease instead of DeclarativeMeta
@pytest.mark.unit
def test_generate_rest_api_routes(valid_base, empty_api):
    test_base = declarative_base()

    class team(test_base):
        __tablename__ = "it reads class name not tablename"
        id = Column(Integer, primary_key=True)

    generate_rest_api_routes(empty_api, team)

    assert len(empty_api.endpoints) == 3
    assert "team_ep_0" in empty_api.endpoints
    assert "team_ep_1" in empty_api.endpoints
    assert "team_ep_2" in empty_api.endpoints

    # Assert all http verbs are present
    for rule in empty_api.app.url_map.iter_rules():
        if "static" in repr(rule):
            continue

        assert all(
            [
                http_verb in rule.methods
                for http_verb in ["GET", "POST", "PATCH", "DELETE", "PUT"]
            ]
        )

        # Assert that all urls are correct
        # import pdb; pdb.set_trace()
        # url_for(rules)
        #         (Pdb) url_for(rule)
        # *** RuntimeError: Attempted to generate a URL without the application context being pushed. This has to be executed when application context is available.


@pytest.mark.unit
def test_generate_saves_swagger_file(valid_base, empty_api, mocker):
    # save_file = mocker
    mocked_file = mocker.patch("data_resource.generator.app.open", mocker.mock_open())
    fake_file_path = "./swagger.json"

    save_swagger({"hello": True})

    mocked_file.assert_called_once_with(fake_file_path, "w")
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

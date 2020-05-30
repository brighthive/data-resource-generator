from data_resource.generator.api_manager.temp import generate_rest_api_routes
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer


# Given a tableschema assert the correct flask restful routes are generated
def test_generate_rest_api_routes(valid_base, empty_api):
    test_base = declarative_base()

    class SomeClass(test_base):
        __tablename__ = "team"
        id = Column(Integer, primary_key=True)

    generate_rest_api_routes(empty_api, SomeClass)

    assert len(empty_api.endpoints) == 3
    assert "team_ep_0" in empty_api.endpoints
    assert "team_ep_1" in empty_api.endpoints
    assert "team_ep_2" in empty_api.endpoints

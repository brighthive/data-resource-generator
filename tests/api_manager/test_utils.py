import pytest
from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_json_from_object,
    _compute_offset,
    _compute_page,
    build_links,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer


@pytest.mark.unit
def test_compute_offset():
    assert _compute_offset(1, 20) == 0


@pytest.mark.unit
def test_compute_page():
    assert _compute_page(0, 20) == 1
    assert _compute_page(1, 20) == 1
    assert _compute_page(19, 20) == 1
    assert _compute_page(20, 20) == 2
    assert _compute_page(99, 20) == 5


@pytest.mark.unit
def test_build_json_from_object_works_with_orm():
    test_base = declarative_base()

    class Team(test_base):
        __tablename__ = "test"
        id = Column(Integer, primary_key=True)
        keepme = Column(Integer)
        deleteme = Column(Integer)

    row = Team(keepme="1", deleteme="1")
    restricted_fields = ["deleteme"]

    result = build_json_from_object(row, restricted_fields)

    assert result == {"keepme": "1"}  # ID won't init since we aren't commiting


@pytest.mark.unit
def test_build_json_from_object_works_with_dict():
    row = {"keepme": "1", "deleteme": "1"}
    restricted_fields = ["deleteme"]

    result = build_json_from_object(row, restricted_fields)

    assert result == {"keepme": "1"}


@pytest.mark.unit
def test_build_links():
    pass
    # "links": [
    #     {"rel": "self", "href": "/people?offset=0&limit=20"},
    #     {"rel": "first", "href": "/people?offset=0&limit=20"},
    #     {"rel": "last", "href": "/people?offset=0&limit=20"},

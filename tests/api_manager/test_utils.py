import pytest
from data_resource.generator.api_manager.v1_0_0.resource_utils import (
    build_json_from_object,
    _compute_offset,
    _compute_page,
    build_links,
)


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
def test_build_json_from_object():
    pass


@pytest.mark.unit
def test_build_links():
    pass

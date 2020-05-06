from data_resource.db.base import MetadataSingleton
import pytest


@pytest.mark.unit
def test_singleton_stores_metadata():
    MetadataSingleton.clear()

    MetadataSingleton.set_metadata("hi")

    assert MetadataSingleton.instance() != None

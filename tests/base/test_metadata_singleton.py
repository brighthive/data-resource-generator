from data_resource.db.base import MetadataSingleton
import pytest


@pytest.mark.unit
def test_singleton_stores_metadata():
    MetadataSingleton._clear()

    MetadataSingleton.set_metadata("hi")

    assert MetadataSingleton.instance() != None


@pytest.mark.unit
def test_errors_when_no_metadata():
    MetadataSingleton._clear()

    with pytest.raises(RuntimeError):
        MetadataSingleton.instance()

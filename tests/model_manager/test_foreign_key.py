import pytest
import tableschema
from data_resource.generator.model_manager.model_manager import (
    create_all_tables_from_schemas,
    get_table_names_and_descriptors,
    create_models,
)


@pytest.mark.unit
def test_fails_to_validate_when_a_fk_references_missing_descriptor_table(
    missing_foreign_key_table
):
    table_descriptors = missing_foreign_key_table["data"]

    with pytest.raises(tableschema.exceptions.ValidationError):
        _ = create_models(table_descriptors)


@pytest.mark.unit
def test_handles_fk_properly(valid_foreign_key):
    table_descriptors = valid_foreign_key["data"]

    base = create_models(table_descriptors)

    metadata = base.metadata

    assert "fk_relation" in metadata.tables
    assert "fk_table" in metadata.tables

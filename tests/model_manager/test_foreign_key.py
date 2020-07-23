import pytest
import tableschema
from data_resource.generator.model_manager.model_manager import (
    create_all_tables_from_schemas,
    get_table_names_and_descriptors,
    create_models,
    get_relationships_from_data_dict,
)


@pytest.mark.unit
def test_fails_to_validate_when_a_fk_references_missing_descriptor_table(
    MISSING_FOREIGN_KEY_TABLE
):
    table_descriptors = MISSING_FOREIGN_KEY_TABLE["data"]

    with pytest.raises(tableschema.exceptions.ValidationError):
        base = create_models(table_descriptors)


@pytest.mark.unit  # Does this requiredb tho?
def test_handles_fk_properly(VALID_FOREIGN_KEY):
    table_descriptors = VALID_FOREIGN_KEY["data"]

    base = create_models(table_descriptors)

    metadata = base.metadata

    assert "fk_relation" in metadata.tables
    assert "fk_table" in metadata.tables

    # Given a foreign key, ensure the proper FK relationship is present on the parent ORM

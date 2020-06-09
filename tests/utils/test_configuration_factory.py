"""Configuration Factory Unit Test."""

import pytest
from data_resource.config import ConfigurationFactory, InvalidConfigurationError


"""Application Configuration Unit Tests."""


@pytest.mark.unit
def test_load_configuration_from_env():
    """Load a configuration from the configuration factory.

    Ensure that a configuration object can be pulled from the
    environment.
    """

    configuration = ConfigurationFactory.from_env()
    assert hasattr(configuration, "POSTGRES_PORT")
    assert hasattr(configuration, "POSTGRES_HOSTNAME")


@pytest.mark.unit
def test_manually_request_configuration():
    """Manually specify a configuration.

    Ensure that bad or unknown configurations will throw an
    InvalidConfigurationError.
    """

    # bad configuration
    with pytest.raises(InvalidConfigurationError):
        ConfigurationFactory.get_config(config_type="UNDEFINED")

    # good configuration
    configuration = ConfigurationFactory.get_config(config_type="TEST")
    assert hasattr(configuration, "POSTGRES_PORT")
    assert hasattr(configuration, "POSTGRES_HOSTNAME")

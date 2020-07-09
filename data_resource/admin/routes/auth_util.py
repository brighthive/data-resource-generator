"""This is copy and pasted from the
generator.api_manager.core.versioned_resource code.

This allows the application to ignore auth if its running in test mode.
"""
from data_resource.logging import LogFactory
from data_resource.config import ConfigurationFactory
from brighthive_authlib import token_required


logger = LogFactory.get_console_logger("admin:authchecker")
provider = ConfigurationFactory.from_env().get_oauth2_provider()


def check_auth():
    """Raises authlib error if not authorized."""
    if not ConfigurationFactory.from_env().SKIP_AUTH_CHECK:
        # provider.validate_token()
        token_required(provider)(lambda: None)()

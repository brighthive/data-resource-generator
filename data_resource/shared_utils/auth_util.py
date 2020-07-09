"""This is copy and pasted from the
generator.api_manager.core.versioned_resource code.

This allows the application to ignore auth if its running in test mode.
"""
from data_resource.shared_utils.log_factory import LogFactory
from data_resource.config import ConfigurationFactory
from brighthive_authlib import token_required
import functools


logger = LogFactory.get_console_logger("admin:authchecker")
provider = ConfigurationFactory.from_env().get_oauth2_provider()


def _check_auth():
    """Raises authlib error if not authorized."""
    if not ConfigurationFactory.from_env().SKIP_AUTH_CHECK:
        # provider.validate_token()
        token_required(provider)(lambda: None)()


def check_auth(func):
    @functools.wraps(func)
    def check_auth_wrapper(*args, **kwargs):
        _check_auth()
        return func(*args, **kwargs)

    return check_auth_wrapper

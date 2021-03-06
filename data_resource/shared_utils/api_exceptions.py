from flask import jsonify
from werkzeug.exceptions import NotFound
from data_resource.shared_utils.log_factory import LogFactory
from brighthive_authlib import OAuth2ProviderError
import tableschema
import jsonschema

logger = LogFactory.get_console_logger("api-exceptions")


class DRApiError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        if errors is None:
            errors = []
        self.errors = errors

    def get_message(self):
        resp = {}
        resp["error"] = self.message

        if self.errors:
            resp["errors"] = self.errors

        return jsonify(resp)

    def get_status_code(self):
        return self.status_code


class ApiError(DRApiError):
    """Returns an error to the client and does not log the exception."""

    pass


class ApiUnhandledError(DRApiError):
    """Returns an error message to client and logs the exception."""

    pass


class InternalServerError(ApiUnhandledError):
    def __init__(self, status_code=500):
        message = "Internal Server Error"
        DRApiError.__init__(self, message, status_code)


class MethodNotAllowed(ApiError):
    def __init__(self):
        message = "Method not allowed"
        status_code = 405
        DRApiError.__init__(self, message, status_code)


class SchemaValidationFailure(ApiError):
    """Called when frictionless fails to validate."""

    def __init__(self):
        message = "Data schema validation error."
        status_code = 400
        DRApiError.__init__(self, message, status_code)


class NoRequestBodyFound(ApiError):
    def __init__(self):
        message = "No request body found."
        status_code = 400
        DRApiError.__init__(self, message, status_code)


def handle_errors(e):
    """Flask App Error Handler.

    A generic error handler for Flask applications.

    Note:
        This error handler is essentially to ensure that OAuth 2.0 authorization errors
        are handled in an appropriate fashion. The application configuration used when
        building the application must set the PROPOGATE_EXPECTIONS environment variable to
        True in order for the exception to be propogated.

    Return:
        dict, int: The error message and associated error code.
    """

    logger.exception("Encountered a handled error while processing a request.")

    if isinstance(e, OAuth2ProviderError):
        return jsonify({"message": "Access Denied"}), 401

    if isinstance(e, NotFound):
        return jsonify({"error": "Location not found"}), 404

    if isinstance(e, ApiError):
        return e.get_message(), e.get_status_code()

    if isinstance(e, tableschema.exceptions.ValidationError):
        return (
            jsonify(
                {
                    "message": "Tableschema validation failure.",
                    "error": [str(error) for error in e.errors],
                }
            ),
            400,
        )

    logger.exception("Encountered an unhandled error while processing a request.")

    if isinstance(e, ApiUnhandledError):
        return e.get_message(), e.get_status_code()

    return e.get_response()

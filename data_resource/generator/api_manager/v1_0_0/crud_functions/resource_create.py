# from tableschema import Schema, validate
from data_resource.db.base import db_session
from flask import Request
from data_resource.shared_utils.api_exceptions import ApiError
from data_resource.shared_utils.log_factory import LogFactory
from sqlalchemy.orm import class_mapper

logger = LogFactory.get_console_logger("generator:resource-create")


class ResourceCreate:
    def insert_one(self, resource_orm: object = None, request: Request = None):
        """Insert a new object.

        Args:
            resource_orm (object): SQLAlchemy ORM model.
            request_obj (flask.Request): HTTP request object.

        Return:
            dict, int: The response object and associated HTTP status code.
        """
        try:
            request_obj = request.json
        except Exception:
            raise ApiError("No request body found.", 400)

        # Validate our schema? This should have already occured # TODO add test for do not let unvalidated tableschema in
        # Check for required fields # Need tableschema to find required items... won't this be in the ORM? TODO check ORM for required? try except?
        try:
            new_object = resource_orm()
            for key, value in request_obj.items():
                setattr(
                    new_object, key, value
                )  # TODO is it a security concern to destructure user given items into sqlalchemy model like this?

            db_session.add(new_object)
            db_session.commit()

            # https://stackoverflow.com/questions/6745189/how-do-i-get-the-name-of-an-sqlalchemy-objects-primary-key
            pk_col = class_mapper(resource_orm).primary_key[0].name
            pk_value = getattr(new_object, pk_col)

            return {"message": "Successfully added new resource.", "id": pk_value}, 201
        except Exception:
            # wrong type -- psycopg2.errors.InvalidTextRepresentation
            # IntegrityError('(psycopg2.errors.NotNullViolation) null value in column "required" violates not-null constraint\nDETAIL:  Failing row contains (1, null, 1).\n')
            db_session.rollback()
            raise ApiError(f"Failed to create new resource.", 400)

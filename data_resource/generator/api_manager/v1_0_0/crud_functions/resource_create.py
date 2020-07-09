# from tableschema import Schema, validate
from data_resource.db.base import db_session
from flask import Request
from data_resource.shared_utils.api_exceptions import ApiError
from data_resource.shared_utils import LogFactory

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
        # _ = Schema(table_schema)
        # errors = []
        # accepted_fields = []

        # if not validate(table_schema):
        # raise SchemaValidationFailure()
        # raise

        # Check for required fields # Need tableschema to find required items... won't this be in the ORM? TODO check ORM for required? try except?
        # for field in table_schema["fields"]:
        # accepted_fields.append(field["name"])

        # if field["required"] and not field["name"] in request_obj.keys():
        # errors.append(f"Required field '{field['name']}' is missing.")

        # valid_fields = []

        # check if the value is in our tbl schema or assume its a many to many
        # removed code

        # TODO is it a security concern to destructure anything into sqlalchemy model?
        try:
            new_object = resource_orm()
            for key, value in request_obj.items():
                setattr(new_object, key, value)

            # try except here to catch errors? # TODO
            db_session.add(new_object)
            db_session.commit()

            # Can we get primary key(s) from sqlalchemy model?
            # https://stackoverflow.com/questions/6745189/how-do-i-get-the-name-of-an-sqlalchemy-objects-primary-key
            # id_value = getattr(new_object, table_schema["primaryKey"])
            id_value = new_object.id  # TODO

            # if there are many to many items they need to be built in orm and processed here # TODO FIX

            return {"message": "Successfully added new resource.", "id": id_value}, 201
        except Exception:
            # wrong type -- psycopg2.errors.InvalidTextRepresentation
            # IntegrityError('(psycopg2.errors.NotNullViolation) null value in column "required" violates not-null constraint\nDETAIL:  Failing row contains (1, null, 1).\n')
            db_session.rollback()
            raise ApiError("Failed to create new resource.", 400)

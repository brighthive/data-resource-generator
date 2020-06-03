from tableschema import Schema, validate
from data_resource.db.base import db_session


class ResourcePost:
    # @token_required(ConfigurationFactory.get_config().get_oauth2_provider())
    def insert_one_secure(self, *args, **kwargs):
        """Wrapper method for insert one method.

        Args:
            data_model (object): SQLAlchemy ORM model.
            data_resource_name (str): Name of the data resource.
            table_schema (dict): The Table Schema object to use for validation.
            request_obj (dict): HTTP request object.

        Return:
            function: The wrapped method.
        """
        return self.insert_one(*args, **kwargs)

    def insert_one(
        self,
        # data_model, data_resource_name, table_schema, request_obj
        resource_orm,
    ):
        """Insert a new object.

        Args:
            data_model (object): SQLAlchemy ORM model.
            data_resource_name (str): Name of the data resource.
            table_schema (dict): The Table Schema object to use for validation.
            request_obj (dict): HTTP request object.

        Return:
            dict, int: The response object and associated HTTP status code.
        """
        # get the request obj...
        try:
            request_obj = request_obj.json  # uh what
        except Exception:
            # raise ApiError("No request body found.", 400)
            raise

        # Validate our schema? This should have already occured # TODO add test for do not let unvalidated tableschema in
        _ = Schema(table_schema)
        errors = []
        accepted_fields = []

        if not validate(table_schema):
            # raise SchemaValidationFailure()
            raise

        # Check for required fields # Need tableschema to find required items... won't this be in the ORM? TODO check ORM for required? try except?
        for field in table_schema["fields"]:
            accepted_fields.append(field["name"])

            if field["required"] and not field["name"] in request_obj.keys():
                errors.append(f"Required field '{field['name']}' is missing.")

        valid_fields = []

        # check if the value is in our tbl schema or assume its a many to many
        # removed code

        # TODO is it a security concern to destructure anything into sqlalchemy model?
        try:
            new_object = resource_orm()
            for field in valid_fields:
                value = request_obj[field]
                setattr(new_object, field, value)
            db_session.add(new_object)
            db_session.commit()
            # Can we get primary key(s) from sqlalchemy model?
            # https://stackoverflow.com/questions/6745189/how-do-i-get-the-name-of-an-sqlalchemy-objects-primary-key
            id_value = getattr(new_object, table_schema["primaryKey"])

            # if there are many to many items they need to be built in orm and processed here # TODO FIX

            return {"message": "Successfully added new resource.", "id": id_value}, 201
        except Exception:
            # raise ApiUnhandledError("Failed to create new resource.", 400)
            raise

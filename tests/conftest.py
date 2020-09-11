import pytest
import os
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect
from data_resource import create_app
from data_resource.db import db_session
from data_resource.generator.app import start_data_resource_generator
from data_resource.generator.model_manager.model_manager import create_models
from flask_restful import Api
from flask import Flask
from tests.testing_schemas.default import DATA_DICTIONARY
from tests.testing_schemas.all_types import ALL_TYPES_DATA_DICTIONARY
from tests.testing_schemas.foreign_key import (
    _VALID_FOREIGN_KEY,
    _MISSING_FOREIGN_KEY_TABLE,
)


@pytest.fixture
def valid_data_dictionary():
    return DATA_DICTIONARY


@pytest.fixture
def missing_foreign_key_table():
    return _MISSING_FOREIGN_KEY_TABLE


@pytest.fixture
def valid_foreign_key():
    return _VALID_FOREIGN_KEY


class Database:
    def ping(self):
        db_session.query("1").all()
        return True

    def destory_db(self):
        try:
            db_session.execute("drop schema admin cascade")
            db_session.execute("create schema admin")
            db_session.execute("drop schema public cascade")
            db_session.execute("create schema public")
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()


@pytest.fixture(scope="function")
def empty_database():
    db = Database()
    db.destory_db()
    yield
    try:
        os.remove("./static/data_resource_schema.json")
    except (OSError, FileNotFoundError):
        pass

    try:
        os.remove("./static/swagger.json")
    except (OSError, FileNotFoundError):
        pass


@pytest.fixture
def valid_base(valid_data_dictionary, empty_database):
    table_descriptors = valid_data_dictionary["data"]
    base = create_models(table_descriptors)
    return base


@pytest.fixture
def valid_people_orm(valid_base):
    return getattr(valid_base.classes, "people")


@pytest.fixture
def valid_team_orm(valid_base):
    return getattr(valid_base.classes, "team")


@pytest.fixture
def valid_orm_with_required_field(valid_base):
    return getattr(valid_base.classes, "required")


@pytest.fixture(scope="function")
def database():
    db = Database()
    yield db


@pytest.fixture(scope="function")
def admin_e2e(empty_database):
    app = create_app(actually_run=False)
    return app.test_client()


@pytest.fixture(scope="function")
def generated_e2e(empty_database):
    # start the app
    app = create_app(actually_run=False)

    api = app.config["api"]

    with app.app_context():
        # skip generation process -- inject the data dict
        start_data_resource_generator(
            {"data_resource_schema": DATA_DICTIONARY, "ignore_validation": 1}, api
        )

    return app


@pytest.fixture(scope="function")
def all_types_generated_e2e(empty_database):
    # start the app
    app = create_app(actually_run=False)

    api = app.config["api"]

    with app.app_context():
        # skip generation process -- inject the data dict
        start_data_resource_generator(
            {"data_resource_schema": ALL_TYPES_DATA_DICTIONARY, "ignore_validation": 1},
            api,
        )

    return app


@pytest.fixture(scope="function")
def generated_e2e_client(generated_e2e):
    return generated_e2e.test_client()


@pytest.fixture(scope="function")
def all_types_generated_e2e_client(all_types_generated_e2e):
    return all_types_generated_e2e.test_client()


@pytest.fixture(scope="function")
def generated_e2e_database_inspector(generated_e2e):
    """This will trigger a generated e2e app but return a database inspection
    tool client."""
    return inspect(generated_e2e.config["engine"])


@pytest.fixture(scope="function")
def empty_api():
    app = Flask("what")
    api = Api(app)
    return api

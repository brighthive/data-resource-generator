import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect
from data_resource import start
from data_resource.db import db_session
from data_resource.generator.app import start_data_resource_generator
from data_resource.generator.model_manager.model_manager import create_models
from flask_restful import Api
from flask import Flask
from tests.schemas import DATA_DICTIONARY


@pytest.fixture
def VALID_DATA_DICTIONARY():
    return DATA_DICTIONARY


class Database:
    def ping(self):
        try:
            db_session.query("1").all()
            return True
        except OperationalError:
            raise

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


@pytest.fixture
def valid_base(VALID_DATA_DICTIONARY, empty_database):
    table_descriptors = VALID_DATA_DICTIONARY["data"]
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
    app = start(actually_run=False)
    return app.test_client()


@pytest.fixture(scope="function")
def generated_e2e(empty_database):
    # start the app
    app = start(actually_run=False)

    api = app.config["api"]

    with app.app_context():
        # skip generation process -- inject the data dict
        start_data_resource_generator(DATA_DICTIONARY, api)

    return app


@pytest.fixture(scope="function")
def generated_e2e_client(generated_e2e):
    return generated_e2e.test_client()


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

import os

import pymysql.cursors
import pytest
from flask import Flask as _Flask

from src.config import configuration
from src.di import get_injector
from src.infra.mysql.db import Base, engine, session
from src.infra.mysql.model.user import UserDTO
from src.presentation.api.route import json_api_routing


class Flask(_Flask):
    testing = True  # type: ignore
    secret_key = __name__  # type: ignore

    def make_response(self, rv):
        if rv is None:
            rv = ""

        return super().make_response(rv)


def run_sql(sql):
    connection = pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        charset="utf8",
    )
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.close()


def create_app():
    app = Flask(__name__)
    env = "testing"
    app.config.from_object(configuration[env])
    app.app_context().push()
    injector = get_injector()
    json_api_routing(app, injector)
    return app


@pytest.fixture(scope="session", autouse=True)
def scope_session():
    create_app()
    db_name = "pyconjp2025_test"
    os.environ["DB_NAME"] = db_name
    setup_db(db_name=db_name)
    setup_table()
    yield


def setup_db(db_name: str):
    run_sql(f"DROP DATABASE IF EXISTS {db_name}")
    run_sql(f"CREATE DATABASE IF NOT EXISTS `{db_name}` default character set utf8")


def setup_table():
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def scope_function():
    connection = engine.connect()
    transaction = connection.begin()
    session.configure(bind=connection)
    yield session
    transaction.rollback()
    connection.close()
    session.remove()


def fixture_user(id: int, auth0_id: str, name: str, email: str) -> UserDTO:
    x = UserDTO(id=id, auth0_id=auth0_id, name=name, email=email)
    session.add(x)
    session.flush()
    return x

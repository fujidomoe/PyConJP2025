import os

import pymysql.cursors
import pytest
from flask import Flask as _Flask
from sqlalchemy import create_engine

from src.config import configuration
from src.di import get_injector
from src.infra.mysql.db import Base, session
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
    os.environ["APP_ENV"] = "testing"
    # os.environ["DB_NAME"] = "pyconjp2025_test"
    # app.config["ENV"] = env
    app.config.from_object(configuration[env])
    app.app_context().push()
    injector = get_injector()
    json_api_routing(app, injector)
    return app


@pytest.fixture(scope="session", autouse=True)
def scope_session():
    app = create_app()
    app.testing = True
    database = "pyconjp2025_test"
    run_sql(f"DROP DATABASE IF EXISTS {database}")
    run_sql(f"CREATE DATABASE IF NOT EXISTS `{database}` default character set utf8")
    username = os.environ["DB_USER"]
    password = os.environ["DB_PASS"]
    hostname = os.environ["DB_HOST"]
    dsl = f"mysql+pymysql://{username}:{password}@{hostname}/{database}?charset=utf8mb4"

    engine = create_engine(dsl)

    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="function", autouse=True)
def scope_function():
    session.begin()
    yield
    session.rollback()
    session.close()
    session.remove()

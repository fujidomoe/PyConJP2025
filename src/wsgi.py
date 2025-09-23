import os
from flask import Flask
from src.config import configuration
from src.di import get_injector
from src.presentation.api.route import json_api_routing

app = Flask(__name__)


def init_app() -> Flask:
    env = os.environ.get("APP_ENV")
    app.config.from_object(configuration[env])
    app.config["JSON_AS_ASCII"] = False
    injector = get_injector()
    app.app_context().push()
    json_api_routing(app, injector)
    return app


@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = ["http://localhost:8090"]
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET"
    response.headers["Allow"] = "OPTIONS, GET"
    response.headers["Access-Control-Max-Age"] = "3600"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Server"] = None
    response.headers["Cache-Control"] = "no-store"
    return response


app = init_app()
if __name__ == "__main__":
    app.run()

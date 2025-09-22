import os
from flask import Flask, current_app, request, Blueprint, Flask, jsonify, make_response


app = Flask(__name__)


def init_app() -> Flask:
    app.config["JSON_AS_ASCII"] = False
    app.app_context().push()
    app.register_blueprint(healthcheck)
    return app

healthcheck = Blueprint("healthcheck", __name__)
@healthcheck.route("/healthcheck", methods=["GET"])
def health():
    result = {"healthcheck": "ok"}
    return make_response(jsonify(result), 200, {"Content-Type": "application/json"})


@app.after_request
def add_header(response):
    http_origin = request.environ.get("HTTP_ORIGIN")
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

from flask import Blueprint, Flask, jsonify, make_response
from src.presentation.api.view.user import UserMe
from src.application.usecase.user import UserMeInteractor


def json_api_routing(app: Flask, injector):
    app.register_error_handler(404, page_not_found)
    app.register_blueprint(healthcheck)

    app.add_url_rule(
        "/v1/users/me",
        view_func=UserMe.as_view("user_me"),
        defaults={"interactor": injector.get(UserMeInteractor)},
    )


healthcheck = Blueprint("healthcheck", __name__)
@healthcheck.route("/healthcheck", methods=["GET"])
def health():
    result = {"healthcheck": "ok"}
    return make_response(jsonify(result), 200, {"Content-Type": "application/json"})


def page_not_found(error):
    return make_response(jsonify({}), 404, {"Content-Type": "application/json"})

from contextvars import ContextVar

from flask import current_app, make_response
from flask.views import MethodView, request  # type: ignore
from injector import inject
from werkzeug.exceptions import BadRequest

from src.di import get_injector
from src.domain.model.user import User
from src.domain.repository.user import IUserRepo
from src.exception import (
    BadRequestHttpException,
    JsonHttpException,
    NotFoundHttpException,
)
from src.logger import LogContext, logger

me_context = ContextVar("me_context", default=None)  # type: ignore


class APIMethodView(MethodView):
    is_necessary_body = True

    def dispatch_request(self, *args, **kwargs):
        if request.method == "OPTIONS":
            return make_response({}, 200)

        try:
            client = current_app.config["AUTH_CLIENT"]
            auth0_id = client(request.headers.get("Authorization", None)).auth0_id
            m = get_injector().get(MeContext)
            me_context.set(m.generate(auth0_id))
            if self.is_necessary_body and request.method in ["POST", "PATCH"]:
                try:
                    _ = request.json
                except BadRequest as e:
                    raise BadRequestHttpException(messages=[e.description]) from e
            meth = getattr(self, request.method.lower(), None)
            if meth is None and request.method == "HEAD":
                meth = getattr(self, "get", None)
            assert meth is not None, f"Unimplemented method {request.method!r}"
            return meth(*args, **kwargs)
        except JsonHttpException as e:
            return make_response(e.errors, e.status_code, {"Content-Type": "application/json"})


class MeContext:
    @inject
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    def generate(self, auth0_id: str) -> User | None:
        user: User | None = self.user_repo.find_user_by_auth0_id(auth0_id)
        if user is None:
            raise NotFoundHttpException(["I can't find myself"])
        log_context = LogContext(f"user_id:{str(user.user_id)}")
        logger.addFilter(log_context)
        return user

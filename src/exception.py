from dataclasses import dataclass

from flask import jsonify


@dataclass
class ErrorFormat:
    message: str


class JsonHttpException(Exception):
    def __init__(self, errors, status_code):
        self.errors = jsonify({"errors": errors})
        self.status_code = status_code


class AuthHttpException(JsonHttpException):
    def __init__(self, messages: list[str], status_code=401):
        self.messages = messages
        errors = [ErrorFormat(message) for message in messages]
        super().__init__(errors, status_code)


class BadRequestHttpException(JsonHttpException):
    def __init__(self, messages: list[str], status_code=400):
        self.messages = messages
        errors = [ErrorFormat(message) for message in messages]
        super().__init__(errors, status_code)


class NotAuthorizedHttpException(JsonHttpException):
    def __init__(self, messages: list[str], status_code=403):
        self.messages = messages
        errors = [ErrorFormat(message) for message in messages]
        super().__init__(errors, status_code)


class NotFoundHttpException(JsonHttpException):
    def __init__(self, messages: list[str], status_code=404):
        self.messages = messages
        errors = [ErrorFormat(message) for message in messages]
        super().__init__(errors, status_code)

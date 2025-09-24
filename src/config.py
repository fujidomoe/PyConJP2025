import logging
from logging import DEBUG, INFO, StreamHandler

from src.infra.auth0.client import Auth0Client, IAuth0Client, StubAuth0Client


class Config:
    LOG_LEVEL = INFO
    LOG_HANDLER: logging.Handler = StreamHandler()
    AUTH_CLIENT: type[IAuth0Client] = Auth0Client


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    pass


class DevelopmentConfig(Config):
    LOG_LEVEL = DEBUG


class TestingConfig(Config):
    LOG_LEVEL = DEBUG
    AUTH_CLIENT = StubAuth0Client


configuration = {
    "production": ProductionConfig(),
    "staging": StagingConfig(),
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
}

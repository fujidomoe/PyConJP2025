import logging
from logging import DEBUG, INFO, StreamHandler


class Config:
    LOG_LEVEL = INFO
    LOG_HANDLER: logging.Handler = StreamHandler()


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    pass


class DevelopmentConfig(Config):
    LOG_LEVEL = DEBUG


class TestingConfig(Config):
    LOG_LEVEL = DEBUG


configuration = {
    "production": ProductionConfig(),
    "staging": StagingConfig(),
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
}

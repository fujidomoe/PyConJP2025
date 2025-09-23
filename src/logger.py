import logging
import os
from logging import Formatter, getLogger
from src.config import configuration

cfg = configuration[os.environ["APP_ENV"]]
logger = getLogger()
handler = cfg.LOG_HANDLER
log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
handler.setFormatter(Formatter(log_format))
logger.addHandler(handler)
logger.setLevel(cfg.LOG_LEVEL)

class LogContext(logging.Filter):
    def filter(self, record) -> bool:
        record.name = self.name
        return True

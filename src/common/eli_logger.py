
from singleton_class import Singleton
from insight_analysis.manager.env_manager import EnvManager
import logging
from logging.handlers import TimedRotatingFileHandler
from insight_analysis.constants import common_constants as comconstants
import os.path as ospath
import re


class EliLogger:

    __metaclass__ = Singleton

    _instance = None

    def __init__(self):
        env_manager = EnvManager()
        self.log_path = env_manager.get_log_path()
        if not self.log_path:
            self.log_path = ospath.dirname(__file__)
        self.logger_name = env_manager.get_log_names()
        self._config_log()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = EliLogger()
        return cls._instance

    def _config_log(self):
        logger = logging.getLogger(comconstants.LOG_NAME_ANALYSIS)
        logger.setLevel(logging.INFO)

        log_file_name = ospath.join(self.log_path, 'analysis')
        file_handler = TimedRotatingFileHandler(log_file_name, 'D', 1)
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(name)s]: %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    def _get_logger(self, log_name):
        if log_name not in self.logger_name:
            log_name = comconstants.LOG_NAME_ANALYSIS

        logger = logging.getLogger(log_name)
        return logger

    def info(self, message, log_name=comconstants.LOG_NAME_ANALYSIS):
        logger = self._get_logger(log_name)
        logger.info(message)

    def warn(self, message, log_name=comconstants.LOG_NAME_ANALYSIS):
        logger = self._get_logger(log_name)
        logger.warn(message)

    def error(self, message, log_name=comconstants.LOG_NAME_ANALYSIS):
        logger = self._get_logger(log_name)
        logger.error(message)

    def debug(self, message, log_name=comconstants.LOG_NAME_ANALYSIS):
        logger = self._get_logger(log_name)
        logger.debug(message)













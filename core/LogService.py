import time
import logging
import config
from logging.handlers import RotatingFileHandler


class LogService:

    def __init__(self, log_path):
        """
        Create logger object
        :param log_path:
        """
        self.logger = logging.getLogger("Rotating Log")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(RotatingFileHandler(log_path,
                                                   maxBytes=config.LOG_FILE_MAX_BYTE_SIZE,
                                                   backupCount=config.MAX_LOG_FILES))

    def log(self, message):
        """
        Logs a message to file
        :param message:
        :return:
        """
        self.logger.info('{} : {}'.format(time.strftime('%c'), message))
        print('{} : {}'.format(time.strftime('%c'), message))

    def log_error(self, message, error):
        """
        Logs both a message and an error object.
        :param message:
        :param error:
        :return:
        """
        self.logger.error('{} : {}'.format(time.strftime('%c'), message))
        print('{} : {}'.format(time.strftime('%c'), message))
        self.logger.error('{} : {}'.format(time.strftime('%c'), error.__str__()))
        print('{} : {}'.format(time.strftime('%c'), error.__str__()))

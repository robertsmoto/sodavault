import logging
from decouple import config


class SVlog:

    def __init__(self):
        self.err_cnt = 0

    def debug(self, msg: str, field=None):
        """Debug logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.INFO,
            filename=config('LOG_DEBUG_DIR')
            )
        if config('LOG_DEBUG', cast=bool):
            logging.info("%s, %s, %s", msg, field, type(field))
            print(f"INFO: {msg} {field} {type(field)}")
        return self

    def info(self, msg: str):
        """Info logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.INFO,
            filename=config('LOG_INFO_DIR')
            )
        if config('LOG_INFO', cast=bool):
            logging.info("%s", msg)
            print(f"INFO: {msg}")
        return self

    def warn(self, msg: str):
        """Warn logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.WARN,
            filename=config('LOG_WARN_DIR')
            )
        if config('LOG_WARN', cast=bool):
            logging.info("%s", msg)
            print(f"WARN: {msg}")
        return self

    def error(self, msg: str):
        """Error logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.ERROR,
            filename=config('LOG_ERROR_DIR')
            )
        self.err_cnt += 1
        if config('LOG_ERROR', cast=bool):
            logging.info("%s", msg)
            print(f"ERROR: {msg}")
        return self

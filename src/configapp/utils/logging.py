import logging
from decouple import config


class SVlog:

    def __init__(self):
        self.err_cnt = 0

    def info(self, msg: str):
        """Info logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.INFO,
            filename=config('LOG_INFO_DIR')
            )
        logging.info("%s", msg)
        if config('LOG_DEBUG', cast=bool):
            print(f"INFO: {msg}")
        return self

    def warn(self, msg: str):
        """Warn logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.WARN,
            filename=config('LOG_WARN_DIR')
            )
        logging.info("%s", msg)
        if config('LOG_DEBUG', cast=bool):
            print(f"WARN: {msg}")
        return self

    def error(self, msg: str):
        """Error logging message."""
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.ERROR,
            filename=config('LOG_ERROR_DIR')
            )
        logging.info("%s", msg)
        self.err_cnt += 1
        if config('LOG_DEBUG', cast=bool):
            print(f"ERROR: {msg}")
        return self

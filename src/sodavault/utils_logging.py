import logging


def svlog_info(msg: str) -> None:
    logging.info(msg)
    print("INFO", msg)
    return

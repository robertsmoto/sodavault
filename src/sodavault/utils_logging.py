import logging


def svlog_info(msg: str, field=None) -> None:
    if field:
        ftype = type(field)
        msg = f"{msg} field: {field} type: {ftype}"
    logging.info(msg)
    print("INFO", msg)
    return

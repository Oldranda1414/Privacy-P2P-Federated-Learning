import logging

def get_logger(name: str, fmt: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))

    logger.addHandler(handler)
    logger.propagate = False  # don’t also log through root
    return logger


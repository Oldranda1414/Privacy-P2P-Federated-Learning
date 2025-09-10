import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(f"%(asctime)s - {name} - %(levelname)s - %(message)s"))

        

    logger.addHandler(handler)
    logger.propagate = False  # don’t also log through root
    return logger


import logging


def create_logger(name):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename="foxtrot.log",
        filemode="w",
    )
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(console)
    return logger

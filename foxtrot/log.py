import logging


def create_logger(name):
    return logging.getLogger(name)


def init():
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
    logging.getLogger("").addHandler(console)


init()

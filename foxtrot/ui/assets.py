import os

import pyxel

from foxtrot import log

logger = log.create_logger(__name__)


def assets_path():
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, "..", "..", "assets")


def asset_path(path):
    return os.path.join(assets_path(), path)


def load_assets():
    path = asset_path("tiles.png")
    logger.debug("Loading gameplay asset: %s", path)
    pyxel.image(0).load(0, 0, path)

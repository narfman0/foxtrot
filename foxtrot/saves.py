import json
import os
from pathlib import Path

import dill

from foxtrot import log, settings

logger = log.create_logger(__name__)
home_dir = os.path.join(str(Path.home()), ".foxtrot")
save_dir = os.path.join(home_dir, "save")
settings_path = os.path.join(home_dir, "settings.json")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
extension = "fxt"


def list_saves():
    files = []
    for candidate in os.listdir(save_dir):
        if str(candidate).endswith(extension):
            files.append(candidate)
    return files


def load(name):
    path = "%s.%s" % (os.path.join(save_dir, name), extension)
    with open(path, "rb") as f:
        return dill.load(f)


def save(world):
    path = "%s.%s" % (os.path.join(save_dir, world.player.name), extension)
    with open(path, "wb") as f:
        dill.dump(world, f)


def load_settings():
    try:
        with open(settings_path) as f:
            updates = json.load(f)
            settings.settings.update(updates)
    except Exception as e:
        logger.warning("Failed to load settings with exception: %s", e)


def save_settings():
    with open(settings_path, "w") as outfile:
        json.dump(settings.settings, outfile)

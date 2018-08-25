import os
from pathlib import Path

import dill

save_dir = os.path.join(str(Path.home()), ".foxtrot", "save")
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

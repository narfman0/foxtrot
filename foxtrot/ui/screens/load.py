import functools
import pyxel

from foxtrot.models import saves
from foxtrot.ui.components.menu import Menu
from foxtrot.ui.screens.gameplay import GameplayScreen


class LoadScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        options = []
        for name in saves.list_saves():
            name = name[0 : -len(saves.extension) - 1]
            handler = functools.partial(self.handle_selection, name)
            options.append((name, handler))
        options.append(("Back", lambda: self.screen_manager.pop()))
        self.menu = Menu(options)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.screen_manager.pop()
        self.menu.update()

    def draw(self):
        self.menu.draw()

    def handle_selection(self, name):
        world = saves.load(name)
        self.screen_manager.push(GameplayScreen(self.screen_manager, world=world))

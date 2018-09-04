import pyxel

from foxtrot import saves
from foxtrot.ui.components.menu import Menu
from foxtrot.ui.screens.gameplay import GameplayScreen
from foxtrot.ui.screens.load import LoadScreen


TITLE = "Foxtrot"


class MenuScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.menu = Menu(
            options=[
                ("New Game", self.start_game),
                ("Load Game", self.load_game),
                ("Quit", self.quit),
            ]
        )

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.quit()
        self.menu.update()

    def draw(self):
        self.menu.draw()
        pyxel.text(
            pyxel.width / 2 - len(TITLE) * 4 / 2, 64, TITLE, pyxel.frame_count % 16
        )

    def load_game(self):
        self.screen_manager.push(LoadScreen(self.screen_manager))

    def start_game(self):
        self.screen_manager.push(GameplayScreen(self.screen_manager))

    def quit(self):
        saves.save_settings()
        pyxel.quit()

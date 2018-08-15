import pyxel

from foxtrot.components.menu import Menu
from foxtrot.screens.gameplay import GameplayScreen


TITLE = "Main Screen"


class MenuScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.menu = Menu(
            [("Start Game", self.start_game), ("Quit", lambda: pyxel.quit())]
        )

    def update(self):
        self.menu.update()

    def draw(self):
        self.menu.draw()
        pyxel.text(
            pyxel.width / 2 - len(TITLE) * 4 / 2, 64, TITLE, pyxel.frame_count % 16
        )

    def start_game(self):
        self.screen_manager.push(GameplayScreen(self.screen_manager))

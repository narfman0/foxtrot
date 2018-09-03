import pyxel

from foxtrot import log

logger = log.create_logger(__name__)


class Menu:
    border_width = 4
    text_height = 8
    text_color = 2
    text_color_selected = 7

    def __init__(self, listener=None, text=None, options=None, background_color=None):
        self.listener = listener
        self.text = text
        self.options = options
        self.current_option = 0
        self.background_color = background_color
        text_rows = (1 if text else 0) + len(options)
        self.height = text_rows * self.text_height + self.border_width
        lengths = [len(option[0]) for option in options]
        if self.text:
            lengths.append(len(self.text))
        self.width = max(lengths) * 4 + self.border_width
        logger.debug("Created menu with options: %s", options)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            text, handler = self.get_option(self.options[self.current_option])
            logger.debug("Menu selected option: %s", text)
            if self.listener:
                self.listener.handle_selection(self.current_option)
            if handler:
                handler()
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.current_option == len(self.options) - 1:
                self.current_option = 0
            else:
                self.current_option += 1
        if pyxel.btnp(pyxel.KEY_UP):
            if self.current_option == 0:
                self.current_option = len(self.options) - 1
            else:
                self.current_option -= 1

    def draw(self):
        if self.background_color:
            x1 = pyxel.width // 2 - self.width // 2
            y1 = pyxel.height // 2 - self.height // 2
            pyxel.rect(x1, y1, x1 + self.width, y1 + self.height, self.background_color)
        index = 0
        if self.text:
            x = pyxel.width / 2 - len(self.text) * 2 + self.border_width // 2
            y = pyxel.height / 2 - self.height // 2 + self.border_width // 2
            pyxel.text(x, y, self.text, self.text_color)
            index += 1
        for text, handler in self.get_options():
            color = (
                self.text_color_selected
                if index - (1 if self.text else 0) == self.current_option
                else self.text_color
            )
            x = pyxel.width / 2 - len(text) * 2 + self.border_width // 2
            y = (
                pyxel.height / 2
                + self.text_height * index
                - self.height // 2
                + self.border_width // 2
            )
            pyxel.text(x, y, text, color)
            index += 1

    def get_options(self):
        for option in self.options:
            yield self.get_option(option)

    def get_option(self, option):
        if isinstance(option, str):
            return (option, None)
        else:
            return option

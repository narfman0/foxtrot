import pyxel

from foxtrot import log, util

logger = log.create_logger(__name__)


class Menu:
    border_width = 4
    text_height = 8
    text_width = 4
    text_color = 2
    text_color_selected = 7

    def __init__(self, listener=None, text=None, options=None, background_color=None):
        self.listener = listener
        self.text = util.split_string(text, pyxel.width // 2 / self.text_width) if text else []
        self.options = options
        self.current_option = 0
        self.background_color = background_color
        self.height = self.get_height()
        self.width = self.get_width()
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
            for text_index, text in enumerate(self.text):
                x = pyxel.width / 2 - len(text) * 2 + self.border_width // 2
                y = (
                    pyxel.height / 2
                    + self.text_height * text_index
                    - self.height // 2
                    + self.border_width // 2
                )
                pyxel.text(x, y, text, 15)
                index += 1
        for text, handler in self.get_options():
            color = (
                self.text_color_selected
                if index - (len(self.text) if self.text else 0) == self.current_option
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

    def get_height(self):
        text_rows = len(self.text) + len(self.options)
        return text_rows * self.text_height + self.border_width

    def get_width(self):
        lengths = [len(option[0]) for option in self.options]
        if self.text:
            lengths.append(max(len(text) for text in self.text))
        return max(lengths) * self.text_width + self.border_width

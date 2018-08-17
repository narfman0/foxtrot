import pyxel

from foxtrot.models.world import World


TILE_WIDTH = 8


class GameplayScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.world = World()

    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.screen_manager.pop()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.world.player.y -= 1
        if pyxel.btnp(pyxel.KEY_UP):
            self.world.player.y += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.world.player.x -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.world.player.x += 1

    def draw(self):
        text = "x,y: %d,%d" % (self.world.player.x, self.world.player.y)
        pyxel.text(pyxel.width / 2 - len(text) * 2, 4, text, pyxel.frame_count % 16)
        index = 1
        for chunk in self.world.chunks:
            color = 8
            if self.chunk_visible(chunk):
                self.draw_chunk(chunk, index)
                color = 10
            text = "x,y: %d,%d" % (chunk.x, chunk.y)
            pyxel.text(pyxel.width / 2 - len(text) * 2, 4 + 8 * index, text, color)
            index += 1
        self.draw_player()

    def draw_player(self):
        pyxel.circ(pyxel.width / 2, pyxel.height / 2, TILE_WIDTH // 2, 7)

    def draw_chunk(self, chunk, index):
        for tile_x, tile_y, tile in chunk.tiles:
            world_x = (chunk.x - chunk.size // 2 + tile_x) - self.world.player.x
            world_y = (chunk.y - chunk.size // 2 + tile_y) - self.world.player.y
            self.draw_tile(world_x, world_y, str(tile))

    def chunk_visible(self, chunk):
        cull_distance = pyxel.width // TILE_WIDTH
        return (
            abs(self.world.player.x - chunk.x) - chunk.size // 2 < cull_distance
            and abs(self.world.player.y - chunk.y) - chunk.size // 2 < cull_distance
        )

    def draw_tile(self, x, y, tile):
        """ Draw a tile given world coordinates x, y """
        render_x = x * TILE_WIDTH + pyxel.width // 2
        render_y = -y * TILE_WIDTH + pyxel.height // 2
        pyxel.text(render_x - 1, render_y - 2, str(tile), 9)

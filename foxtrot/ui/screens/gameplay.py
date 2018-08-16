import pyxel

from foxtrot.models.world import World


TILE_WIDTH = 8
CHUNK_CULL_DISTANCE = 32


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
        self.draw_player()
        index = 1
        for x, y, chunk in self.world.chunks:
            text = "x,y: %d,%d" % (x, y)
            pyxel.text(pyxel.width / 2 - len(text) * 2, 4 + 8 * index, text, 8)
            self.draw_chunk(x, y, chunk, index)
            index += 1

    def draw_player(self):
        pyxel.circ(pyxel.width / 2, pyxel.height / 2, TILE_WIDTH // 2, 7)

    def draw_chunk(self, x, y, chunk, index):
        if (
            abs(self.world.player.x - x) - chunk.size // 2 > CHUNK_CULL_DISTANCE
            or abs(self.world.player.y - y) - chunk.size // 2 > CHUNK_CULL_DISTANCE
        ):
            return
        # draw chunk :)
        for chunk_x, chunk_y, tile in chunk.tiles:
            world_x = (x - chunk.size // 2 + chunk_x) - self.world.player.x
            world_y = (y - chunk.size // 2 + chunk_y) - self.world.player.y
            self.draw_tile(world_x, world_y, str(tile))

    def draw_tile(self, x, y, tile):
        """ Draw a tile given world coordinates x, y """
        render_x = x * TILE_WIDTH + pyxel.width // 2
        render_y = -y * TILE_WIDTH + pyxel.height // 2
        pyxel.text(render_x - 1, render_y - 2, str(tile), 9)

import pyxel

from foxtrot.models import NPC, World
from foxtrot.ui.components import debug


TILE_WIDTH = 8
DEBUG = True


class GameplayScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.world = World()

    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.screen_manager.pop()
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x, self.world.player.y - NPC.VELOCITY_IN_GRAVITY
                ):
                    self.world.player.y -= NPC.VELOCITY_IN_GRAVITY

            else:
                self.world.player.dy -= NPC.EVA_ACCELERATION
        if pyxel.btn(pyxel.KEY_UP):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x, self.world.player.y + NPC.VELOCITY_IN_GRAVITY
                ):
                    self.world.player.y += NPC.VELOCITY_IN_GRAVITY
            else:
                self.world.player.dy += NPC.EVA_ACCELERATION
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x - NPC.VELOCITY_IN_GRAVITY, self.world.player.y
                ):
                    self.world.player.x -= NPC.VELOCITY_IN_GRAVITY
            else:
                self.world.player.dx -= NPC.EVA_ACCELERATION
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x + NPC.VELOCITY_IN_GRAVITY, self.world.player.y
                ):
                    self.world.player.x += NPC.VELOCITY_IN_GRAVITY
            else:
                self.world.player.dx += NPC.EVA_ACCELERATION
        self.world.update()

    def draw(self):
        for chunk in self.world.chunks:
            if self.world.chunk_active(chunk):
                self.draw_chunk(chunk)
        if DEBUG:
            debug.draw(self)
        self.draw_player()

    def draw_player(self):
        pyxel.circ(pyxel.width / 2, pyxel.height / 2, TILE_WIDTH // 2, 7)

    def draw_chunk(self, chunk):
        for tile_x, tile_y, tile in chunk.tiles:
            world_x = (chunk.x - chunk.size // 2 + tile_x) - self.world.player.x
            world_y = (chunk.y - chunk.size // 2 + tile_y) - self.world.player.y
            self.draw_tile(world_x, world_y, str(tile))

    def draw_tile(self, x, y, tile):
        """ Draw a tile given world coordinates x, y """
        render_x = x * TILE_WIDTH + pyxel.width // 2
        render_y = -y * TILE_WIDTH + pyxel.height // 2
        pyxel.text(render_x - 1, render_y - 2, str(tile), 9)

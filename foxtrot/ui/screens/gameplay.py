import pyxel

from foxtrot.models import NPC, RoomType, Ship, World
from foxtrot.ui.components import debug
from foxtrot.ui.components.menu import Menu


TILE_WIDTH = 8
DEBUG = True


class GameplayScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.world = World()
        self.menus = []

    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.screen_manager.pop()
        if self.menus:
            menu = self.menus[-1]
            menu.update()
        else:
            self.handle_movement_input()
        if pyxel.btnp(pyxel.KEY_E):
            if self.world.player.in_room and type(self.world.player.chunk) is Ship:
                room_type = getattr(self.world.player.room, "type", None)
                if room_type is RoomType.BRIDGE:
                    destinations = self.world.get_destinations(
                        self.world.player.x, self.world.player.y
                    )
                    origin = self.world.player.chunk
                    options = [
                        (
                            destination.name,
                            lambda: self.handle_flight(origin, destination),
                        )
                        for destination in destinations
                    ]
                    menu = Menu(options, background_color=1)
                    self.menus.append(menu)
        self.world.update()

    def handle_flight(self, origin, destination):
        self.menus.pop()
        self.world.fly(origin, destination)

    def handle_movement_input(self):
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

    def draw(self):
        for chunk in self.world.chunks:
            if self.world.chunk_active(chunk):
                self.draw_chunk(chunk)
        if DEBUG:
            debug.draw(self)
        self.draw_player()
        if self.world.player.in_chunk:
            text = self.world.player.chunk.name
            if self.world.player.in_room and hasattr(self.world.player.room, "type"):
                text += ", " + self.world.player.room.type.name
            pyxel.text(pyxel.width / 2 - len(text) * 2, 4, text, 12)
        for menu in self.menus:
            menu.draw()

    def draw_player(self):
        pyxel.circ(pyxel.width / 2, pyxel.height / 2, TILE_WIDTH // 2, 7)

    def draw_chunk(self, chunk):
        for tile_x, tile_y, tile in chunk.tiles:
            world_x = (chunk.x - chunk.width // 2 + tile_x) - self.world.player.x
            world_y = (chunk.y - chunk.height // 2 + tile_y) - self.world.player.y
            self.draw_tile(world_x, world_y, str(tile))

    def draw_tile(self, x, y, tile):
        """ Draw a tile given world coordinates x, y """
        render_x = x * TILE_WIDTH + pyxel.width // 2
        render_y = -y * TILE_WIDTH + pyxel.height // 2
        pyxel.text(render_x + 2, render_y - 5, str(tile), 9)

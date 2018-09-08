import functools

import pyxel

from foxtrot import log, math, saves
from foxtrot.models import Colony, NPC, Planet, RoomType, Ship, World
from foxtrot.models.missions import triggers
from foxtrot.ui.components import debug
from foxtrot.ui.components.menu import Menu


TILE_WIDTH = 8
logger = log.create_logger(__name__)


class GameplayScreen:
    def __init__(self, screen_manager, world=None):
        self.screen_manager = screen_manager
        self.menus = []
        self.debug = True
        distance_hint = pyxel.width // 2 // TILE_WIDTH
        if world:
            self.world = world
            world.listener = self
        else:
            self.world = World(listener=self).create(
                tile_width=TILE_WIDTH, distance_hint=distance_hint
            )

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            options = [
                ("Yes", self.handle_save),
                ("No", self.screen_manager.pop),
                ("Cancel", self.menus.pop),
            ]
            menu = Menu(
                text="Save game as %s?" % self.world.player.name,
                options=options,
                background_color=1,
            )
            self.menus.append(menu)
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.screen_manager.pop()
        if self.menus:
            menu = self.menus[-1]
            menu.update()
        else:
            self.handle_movement_input()
        if self.debug and pyxel.btnp(pyxel.KEY_M) and pyxel.btn(pyxel.KEY_LEFT_SHIFT):
            if isinstance(self.world.missions[0].trigger, triggers.RoomTrigger):
                for chunk in self.world.chunks:
                    for room in chunk.tiles.rooms:
                        if room == self.world.missions[0].trigger.room:
                            room_x, room_y = chunk.get_room_position(room)
                            self.world.player.x = room_x
                            self.world.player.y = room_y
            self.world.missions[0].trigger = triggers.BooleanTrigger()
            logger.info("Current mission trigger swapped to activate next check")
        if pyxel.btnp(pyxel.KEY_E) and self.world.player.in_room:
            room_type = getattr(self.world.player.room, "type", None)
            if type(self.world.player.chunk) is Ship:
                if room_type is RoomType.BRIDGE:
                    x, y = self.world.player.position
                    destinations = self.world.get_destinations(x, y)
                    origin = self.world.player.chunk
                    options = []
                    for destination in destinations:
                        cost = math.travel_cost((origin.x, origin.y), (destination.x, destination.y))
                        if not self.world.fuel >= cost:
                            continue
                        handler = functools.partial(
                            self.handle_travel, origin, destination
                        )
                        text = '%s for %dF' % (destination.name, cost)
                        options.append((text, handler))
                    options.append(("Back", self.menus.pop))
                    menu = Menu(text="Travel to:", options=options, background_color=1)
                    self.menus.append(menu)
            elif type(self.world.player.chunk) is Colony:
                if room_type is RoomType.CONTROL:
                    options = []
                    room_options = [
                        (RoomType.CARGO, 1000),
                        (RoomType.CREW, 1200),
                        (RoomType.FARM, 1500),
                        (RoomType.MINING, 2500),
                        (RoomType.WEAPONS, 3000),
                        (RoomType.REFINERY, 5000),
                    ]
                    for room_type, cost in room_options:
                        if self.world.salvage < cost:
                            break
                        handler = functools.partial(self.handle_buildout, room_type, cost)
                        text = '%s: %dS' % (room_type.name, cost)
                        options.append((text, handler))
                    options.append(("Back", self.menus.pop))
                    menu = Menu(text="Buildout colony with:", options=options, background_color=1)
                    self.menus.append(menu)
            elif type(self.world.player.chunk) is Planet:
                if room_type is RoomType.TRADER:
                    options = []
                    salvage_cost = self.world.player.room.salvage_cost
                    for amount in [1, 5, 10, 20]:
                        if self.world.credits < amount * salvage_cost:
                            break
                        handler = functools.partial(self.handle_purchase_salvage, amount, salvage_cost)
                        text = "%d Salvage, $%d" % (amount, salvage_cost * amount)
                        options.append((text, handler))
                    fuel_cost = self.world.player.room.fuel_cost
                    for amount in [1, 5, 10, 20]:
                        if self.world.credits < amount * fuel_cost:
                            break
                        handler = functools.partial(self.handle_purchase_fuel, amount, fuel_cost)
                        text = "%d Fuel, $%d" % (amount, fuel_cost * amount)
                        options.append((text, handler))
                    options.append(("Back", self.menus.pop))
                    menu = Menu(text="Purchase:", options=options, background_color=1)
                    self.menus.append(menu)
        if pyxel.btnp(pyxel.KEY_F2):
            self.debug = not self.debug
        if self.debug and pyxel.btnp(pyxel.KEY_F3):
            self.world.credits += 1000
        if self.debug and pyxel.btnp(pyxel.KEY_F4):
            self.world.salvage += 1000
        if self.debug and pyxel.btnp(pyxel.KEY_F5):
            self.world.fuel += 100
        self.world.update()

    def handle_purchase_fuel(self, amount, cost):
        self.world.fuel += amount
        self.world.credits -= (cost * amount)
        logger.info('Purchased %d fuel for $%d', amount, cost * amount)
        self.menus.pop()

    def handle_purchase_salvage(self, amount, cost):
        self.world.salvage += amount
        self.world.credits -= (cost * amount)
        logger.info('Purchased %d salvage for $%d', amount, cost * amount)
        self.menus.pop()

    def handle_save(self):
        saves.save(self.world)
        self.screen_manager.pop()

    def handle_travel(self, origin, destination):
        self.menus.pop()
        self.world.travel(origin, destination)

    def handle_buildout(self, room_type, cost):
        self.menus.pop()
        self.world.buildout(room_type, cost)

    def handle_movement_input(self):
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x, self.world.player.y - NPC.VELOCITY_IN_GRAVITY
                ) or (self.debug and pyxel.btn(pyxel.KEY_LEFT_SHIFT)):
                    self.world.player.y -= NPC.VELOCITY_IN_GRAVITY

            else:
                self.world.player.dy -= NPC.EVA_ACCELERATION
        if pyxel.btn(pyxel.KEY_UP):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x, self.world.player.y + NPC.VELOCITY_IN_GRAVITY
                ) or (self.debug and pyxel.btn(pyxel.KEY_LEFT_SHIFT)):
                    self.world.player.y += NPC.VELOCITY_IN_GRAVITY
            else:
                self.world.player.dy += NPC.EVA_ACCELERATION
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x - NPC.VELOCITY_IN_GRAVITY, self.world.player.y
                ) or (self.debug and pyxel.btn(pyxel.KEY_LEFT_SHIFT)):
                    self.world.player.x -= NPC.VELOCITY_IN_GRAVITY
            else:
                self.world.player.dx -= NPC.EVA_ACCELERATION
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.world.player.in_chunk:
                if self.world.player.chunk.passable(
                    self.world.player.x + NPC.VELOCITY_IN_GRAVITY, self.world.player.y
                ) or (self.debug and pyxel.btn(pyxel.KEY_LEFT_SHIFT)):
                    self.world.player.x += NPC.VELOCITY_IN_GRAVITY
            else:
                self.world.player.dx += NPC.EVA_ACCELERATION

    def draw(self):
        for chunk in self.world.chunks:
            if self.chunk_active(chunk):
                self.draw_chunk(chunk)
        if self.debug:
            debug.draw(self)
        self.draw_player()
        self.draw_hud()
        for menu in self.menus:
            menu.draw()

    def draw_hud(self):
        if self.world.player.in_chunk:
            text = self.world.player.chunk.name
            if self.world.player.in_room and hasattr(self.world.player.room, "type"):
                room_type = self.world.player.room.type
                text += ", " + (
                    self.world.company_name
                    if room_type == RoomType.CORPORATION
                    else room_type.name
                )
            pyxel.text(pyxel.width / 2 - len(text) * 2, 4, text, 12)
        text = "Credits: $%d" % self.world.credits
        pyxel.text(4, 4, text, 12)
        text = "Salvage: %d" % self.world.salvage
        pyxel.text(4, 4 + 8, text, 12)
        text = "Fuel: %d" % self.world.fuel
        pyxel.text(4, 4 + 16, text, 12)

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
        # easy avoiding rendering offscreen. note: we can know this beforehand
        if (
            render_x > -TILE_WIDTH
            and render_x < pyxel.width + TILE_WIDTH
            and render_y > -TILE_WIDTH
            and render_y < pyxel.height + TILE_WIDTH
        ):
            pyxel.text(render_x + 2, render_y - 5, str(tile), 9)

    def chunk_active(self, chunk):
        """ Check if chunk should be active or not """
        return (
            abs(self.world.player.x - chunk.x) - chunk.width // 2
            < pyxel.width // 2 // TILE_WIDTH
            and abs(self.world.player.y - chunk.y) - chunk.height // 2
            < pyxel.height // 2 // TILE_WIDTH
        )

    def create_menu(self, text, options):
        menu = Menu(listener=self, text=text, options=options, background_color=1)
        self.menus.append(menu)

    def handle_selection(self, selection):
        """ Handle menu selection. selection is the index of menu item
        selected. """
        self.menus.pop()

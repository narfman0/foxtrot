import pyxel


def draw(screen):
    draw_chunk_locations(screen)
    draw_chunk_tile(screen)
    draw_player_location(screen)


def draw_player_location(screen):
    text = "%d,%d" % (screen.world.player.x, screen.world.player.y)
    pyxel.text(4, pyxel.height - 12, text, 13)


def draw_chunk_locations(screen):
    index = 0
    for chunk in screen.world.chunks:
        color = 8
        if screen.world.chunk_active(chunk):
            color = 10
        text = "%s x,y: %d,%d" % (type(chunk).__name__, chunk.x, chunk.y)
        pyxel.text(pyxel.width - len(text) * 4 - 4, 4 + 8 * index, text, color)
        index += 1


def draw_chunk_tile(screen):
    if screen.world.player.in_chunk:
        chunk = screen.world.player.chunk
        player_rel_x = int(screen.world.player.x) - chunk.x + chunk.width // 2
        player_rel_y = int(screen.world.player.y) - chunk.y + chunk.height // 2
        text = "%s x,y length: %d,%d player_rel: %d,%d" % (
            type(chunk).__name__,
            len(chunk.tiles.grid),
            len(chunk.tiles.grid[0]),
            player_rel_x,
            player_rel_y,
        )
        pyxel.text(4, 4, text, 7)
        try:
            text = "tile: " + str(chunk.tiles.grid[player_rel_x][player_rel_y])
            pyxel.text(4, 20, text, 7)
        except:
            pass

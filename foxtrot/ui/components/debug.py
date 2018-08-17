import pyxel


def draw(screen):
    draw_chunk_locations(screen)
    draw_chunk_tile(screen)
    draw_player_location(screen)


def draw_player_location(screen):
    text = "player x,y: %d,%d" % (screen.world.player.x, screen.world.player.y)
    pyxel.text(pyxel.width / 2 - len(text) * 2, 4, text, pyxel.frame_count % 16)


def draw_chunk_locations(screen):
    index = 1
    for chunk in screen.world.chunks:
        color = 8
        if screen.world.chunk_active(chunk):
            color = 10
        text = "chunk x,y: %d,%d" % (chunk.x, chunk.y)
        pyxel.text(pyxel.width / 2 - len(text) * 2, 4 + 8 * index, text, color)
        index += 1


def draw_chunk_tile(screen):
    if screen.world.player.in_chunk:
        chunk = screen.world.player.chunk
        player_rel_x = int(screen.world.player.x + .5) - chunk.x + chunk.size // 2
        player_rel_y = int(screen.world.player.y + .5) - chunk.y + chunk.size // 2
        text = "chunk x,y length: %d,%d player_rel: %d,%d" % (
            len(chunk.tiles.grid),
            len(chunk.tiles.grid[0]),
            player_rel_x,
            player_rel_y,
        )
        pyxel.text(4, 4, text, 7)
        try:
            text = "tile: " + str(chunk.tiles.grid[player_rel_x][player_rel_y])
            pyxel.text(4, 12, text, 7)
        except:
            pass

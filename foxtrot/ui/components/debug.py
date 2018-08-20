import pyxel


def draw(screen):
    draw_chunk_locations(screen)
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

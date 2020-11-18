import tcod as libtcod

# Renders all listed entities
def render_all(con, entities, screen_width, screen_height):
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# Clears all listed entities
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# Draws entity
def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# Erases entity
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

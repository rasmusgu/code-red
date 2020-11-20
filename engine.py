import tcod as libtcod

from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap

def main():   
    # Size of the screen
    screen_width = 80
    screen_height = 50
    
    # Size of the map
    map_width = 80
    map_height = 45
    
    # Room variables
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

    # font settings
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    # creates the "screen", initialises its size, title and whether it's fullscreen
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    # new console
    con = libtcod.console.Console(screen_width, screen_height)
    
    # Initialise game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # input storage variables
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # main loop
    while not libtcod.console_is_window_closed():
        
        #captures inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        # renders all called upon entities
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        # refreshes screen
        libtcod.console_flush()
        
        # makes so that characters don't leave trails
        clear_all(con, entities)

        # new variable for handle_keys function from other file
        action = handle_keys(key)
        
        # actions
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        
        if move:
            # moves the character
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            # exits the game
            return True
        
        if fullscreen:
            # makes game fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()

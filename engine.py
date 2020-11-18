import tcod as libtcod
from input_handlers import handle_keys

def main():
    
    # variables
    screen_width = 80
    screen_height = 50
    
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # font settings
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    # creates the "screen", initialises its size, title and whether it's fullscreen
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    # new console
    con = libtcod.console_new(screen_width, screen_height)

    # input storage variables
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # main loop
    while not libtcod.console_is_window_closed():
        
        #captures inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        # sets character colour
        libtcod.console_set_default_foreground(con, libtcod.white)
        # character console, xy, character, ?
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        # screen variables
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        # refreshes screen
        libtcod.console_flush()
        
        # ? removes old character ?
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)
        
        # new variable for handle_keys function from other file
        action = handle_keys(key)
        
        # actions
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        
        # moves the character
        if move:
            dx, dy = move
            player_x += dx
            player_y += dy
        
        # exits the game
        if exit:
            return True
        
        # makes game fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()

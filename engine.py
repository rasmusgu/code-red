import tcod as libtcod

from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap
from fov_functions import initialise_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from death_functions import kill_monster, kill_player


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
    
    # Field of view (fov) variables
    # 0 is the default algorithm tcod uses. Experiment!
    fov_algorithm = 0
    # lights up walls that are seen
    fov_light_walls = True
    # how far you can see
    fov_radius = 10
    
    max_monsters_per_room = 3

    # Colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    # font settings
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    
    # creates the "screen", initialises its size, title and whether it's fullscreen
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    # new console
    con = libtcod.console.Console(screen_width, screen_height)
    
    # Initialise game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    
    # Variable for whether fov check is necessary or not. For example, when standing still or attacking, fov recalculation is unnecessary. "True" by default because we need to compute fov as the game starts
    fov_recompute = True
    
    fov_map = initialise_fov(game_map)

    # input storage variables
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game state variable
    game_state = GameStates.PLAYERS_TURN

    # main loop
    while not libtcod.console_is_window_closed():
        
        #captures inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # renders all called upon entities
        render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        
        # Set to False after initial render_all
        fov_recompute = False

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
        
        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            # moves the character
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

                else:
                    player.move(dx, dy)
                    fov_recompute = True
                
                game_state = GameStates.ENEMY_TURN

        if exit:
            # exits the game
            return True
        
        if fullscreen:
            # makes game fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_results in enemy_turn_results:
                        message = enemy_turn_results.get('message')
                        dead_entity = enemy_turn_results.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)
                            
                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()

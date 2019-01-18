import constants
import utility
import vision

def fill_combat_map(robot):
    pos_x = robot.me.pos_x
    pos_y = robot.me.pos_y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    combat_map_length = len(robot.combat_map)

    min_x = pos_x - (combat_map_length - 1)/2
    max_x = pos_x + (combat_map_length - 1)/2
    min_y = pos_y - (combat_map_length - 1)/2
    max_y = pos_y + (combat_map_length - 1)/2

    visible_units = robot.get_visible_robots()
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)

    for iter_i in range(len(combat_map_length)):
        for iter_j in range(len(combat_map_length)):
            # Impassable or out of bounds
            if utility.is_out_of_bounds(combat_map_length, iter_j + min_x, iter_i + min_y) or passable_map[iter_i][iter_j]!= 1:
                robot.combat_map[iter_i][iter_j] = -1

    for unit in visible_units:
        if unit['team']  == robot.me['team']:
            # 1 to 4096
            robot.combat_map[unit['y'] - min_x][unit['y'] - min_y] = unit['id']
        else:
            # -2 to -4097
            robot.combat_map[unit['y'] - min_x][unit['y'] - min_y] = -unit['id'] - 1


    # robot.combat_map
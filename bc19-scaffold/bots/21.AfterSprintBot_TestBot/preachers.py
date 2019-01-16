import utility
import combat_module

def preacher(robot):
    return preacher_move(robot)

def preacher_move(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = utility.random_cells_around()

    preacher_attack_aggr_mode = combat_module.give_military_command(robot)
    if preacher_attack_aggr_mode != None:
        return preacher_attack_aggr_mode

    if utility.fuel_less_check(robot):
        return None

    for direction in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.move(direction[1], direction[0])

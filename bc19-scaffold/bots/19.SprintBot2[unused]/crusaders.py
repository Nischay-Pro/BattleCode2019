import utility
import combat_module

def crusader(robot):
    return crusader_move(robot)

def crusader_move(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    directions = utility.random_cells_around()

    crusader_is_attacking_or_aggressive_moving = combat_module.give_military_command(robot)
    if crusader_is_attacking_or_aggressive_moving != None:
        return crusader_is_attacking_or_aggressive_moving
    for direction in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.move(direction[1], direction[0])

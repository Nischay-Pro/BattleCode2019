import constants
import utility


def _build_manager_castle(robot):
    None
    #TODO Need to add castle production logic

def _build_manager_church(robot):
    unit_type = constants.unit_prophet
    pos_x = robot.me.x
    pos_y = robot.me.y
    occupied_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()
    directions = utility.random_cells_around()
    for direction in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.build_unit(unit_type, direction[1], direction[0])
    robot.log("No space to build units anymore for churches")
    return None

def default_production_order(robot):
    unit_type = robot.me.unit
    if unit_type == constants.unit_church:
        return _build_manager_church(robot)
    if unit_type == constants.unit_castle:
        return _build_manager_castle(robot)
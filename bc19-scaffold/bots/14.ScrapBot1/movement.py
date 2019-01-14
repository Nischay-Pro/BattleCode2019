import communications
import pathfinding
import constants
import utility
# from datetime import datetime

def calculate_dir(start, target):
    dx = target[0] - start[0]
    dy = target[1] - start[1]
    if dx < 0:
        dx = -1
    elif dx > 0:
        dx = 1
    
    if dy < 0:
        dy = -1
    elif dy > 0: 
        dy = 1
    
    return (dx, dy)
    
def is_completely_surrounded(robot):
    passable_map = robot.get_passable_map()
    pos_x = robot.me.x
    pos_y = robot.me.y
    occupied_map = robot.get_visible_robot_map()
    if robot.me.unit == constants.unit_crusader:
        for direction in constants.crusader_move_directions:
            if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
                return False
    else:
        for direction in constants.non_crusader_move_directions:
            if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
                return False
    return True
# TODO - Sentry formation near pilgrims and churches (is atleast 2 tiles away), form fit over impassale terrain
# TODO - Rush archers, kite mages using knights
# TODO - Make formation movements

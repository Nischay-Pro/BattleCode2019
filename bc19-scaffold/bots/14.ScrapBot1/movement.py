import communications
import pathfinding
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

def move_to_specified_position(robot, unit_signal):
    nearest_mine = communications.convert_message_to_position(unit_signal)
    if nearest_mine:
        # a1 = datetime.now()
        # a1.microsecond
        # robot.log("astar_time 1 " + str(a1))
        tile_to_move_to = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), nearest_mine, 2)
        # a2 = datetime.now()
        # robot.log("astar_time 2 " + str(a2))
    if tile_to_move_to == None:
        return None
    else:
        return tile_to_move_to[0]

# TODO - Sentry formation near pilgrims and churches (is atleast 2 tiles away), form fit over impassale terrain
# TODO - Rush archers, kite mages using knights
# TODO - Make formation movements

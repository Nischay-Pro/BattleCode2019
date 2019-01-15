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

def move_to_destination(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    occupied_map = robot.get_visible_robot_map()

    # robot.log("Current mov destination is " + str(robot.current_move_destination))
    # robot.log("Current location is " + str((robot.me.x, robot.me.y)))

    if robot.current_move_destination != None:
        final_pos_x = robot.current_move_destination[0]
        final_pos_y = robot.current_move_destination[1]
        if utility.is_cell_occupied(occupied_map, final_pos_x, final_pos_y):
            return None # Can't apply pathfinding if final location is visible and occupied

        if robot.mov_path_between_location_and_destination != None or len(robot.mov_path_between_location_and_destination) != 0:
            assumed_pos_x = robot.mov_path_between_location_and_destination[robot.mov_path_index][0]
            assumed_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index][1]
            if assumed_pos_x != pos_x or assumed_pos_y != pos_y:
                robot.mov_path_between_location_and_destination = None

        # Initialise path
        if robot.mov_path_between_location_and_destination == None:
            robot.mov_path_between_location_and_destination = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
            robot.mov_path_index = 0
            new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
            # robot.log("First block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
            return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)

        # Reached end of move list
        elif len(robot.mov_path_between_location_and_destination) - 1 == robot.mov_path_index + 1:
            robot.mov_path_index = robot.mov_path_index + 1
            # Reached destination
            if str(robot.mov_path_between_location_and_destination[robot.mov_path_index]) == str(robot.current_move_destination):
                new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
                # robot.log("Second block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
                if not utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y):
                    robot.pilgrim_mine_ownership = robot.current_move_destination
                    robot.current_move_destination = None
                    robot.mov_path_index = 0
                    return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
            # Computed list ended
            else:
                robot.mov_path_between_location_and_destination = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
                robot.mov_path_index = 0
                new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
                # robot.log("Third block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
                return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
        # In middle of the list
        else:
            robot.mov_path_index = robot.mov_path_index + 1
            new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
            # robot.log("Fouth block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
            # TODO -Try to add fuzzy jump or something (This is when some tile occupies the place you want to move to)
            if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y):
                robot.mov_path_between_location_and_destination = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
                robot.mov_path_index = 0
                new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
                # robot.log("Fifth block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
            return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
    # Conditions not satisfied
    return None

def find_dockspots(robot, depot):
    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    directions = constants.directions

    depot_x = depot.x
    depot_y = depot.y

    dockspots = []

    for direction in directions:
        if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, depot_x + direction[0], depot_y + direction[1]):
            dockspots.append((depot_x + direction[0], depot_y + direction[1]))

    return dockspots

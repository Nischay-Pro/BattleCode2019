import communications
import pathfinding
import constants
import utility
import check

# from datetime import datetime

def is_relatively_surrounded(robot):
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)

    pos_x = robot.me.x
    pos_y = robot.me.y
    locked_spaces = 0
    if robot.me.unit == constants.unit_crusader:
        for direction in constants.crusader_move_directions:
            if utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0]) or passable_map[pos_y + direction[0]][pos_x + direction[1]] != 1:
                locked_spaces += 1
        return locked_spaces/len(constants.crusader_move_directions)
    else:
        for direction in constants.non_crusader_move_directions:
            if utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0]) or passable_map[pos_y + direction[0]][pos_x + direction[1]] != 1:
                locked_spaces +=1
        return locked_spaces/len(constants.non_crusader_move_directions)

def is_completely_surrounded(robot):
    locked_spaces_ratio = is_relatively_surrounded(robot)
    # robot.log(str(locked_spaces_ratio))
    if locked_spaces_ratio < 1:
        return False
    return True

# TODO - Sentry formation near pilgrims and churches (is atleast 2 tiles away), form fit over impassale terrain
# TODO - Rush archers, kite mages using knights
# TODO - Make formation movements

def move_to_destination(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()

    if robot.current_move_destination != None:
        # robot.log("Current mov destination is " + str(robot.current_move_destination))
        # robot.log("Current location is " + str((robot.me.x, robot.me.y)))
        final_pos_x = robot.current_move_destination[0]
        final_pos_y = robot.current_move_destination[1]

        # Can't apply pathfinding if final location is visible and occupied
        if utility.is_cell_occupied(occupied_map, final_pos_x, final_pos_y):
            robot.current_move_destination = None
            utility.default_movement_variables(robot)
            utility.default_movement_variables(robot)
            return None
        # We already at the final location
        elif len(robot.mov_path_between_location_and_destination) == 1:
            robot.current_move_destination = None # Reached destination
            utility.default_movement_variables(robot)
            utility.default_movement_variables(robot)
            return None
        # Another way to check the above
        elif robot.me.x == robot.current_move_destination[0] and robot.me.y == robot.current_move_destination[1]:
            robot.current_move_destination = None
            utility.default_movement_variables(robot)
            return None

        if robot.mov_path_between_location_and_destination != None or len(robot.mov_path_between_location_and_destination) != 0:
            if len(robot.mov_path_between_location_and_destination[robot.mov_path_index]) == 2:
                assumed_pos_x = robot.mov_path_between_location_and_destination[robot.mov_path_index][0]
                assumed_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index][1]
                if assumed_pos_x != pos_x or assumed_pos_y != pos_y:
                    utility.default_movement_variables(robot)

        if robot.bug_nav_counter > 5:
            robot.mov_path_between_location_and_destination = None
        elif robot.bug_nav_counter > 10:
            robot.current_move_destination = None
            utility.default_movement_variables(robot)
            return None

        # Initialise path
        if robot.mov_path_between_location_and_destination == None:
            utility.default_movement_variables(robot)
            robot.mov_path_between_location_and_destination, robot.burned_out = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
            robot.mov_path_index = 0
            new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
            # robot.log("First block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
            # TRAVIS MOVE CHECK 3
            return check.move_check(robot, new_pos_x - pos_x, new_pos_y - pos_y, 3)
        # Reached end of move list
        elif len(robot.mov_path_between_location_and_destination) - 1 == robot.mov_path_index + 1:
            robot.mov_path_index = robot.mov_path_index + 1
            new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
            # robot.log("Second block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
            if str(robot.mov_path_between_location_and_destination[robot.mov_path_index]) != str(robot.current_move_destination):
                utility.default_movement_variables(robot)
            if not utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y):
                robot.current_move_destination = None
                # TRAVIS MOVE CHECK 4
                return check.move_check(robot, new_pos_x - pos_x, new_pos_y - pos_y, 4)
        # In middle of the list
        else:
            # robot.log("Current location is " + str((robot.me.x, robot.me.y)))
            if robot.bug_nav_destination != None:
                possible_pos_x, possible_pos_y = robot.bug_nav_destination
                if str(pos_x, pos_y) == str(possible_pos_x, possible_pos_y):
                    robot.bug_nav_destination = None
                    robot.mov_path_index = robot.bug_nav_index
                    # robot.log("^^^^ Reached ^^^^" + str(robot.bug_nav_index))
                    robot.bug_nav_index = -1
                    robot.bug_nav_counter = 0
                else:
                    for iter_i in range(robot.bug_nav_index, len(robot.mov_path_between_location_and_destination)):
                        possible_pos_x, possible_pos_y = robot.mov_path_between_location_and_destination[iter_i]
                        if not utility.is_cell_occupied(occupied_map, possible_pos_x, possible_pos_y):
                            robot.bug_nav_destination = robot.mov_path_between_location_and_destination[iter_i]
                            robot.bug_nav_index = iter_i
                            fin_dir = 0
                            fin_dir = pathfinding.bug_walk_toward(robot, robot.mov_path_between_location_and_destination[iter_i])
                            if fin_dir != 0:
                                # robot.log("Ninth block list " + str(possible_pos_x) + " " + str(possible_pos_y) + " " + str(robot.bug_nav_destination) + " index " + str(robot.bug_nav_index))
                                # TRAVIS MOVE CHECK 6
                                return check.move_check(robot, fin_dir[0], fin_dir[1], 6)
                            else:
                                # robot.log("None2")
                                return None
                    # robot.log("None3")
                    return None
            robot.mov_path_index = robot.mov_path_index + 1
            if len(robot.mov_path_between_location_and_destination[robot.mov_path_index]) == 2:
                new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
            else:
                # robot.log("These are the problem values in move_to_destination " + robot.mov_path_between_location_and_destination + " " + str(robot.mov_path_index) + " " + str(robot.mov_path_between_location_and_destination[robot.mov_path_index]))
                return None

            if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y):
                # robot.log("**** Potential ****")
                # robot.log("Sixth block list " + str(new_pos_x) + " " + str(new_pos_y) + " " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
                possible_pos_x, possible_pos_y = (-1, -1)
                for iter_i in range(robot.mov_path_index, len(robot.mov_path_between_location_and_destination)):
                    possible_pos_x, possible_pos_y = robot.mov_path_between_location_and_destination[iter_i]
                    if not utility.is_cell_occupied(occupied_map, possible_pos_x, possible_pos_y):
                        robot.bug_nav_destination = robot.mov_path_between_location_and_destination[iter_i]
                        robot.bug_nav_index = iter_i
                        robot.bug_nav_counter = 0
                        fin_dir = 0
                        fin_dir = pathfinding.bug_walk_toward(robot, robot.mov_path_between_location_and_destination[iter_i])
                        if fin_dir != 0:
                            # robot.log("Act")
                            # robot.log("Seventh block list " + str(possible_pos_x) + " " + str(possible_pos_y) + " " + str(robot.bug_nav_destination) + " index " + str(robot.bug_nav_index))
                            # TRAVIS MOVE CHECK 7
                            return check.move_check(robot, fin_dir[0], fin_dir[1], 7)
                        else:
                            robot.bug_nav_counter += 1
                            # robot.log("None4")
                            return None
                return None
            # robot.log("Fouth block list " + str(new_pos_x) + " " + str(new_pos_y) + " " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
            # TRAVIS MOVE CHECK 8
            return check.move_check(robot, new_pos_x - pos_x, new_pos_y - pos_y, 8)
    # Conditions not satisfied
    return None

def find_dockspots(robot, depot):
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = constants.directions
    depot_x = depot.x
    depot_y = depot.y

    dockspots = []

    for direction in directions:
        if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, depot_x + direction[0], depot_y + direction[1]):
            # robot.log('111')
            dockspots.append((depot_x + direction[0], depot_y + direction[1]))

    return dockspots

# From examplefuncs player, keep at the bottom
rotate_arr = [
    (0,1),
    (1,1),
    (1,0),
    (1,-1),
    (0,-1),
    (-1, -1),
    (-1, 0),
    (-1, 1)
]

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

def get_list_index(lst, tup):
    # only works for 2-tuples
    for i in range(len(lst)):
        if lst[i][0] == tup[0] and lst[i][1] == tup[1]:
            return i

def rotate(orig_dir, amount):
    direction = rotate_arr[(get_list_index(rotate_arr, orig_dir) + amount) % 8]
    return direction

def reflect(full_map, loc, horizontal=True):
    v_reflec = (len(full_map[0]) - loc[0], loc[1])
    h_reflec = (loc[0], len(full_map) - loc[1])
    if horizontal:
        return h_reflec if full_map[h_reflec[1]][h_reflec[0]] else v_reflec
    else:
        return v_reflec if full_map[v_reflec[1]][v_reflec[0]] else h_reflec

def is_passable(full_map, loc, coord_dir, robot_map=None):
    new_point = (loc[0] + coord_dir[0], loc[1] + coord_dir[1])
    if new_point[0] < 0 or new_point[0] >= len(full_map):
        return False
    if new_point[1] < 0 or new_point[1] >= len(full_map):
        return False
    if not full_map[new_point[1]][new_point[0]]:
        return False
    if robot_map is not None and robot_map[new_point[1]][new_point[0]] > 0:
        return False
    return True

def apply_dir(loc, dir):
    return (loc[0] + dir[0], loc[1] + dir[1])

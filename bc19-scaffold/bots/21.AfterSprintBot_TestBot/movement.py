import communications
import pathfinding
import constants
import utility
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

    # robot.log("Current mov destination is " + str(robot.current_move_destination))
    # robot.log("Current location is " + str((robot.me.x, robot.me.y)))

    if robot.current_move_destination != None:
        final_pos_x = robot.current_move_destination[0]
        final_pos_y = robot.current_move_destination[1]
        if utility.is_cell_occupied(occupied_map, final_pos_x, final_pos_y):
            return None # Can't apply pathfinding if final location is visible and occupied
        elif len(robot.mov_path_between_location_and_destination) == 1:
            robot.current_move_destination = None # Reached destination
            return None

        # Initialise path
        if robot.mov_path_between_location_and_destination == None:
            if robot.burned_out_on_turn != -1:
                robot.mov_path_between_location_and_destination = None
                robot.mov_path_index = 0
                fin_dir = pathfinding.bug_walk(passable_map, occupied_map, final_pos_x, final_pos_y, pos_x, pos_y)
                return robot.move(fin_dir[0], fin_dir[1])
            else:
                robot.mov_path_between_location_and_destination, robot.burned_out = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
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
                if robot.burned_out_on_turn != -1:
                    robot.mov_path_between_location_and_destination = None
                    robot.mov_path_index = 0
                    fin_dir = pathfinding.bug_walk(passable_map, occupied_map, final_pos_x, final_pos_y, pos_x, pos_y)
                    return robot.move(fin_dir[0], fin_dir[1])
                else:
                    robot.mov_path_between_location_and_destination, robot.burned_out = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
                    robot.mov_path_index = 0
                    new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
                    # robot.log("Third block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
                    return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
        # In middle of the list
        else:
            robot.mov_path_index = robot.mov_path_index + 1
            if robot.mov_path_between_location_and_destination == None:
                robot.log("Hit")
                return None
            else:
                if len(robot.mov_path_between_location_and_destination[robot.mov_path_index]) == 2:
                    new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
                else:
                    robot.log("These are the problem values in move_to_destination " + robot.mov_path_between_location_and_destination + " " + str(robot.mov_path_index) + " " + str(robot.mov_path_between_location_and_destination[robot.mov_path_index]))

                # robot.log("Fouth block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
                # TODO -Try to add fuzzy jump or something (This is when some tile occupies the place you want to move to)
                if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y):
                    if robot.burned_out_on_turn != -1:
                        robot.mov_path_between_location_and_destination = None
                        robot.mov_path_index = 0
                        fin_dir = pathfinding.bug_walk(passable_map, occupied_map, final_pos_x, final_pos_y, pos_x, pos_y)
                        return robot.move(fin_dir[0], fin_dir[1])
                    else:
                        robot.mov_path_between_location_and_destination, robot.burned_out = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
                        robot.mov_path_index = 0
                        new_pos_x, new_pos_y = robot.mov_path_between_location_and_destination[robot.mov_path_index]
                        # robot.log("Fifth block , list " + str(robot.mov_path_between_location_and_destination) + " index " + str(robot.mov_path_index))
                return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
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

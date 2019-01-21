import random
import constants
import mapping

def distance(robot, start: tuple, end: tuple) -> int:
    ans = (start[0]-end[0])**2 + (start[1]-end[1])**2
    # robot.log("Distance function: " + str(ans))
    return ans

def get_all_maps(robot):
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()

    return passable_map, occupied_map, karb_map, fuel_map

def is_out_of_bounds(map_dim, pos_x, pos_y):
    return pos_x < 0 or pos_y < 0 or pos_x >= map_dim or pos_y >= map_dim

def is_cell_occupied(occupied_map, pos_x, pos_y):
    bounds_map = len(occupied_map)
    if is_out_of_bounds(bounds_map, pos_x, pos_y):
        return True
    elif occupied_map[pos_y][pos_x] <= 0:
        return False
    else:
        return True

def is_cell_resourceful(karb_map, fuel_map, pos_x, pos_y):
    if is_out_of_bounds(len(karb_map), pos_x, pos_y):
        return False
    elif karb_map[pos_y][pos_x] == 1:
        return True
    elif fuel_map[pos_y][pos_x] == 1:
        return True
    else:
        return False

def is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x, pos_y):
    if is_cell_occupied(occupied_map, pos_x, pos_y):
        return False
    elif passable_map[pos_y][pos_x] != 1:
        return False
    elif is_cell_resourceful(karb_map, fuel_map, pos_x, pos_y):
        return False
    else:
        return True

def random_cells_around():
    dirs = constants.directions
    random.shuffle(dirs, random.random)
    return dirs

def get_relative_karbonite_mine_positions(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    karb_map = robot.get_karbonite_map()

    map_length = len(karb_map)
    queue = []
    distance = []

    for iter_i in range(map_length):
        for iter_j in range(map_length):
            if karb_map[iter_i][iter_j]:
                distance.append((iter_j - pos_x)**2 + (iter_i - pos_y)**2)
                queue.append((iter_j, iter_i))

    sorted_distance, sorted_tuple = insertionSort(distance, queue)
    return sorted_distance, sorted_tuple

def get_relative_fuel_mine_positions(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    fuel_map = robot.get_fuel_map()

    map_length = len(fuel_map)
    queue = []
    distance = []

    for iter_i in range(map_length):
        for iter_j in range(map_length):
            if fuel_map[iter_i][iter_j]:
                distance.append((iter_j - pos_x)**2 + (iter_i - pos_y)**2)
                queue.append((iter_j, iter_i))

    sorted_distance, sorted_tuple = insertionSort(distance, queue)
    return sorted_distance, sorted_tuple

def get_relative_mine_positions(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    fuel_map = robot.get_fuel_map()
    karb_map = robot.get_karbonite_map()

    map_length = len(fuel_map)
    queue = []
    distance = []

    for iter_i in range(map_length):
        for iter_j in range(map_length):
            if fuel_map[iter_i][iter_j] or karb_map[iter_i][iter_j]:
                distance.append((iter_j - pos_x)**2 + (iter_i - pos_y)**2)
                queue.append((iter_j, iter_i))

    sorted_distance, sorted_tuple = insertionSort(distance, queue)
    return sorted_distance, sorted_tuple

def get_sorted_list_from_a_point(pos_x, pos_y, list_to_check):
    queue = []
    distance = []

    for i in range(len(list_to_check)):
        iter_x = list_to_check[i][0]
        iter_y = list_to_check[i][1]
        distance.append((iter_x - pos_x)**2 + (iter_y - pos_y)**2)
        queue.append((iter_x, iter_y))

    sorted_distance, sorted_tuple = insertionSort(distance, queue)
    return sorted_distance, sorted_tuple

def insertionSort(alist, main_list):
    # Quick hack to guard against the conversion of elements into string while sorting
    for index in range(1, len(alist)):
        currentvalue = alist[index]
        currentvalue_ml = main_list[index]
        position = index
        while position > 0 and alist[position - 1] > currentvalue:
            alist[position] = alist[position-1]
            main_list[position] = main_list[position-1]
            position = position -1
        alist[position] = currentvalue
        main_list[position] = currentvalue_ml
    return alist, main_list

def convert_to_decimal(binary_str: str) -> int:
    binary_str = "0b" + binary_str
    return int(binary_str, 2)

def convert_to_binary(dec: int) -> str:
    ary = ["0" for i in range(16)]
    itr = 15 # start from last index
    while dec != 0:
        rem = dec%2
        ary[itr] = str(rem)
        itr -= 1
        dec = dec // 2
    return "".join(ary)

def fuel_less_check(robot):
    if robot.me.turn > 200 and robot.fuel < 2000:
        return True
    elif robot.me.unit != constants.unit_pilgrim and robot.fuel < 200:
        return True
    else:
        return False

def distance_ratio(robot, destination: tuple,
        expected_ratio: float, delta: float) -> bool:
    pos_x, pos_y = robot.me.x, robot.me.y
    # robot.log("Current position: " + str((pos_x, pos_y)))
    start_to_cur = distance(robot, (pos_x, pos_y), robot.our_castle_or_church_base)
    destination_to_cur = distance(robot, (pos_x, pos_y), destination)
    ratio = start_to_cur/(destination_to_cur + start_to_cur)
    if robot.me.id == 1037:
        robot.log("Ratio is: " + str(ratio) + ", diff: " + str(abs(ratio-expected_ratio)))
        robot.log("Ratios are: %d, %d"%(start_to_cur, destination_to_cur))
    ans = True if abs(ratio-expected_ratio) <= delta else False
    # robot.log("Outcome: " + str(ans))
    return ans

def default_movement_variables(robot):
    robot.mov_path_between_location_and_destination = None
    robot.bug_nav_destination = None
    robot.bug_nav_index = -1
    robot.bug_nav_counter = 0
    robot.vertical_ratio_satisfied = False
    robot.even_rule_satisfied = False
    robot.lattice_dest = False

def is_in_list(element, given_list):
    for iter_i in len(given_list):
        if str(element) == str(given_list[iter_i]):
            return True
    return False

import random
import constants

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

def get_closest_coordinate(main_position, list_position):
    least_curr = []
    least_dist = 100000
    for index in range(len(list_position)):
        main_x = main_position[0]
        main_y = main_position[1]
        pt_x = list_position[index][0]
        pt_y = list_position[index][1]

        dist = (((main_x - pt_x) ** 2 ) + ((main_y - pt_y) ** 2 )) ** 0.5
        if dist < least_dist:
            least_curr = list_position[index]
            least_dist = dist
        
    return least_curr

def get_closest_distance(main_position, list_position):
    least_dist = 100000
    for index in range(len(list_position)):
        main_x = main_position[0]
        main_y = main_position[1]
        pt_x = list_position[index][0]
        pt_y = list_position[index][1]

        dist = (((main_x - pt_x) ** 2 ) + ((main_y - pt_y) ** 2 )) ** 0.5
        if dist < least_dist:
            least_dist = dist
    return least_dist

def dict_list_duplicate_count(source_list):
    result_dict = {}
    for index in range(len(source_list)):
        result_dict[source_list[index]] += 1
    return result_dict

def get_least(distance_array):
    minimum = 10000
    for index in range(len(distance_array)):
        if distance_array[index] < minimum:
            minimum = distance_array[index]
    return minimum

def castle_danger_level(robot):
    robot.castle_talk(robot.nearest_enemy_castle_distance)
    distance_array = []
    signal_response = robot.get_visible_robots()
    robot.log(signal_response) 
    count_signal_response = len(signal_response)
    if count_signal_response == 1:
        distance_array.append(robot.nearest_enemy_castle_distance)
    else:
        for index in range(count_signal_response):
            # talking_unit_index = signal_response[index]["id"]
            talking_unit_team = signal_response[index]["team"]
            if (talking_unit_team == robot.me.team and signal_response[index]["castle_talk"] > 0):
                distance = signal_response[index]["castle_talk"]
                distance_array.append(distance)
    distance_dict = dict_list_duplicate_count(distance_array)
    smallest_dist = get_least(distance_array)
    # robot.log(distance_array)
    # robot.log(smallest_dist)
    # robot.log(robot.nearest_enemy_castle_distance)
    if robot.nearest_enemy_castle_distance > smallest_dist:
        robot.early_danger_level = 0
    elif robot.nearest_enemy_castle_distance == smallest_dist:
        if distance_dict[robot.nearest_enemy_castle_distance] > 1:
            robot.early_danger_level = 2
        else:
            robot.early_danger_level = 1
    elif robot.nearest_enemy_castle_distance < smallest_dist:
        robot.log("This shouldn't happen")

            
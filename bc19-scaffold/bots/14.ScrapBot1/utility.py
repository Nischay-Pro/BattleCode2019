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

def _store_destination(dest_x: int, dest_y: int, bin_list: list) -> None:
    '''
    dest_x: abscissa of mine's location (decimal)
    dest_y: ordinate of mine's location (decimal)
    bin_list: self loop message of pilgrim as a list of string (binary
    representation)

    First 4 bits of bin_list are reserved for storing information about next
    move.
    '''
    x_bin = convert_to_binary(dest_x)
    y_bin = convert_to_binary(dest_y)
    start = 4
    # copy binary of x to self loop message
    for i in range(10, 16):
        bin_list[start] = x_bin[i]
        start += 1
    # copy binary of y to self loop message
    for i in range(10, 16):
        bin_list[start] = y_bin[i]
        start += 1

def _store_next_step(astar_path: list, bin_list: list, directions: list) -> None:
    '''
    The first 4 bits are used to store the next step
    directions (list): 12 movements of pilgrim (check pilgrim_directions in
    constant module)
    '''
    if len(astar_path) == 1:
        bin_list[3] = '1'
        for i in range(3):
            bin_list[i] = '0'
        return None

    step = astar_path[0]
    second_step = astar_path[1]
    dx = second_step[0] - step[0]
    dy = second_step[1] - step[1]
    ans = None
    for i in range(len(directions)):
        direction = directions[i]
        if (dx, dy) == direction:
            ans = i
            break
    step_byte = convert_to_binary(ans)
    iter_ = 0
    for i in range(12, 16):
        bin_list[iter_] = step_byte[i]
        iter_ += 1

def encode_self_loop_msg_with_direction(dest_x: int, dest_y: int,
        astar_path: list, directions: list) -> int:
    bin_list = ['0' for i in range(16)]
    _store_destination(dest_x, dest_y, bin_list)
    _store_next_step(astar_path, bin_list, directions)
    return convert_to_decimal("".join(bin_list))

def encode_self_loop_msg_without_direction(dest_x: int, dest_y: int) -> int:
    bin_list = ['0' for i in range(16)]
    _store_destination(dest_x, dest_y, bin_list)
    return convert_to_decimal("".join(bin_list))

def decode_self_loop_msg_with_direction(message: int, directions: list) -> tuple:
    binary_str = convert_to_binary(message)
    direction = convert_to_decimal(binary_str[0:4])
    x_destination = convert_to_decimal(binary_str[4:10])
    y_destination = convert_to_decimal(binary_str[10:16])
    return (direction, x_destination, y_destination)

def decode_self_loop_msg_without_direction(message: int) -> tuple:
    binary_str = convert_to_binary(message)
    x_destination = convert_to_decimal(binary_str[4:10])
    y_destination = convert_to_decimal(binary_str[10:16])
    return (x_destination, y_destination)

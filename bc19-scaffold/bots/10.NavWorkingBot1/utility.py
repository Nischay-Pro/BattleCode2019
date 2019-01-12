import random

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

def cells_around():
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
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

    store1, store2 = insertionSort(distance, queue)
    return store2

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

    store1, store2 = insertionSort(distance, queue)
    return store2

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

    store1, store2 = insertionSort(distance, queue)
    return store2

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

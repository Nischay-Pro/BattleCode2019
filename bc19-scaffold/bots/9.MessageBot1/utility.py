from random import shuffle, random

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
    shuffle(dirs, random)
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
                
    return [x for _,x in sorted(zip(distance, queue))]

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
                
    return [x for _,x in sorted(zip(distance, queue))]

def get_statistics(robot, friendly):
    None

def get_economic_unit(robot, friendly):
    for friend in friendly:
        unit_type = friend['unit']
        robot.log(unit_type)
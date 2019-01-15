import constants

def get_nearby_map(x, y, given_map, grid_radius = 2):
    sub_side = grid_radius * 2 + 1
    sub_map = []

    for i in range(sub_side):
        for j in range(sub_side):
            try:
                sub_map.append(given_map[y-grid_radius+i][x-grid_radius+j] == True)
            except:
                sub_map.append(False)

    return sub_map

def get_map_ratio(x, y, given_map, grid_radius = 2):
    nearby = get_nearby_map(x, y, given_map, grid_radius)
    full = 0

    for cell in nearby:
        if cell == True:
            full += 1

    return full/((grid_radius * 2 + 1)**2)

def analyze_map(given_map, grid_radius = 2):
    sub_side = grid_radius * 2 + 1
    results = []

    y = grid_radius + 1
    while y < len(given_map):
        x = grid_radius + 1
        while x < len(given_map):
            results.append((x, y, get_map_ratio(x, y, given_map, grid_radius)))
            x += sub_side
        y += sub_side

    return results

def find_symmetrical_point(robot, pos_x, pos_y, is_hoz_symmetry):    
    map_length = len(robot.get_passable_map())
    if is_hoz_symmetry == 0:
        return (pos_x, map_length - 1 - pos_y)
    else:
        return (map_length - 1 - pos_x, pos_y)

def return_map_symmetry(robot):
    passable_map = robot.get_passable_map()
    if check_hoz_symmetry(passable_map):
        # robot.log("Is horizontal")
        robot.map_symmetry = 0
    else:
        # robot.log("Is vertical")
        robot.map_symmetry = 1
    
def check_hoz_symmetry(given_map):
    start = 0
    end = len(given_map) - 1

    while start < end:
        for i in range(len(given_map[start])):
            if given_map[start][i] != given_map[end][i]:
                return False
        start += 1
        end -= 1

    return True

def find_chokepoints(robot, grid_radius = 2):
    given_map = robot.get_passable_map()
    sub_side = grid_radius * 2 + 1
    results = []

    y = grid_radius + 1
    while y < len(given_map):
        x = grid_radius + 1
        while x < len(given_map):
            ratio = get_map_ratio(x, y, given_map, grid_radius)
            if ratio < constants.chokepoint_modifier:
                results.append((x, y, ratio))
            x += sub_side
        y += sub_side

    return results

def find_karbonite_rich(robot, grid_radius = 2):
    given_map = robot.karbonite_map
    sub_side = grid_radius * 2 + 1
    results = []

    y = grid_radius + 1
    while y < len(given_map):
        x = grid_radius + 1
        while x < len(given_map):
            ratio = get_map_ratio(x, y, given_map, grid_radius)
            if ratio > constants.karbonite_modifier:
                results.append((x, y, ratio))
            x += sub_side
        y += sub_side

    return results

def find_fuel_rich(robot, grid_radius = 2):
    given_map = robot.fuel_map
    sub_side = grid_radius * 2 + 1
    results = []

    y = grid_radius + 1
    while y < len(given_map):
        x = grid_radius + 1
        while x < len(given_map):
            ratio = get_map_ratio(x, y, given_map, grid_radius)
            if ratio > constants.fuel_modifier:
                results.append((x, y, ratio))
            x += sub_side
        y += sub_side

    return results

def find_resource_rich(robot, grid_radius = 2):
    fuel_map = robot.fuel_map
    karbonite_map = robot.karbonite_map
    sub_side = grid_radius * 2 + 1
    results = []

    y = grid_radius + 1
    while y < len(fuel_map):
        x = grid_radius + 1
        while x < len(fuel_map):
            ratio = get_map_ratio(x, y, fuel_map, grid_radius) + get_map_ratio(x, y, karbonite_map, grid_radius)
            if ratio > constants.fuel_modifier:
                results.append((x, y, ratio))
            x += sub_side
        y += sub_side

    return results
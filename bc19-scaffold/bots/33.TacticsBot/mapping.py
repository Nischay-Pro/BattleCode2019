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

def get_area_occupiability(pos_x, pos_y, robot, grid_radius = 2):
    sub_side = grid_radius * 2 + 1
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    map_dim = len(occupied_map)

    empty = 0

    for i in range(sub_side):
        for j in range(sub_side):
            if pos_x - grid_radius + j >= 0 and pos_y - grid_radius + i >= 0 and pos_x - grid_radius + j < map_dim and pos_y - grid_radius + i < map_dim:
                if passable_map[pos_y - grid_radius + i][pos_x - grid_radius + j] == 1:
                    if occupied_map[pos_y - grid_radius + i][pos_x - grid_radius + j] == 0:
                        empty += 1

    return empty/((grid_radius * 2 + 1)**2)

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

def get_friendly_karbonite(castle):
    karbonite_map = castle.get_karbonite_map()
    hoz_symmetry = check_hoz_symmetry(karbonite_map)

    side = len(karbonite_map)
    mid = side // 2
    init = 0
    fin = mid + 1
    final = []

    if hoz_symmetry:
        if castle.me.y > mid:
            init = mid
            fin = side
        for i in range(init, fin):
            for j in range(side):
                if karbonite_map[i][j] == 1:
                    final.append((j, i))
    else:
        if castle.me.x > mid:
            init = mid
            fin = side
        for i in range(side):
            for j in range(init, fin):
                if karbonite_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_friendly_fuel(castle):
    fuel_map = castle.get_fuel_map()
    hoz_symmetry = check_hoz_symmetry(fuel_map)

    side = len(fuel_map)
    mid = side // 2
    init = 0
    fin = mid + 1
    final = []

    if hoz_symmetry:
        if castle.me.y > mid:
            init = mid
            fin = side
        for i in range(init, fin):
            for j in range(side):
                if fuel_map[i][j] == 1:
                    final.append((j, i))
    else:
        if castle.me.x > mid:
            init = mid
            fin = side
        for i in range(side):
            for j in range(init, fin):
                if fuel_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_friendly_resources(castle):
    fuel_map = castle.get_fuel_map()
    karbonite_map = castle.get_karbonite_map()
    hoz_symmetry = check_hoz_symmetry(karbonite_map)

    side = len(karbonite_map)
    mid = side // 2
    init = 0
    fin = mid + 1
    final = []

    if hoz_symmetry:
        if castle.me.y > mid:
            init = mid
            fin = side
        for i in range(init, fin):
            for j in range(side):
                if karbonite_map[i][j] == 1 or fuel_map[i][j] == 1:
                    final.append((j, i))
    else:
        if castle.me.x > mid:
            init = mid
            fin = side
        for i in range(side):
            for j in range(init, fin):
                if karbonite_map[i][j] == 1 or fuel_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_enemy_karbonite(castle):
    karbonite_map = castle.get_karbonite_map()
    hoz_symmetry = check_hoz_symmetry(karbonite_map)

    side = len(karbonite_map)
    mid = side // 2
    init = 0
    fin = mid
    final = []

    if hoz_symmetry:
        if castle.me.y < mid:
            init = mid + 1
            fin = side
        for i in range(init, fin):
            for j in range(side):
                if karbonite_map[i][j] == 1:
                    final.append((j, i))
    else:
        if castle.me.x < mid:
            init = mid + 1
            fin = side
        for i in range(side):
            for j in range(init, fin):
                if karbonite_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_enemy_fuel(castle):
    fuel_map = castle.get_fuel_map()
    hoz_symmetry = check_hoz_symmetry(fuel_map)

    side = len(fuel_map)
    mid = side // 2
    init = 0
    fin = mid
    final = []

    if hoz_symmetry:
        if castle.me.y < mid:
            init = mid + 1
            fin = side
        for i in range(init, fin):
            for j in range(side):
                if fuel_map[i][j] == 1:
                    final.append((j, i))
    else:
        if castle.me.x < mid:
            init = mid + 1
            fin = side
        for i in range(side):
            for j in range(init, fin):
                if fuel_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_enemy_resources(castle):
    fuel_map = castle.get_fuel_map()
    karbonite_map = castle.get_karbonite_map()
    hoz_symmetry = check_hoz_symmetry(karbonite_map)

    side = len(karbonite_map)
    mid = side // 2
    init = 0
    fin = mid
    final = []

    if hoz_symmetry:
        if castle.me.y < mid:
            init = mid + 1
            fin = side
        for i in range(init, fin):
            for j in range(side):
                if karbonite_map[i][j] == 1 or fuel_map[i][j] == 1:
                    final.append((j, i))
    else:
        if castle.me.x < mid:
            init = mid + 1
            fin = side
        for i in range(side):
            for j in range(init, fin):
                if karbonite_map[i][j] == 1 or fuel_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_contested_resources(castle, delta = constants.contested_delta):
    fuel_map = castle.get_fuel_map()
    karbonite_map = castle.get_karbonite_map()
    hoz_symmetry = check_hoz_symmetry(karbonite_map)

    side = len(karbonite_map)
    mid = side // 2
    init = mid - int(side * delta)
    fin = mid + int(side * delta)
    final = []

    if hoz_symmetry:
        for i in range(init, fin):
            for j in range(side):
                if karbonite_map[i][j] == 1 or fuel_map[i][j] == 1:
                    final.append((j, i))
    else:
        for i in range(side):
            for j in range(init, fin):
                if karbonite_map[i][j] == 1 or fuel_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_contested_karbonite(castle, delta = constants.contested_delta):
    karbonite_map = castle.get_karbonite_map()
    hoz_symmetry = check_hoz_symmetry(karbonite_map)

    side = len(karbonite_map)
    mid = side // 2
    init = mid - int(side * delta)
    fin = mid + int(side * delta)
    final = []

    if hoz_symmetry:
        for i in range(init, fin):
            for j in range(side):
                if karbonite_map[i][j] == 1:
                    final.append((j, i))
    else:
        for i in range(side):
            for j in range(init, fin):
                if karbonite_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_contested_fuel(castle, delta = constants.contested_delta):
    fuel_map = castle.get_fuel_map()
    hoz_symmetry = check_hoz_symmetry(fuel_map)

    side = len(fuel_map)
    mid = side // 2
    init = mid - int(side * delta)
    fin = mid + int(side * delta)
    final = []

    if hoz_symmetry:
        for i in range(init, fin):
            for j in range(side):
                if fuel_map[i][j] == 1:
                    final.append((j, i))
    else:
        for i in range(side):
            for j in range(init, fin):
                if fuel_map[i][j] == 1:
                    final.append((j, i))

    return final

def get_friendly_influence(robot):
    visible_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()
    pos_x = robot.me.x
    pos_y = robot.me.y
    side = len(visible_map)

    visible_area = 0
    visible_friendlies = 0

    for i in range(side):
        for j in range(side):
            if visible_map[i][j] > -1:
                if passable_map[i][j] == 1:
                    visible_area += 1
                    if visible_map[i][j] > 0:
                        if robot.get_robot(visible_map[i][j]).team == robot.me.team:
                            visible_friendlies += 1

    return visible_friendlies / visible_area

def get_enemy_influence(robot):
    visible_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()
    pos_x = robot.me.x
    pos_y = robot.me.y
    side = len(visible_map)

    visible_area = 0
    visible_enemies = 0

    for i in range(side):
        for j in range(side):
            if visible_map[i][j] > -1:
                if passable_map[i][j] == 1:
                    visible_area += 1
                    if visible_map[i][j] > 0:
                        if robot.get_robot(visible_map[i][j]).team != robot.me.team:
                            visible_enemies += 1

    return visible_enemies / visible_area

def get_corner_friendly_influence(robot, grid_radius = 2):
    diagonal_directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    sub_side = grid_radius * 2 + 1
    visible_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()
    p_x = robot.me.x
    p_y = robot.me.y
    map_dim = len(visible_map)

    influences = []

    for d_dir in diagonal_directions:
        pos_x = p_x + d_dir[0]
        pos_y = p_y + d_dir[1]
        visible_area = 0
        visible_friends = 0
        for i in range(sub_side):
            for j in range(sub_side):
                if pos_x - grid_radius + j >= 0 and pos_y - grid_radius + i >= 0 and pos_x - grid_radius + j < map_dim and pos_y - grid_radius + i < map_dim:
                    if passable_map[pos_y - grid_radius + i][pos_x - grid_radius + j] == 1:
                        visible_area += 1
                        if visible_map[pos_y - grid_radius + i][pos_x - grid_radius + j] > 0:
                            if robot.get_robot(visible_map[pos_y - grid_radius + i][pos_x - grid_radius + j]).team == robot.me.team:
                                visible_friends += 1
        influences.append((d_dir[0], d_dir[1], visible_friends / visible_area))

    return influences
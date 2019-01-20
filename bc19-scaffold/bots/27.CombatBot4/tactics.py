# General tactics for all units
import utility
import movement
import pathfinding
import constants
import check

def prophet_will_combat_1vs1(robot, enemy):
    passable_map = robot.get_passable_map()
    if enemy['unit'] == constants.unit_prophet:
        if robot.me.health == constants.prophet_max_health:
            robot.is_targeting_robot_with_id = enemy['id']
            return enemy
        elif robot.me.health < constants.prophet_max_health:
            if enemy['id'] == robot.is_targeting_robot_with_id:
                robot.is_targeting_robot_with_id = enemy['id']
                return enemy
            else:
                new_pos_x = 0
                new_pos_y = 0

                # Can move out of bot vision
                max_distance = constants.prophet_max_attack_range
                for directions in constants.non_crusader_move_directions:
                    guessing_new_pos_x = robot.me.x + directions[0]
                    guessing_new_pos_y = robot.me.y + directions[1]
                    guessing_distance = (guessing_new_pos_x - enemy['x'])**2 + (guessing_new_pos_y- enemy['y'])**2
                    if guessing_distance > max_distance and not utility.is_cell_occupied(passable_map, guessing_new_pos_x, guessing_new_pos_y):
                        guessing_distance = max_distance
                        new_pos_x = guessing_new_pos_x
                        new_pos_y = guessing_new_pos_y
                if max_distance > constants.prophet_max_attack_range:
                    # TRAVIS MOVE CHECK 15
                    return check.move_check(robot, new_pos_x - robot.me.x, new_pos_y - robot.me.y, 15)

                # Can move into non-attack region
                min_distance = constants.prophet_min_attack_range
                for directions in constants.non_crusader_move_directions:
                    guessing_new_pos_x = robot.me.x + directions[0]
                    guessing_new_pos_y = robot.me.y + directions[1]
                    guessing_distance = (guessing_new_pos_x - enemy['x'])**2 + (guessing_new_pos_y- enemy['y'])**2

                    if guessing_distance < min_distance and not utility.is_cell_occupied(passable_map, guessing_new_pos_x, guessing_new_pos_y):
                        guessing_distance = min_distance
                        new_pos_x = guessing_new_pos_x
                        new_pos_y = guessing_new_pos_y
                if min_distance < constants.prophet_min_attack_range:
                    # TRAVIS MOVE CHECK 16
                    return robot.move()

            # robot.is_targeting_robot_with_id = enemy['id']

def simple_attack(robot):
    None

def simulate_conbat_result(robot):
    None

def increase_influence_at_submap(robot, pos_x, pos_y):
    None

# Specific tactics for units
def kiting_by_prophet(robot):
    None

def should_combat_unit_be_at_battle_front(robot) -> bool:
    '''
    To check if a combat unit should be sent to battle front.
    The combat unit should be sent to battle front if and only if it is given
    birth by castle and it has a destination.
    '''
    robot.log("Destination " + str(robot.current_move_destination))
    # robot.log(str(robot.mov_path_between_location_and_destination))
    # robot.log("Build by castle: " + str(robot.built_by_a_castle))
    # robot.log("Home loc: " + str(robot.our_castle_or_church_base))
    if not robot.current_move_destination: return False
    # elif not robot.mov_path_between_location_and_destination: return False
    elif robot.built_by_a_church: return False
    else: return True

def _move(robot):
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    des_x, des_y = robot.current_move_destination
    pos_x, pos_y = robot.me.x, robot.me.y
    find_dir = 0
    find_dir = pathfinding.bug_walk_toward(passable_map, occupied_map, des_x,
            des_y, pos_x, pos_y)
    if robot.me.id == 1037:
        robot.log("Dir is: " + str(find_dir))
    if find_dir != 0:
        # TRAVIS MOVE CHECK 17
        new_dest = (pos_x + find_dir[0], pos_y + find_dir[1])
        if str(robot.bug_nav_prev_coord) == str(new_dest):
            ans = None
        else:
            robot.bug_nav_prev_coord = (pos_x, pos_y)
            ans = check.move_check(robot, find_dir[0], find_dir[1], 17)
    else:
        robot.bug_nav_counter += 1
        ans =  None
    # ans = movement.move_to_destination(robot)
    # robot.log("Return value: " + str(ans))
    return ans

def _stop_movement(robot):
    next_move = _move(robot)
    if next_move:
        return next_move
    else:
        # TODO: find the possible empty lattice points in the adjacent boxes
        robot.current_move_destination = None
        utility.default_movement_variables(robot)
        return None

# Need to optimize
def find_lattice_point(robot):
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    pos_x, pos_y = robot.me.x, robot.me.y
    n = len(occupied_map)
    dist = 10**5
    coord = None
    for i in range(n):
        for j in range(n):
            if not utility.is_out_of_bounds(n, j, i) and occupied_map[i][j] == 0 and (i+j)%2 == 0 and passable_map[i][j] == 1:
                cur_distance = utility.distance(robot, (pos_x, pos_y), (j, i))
                if cur_distance < dist:
                    dist = cur_distance
                    coord = (j, i)
    if robot.me.id == 1037:
        robot.log("Lattice coordinate: " + str(coordinate))
    return coord

def send_combat_unit_to_battle_front(robot, ratio: float, delta: float):
    dest = robot.current_move_destination
    pos_x, pos_y = robot.me.x, robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    if robot.me.id == 1037:
        robot.log("Current pos: " + str((pos_x, pos_y)))

    if robot.lattice_dest and (pos_x + pos_y)%2 == 0:
    # if robot.lattice_dest and str((pos_x, pos_y)) == str(robot.current_move_destination):
        robot.current_move_destination = None
        utility.default_movement_variables(robot)
        return None

    # Safety check
    #  if ratio + delta >= 1:
        #  ratio = ratio - delta
    if robot.fuel <= 30:
        return None
    if not robot.vertical_ratio_satisfied:
        is_combat_unit_at_front = utility.distance_ratio(robot, dest, ratio, delta)
        if robot.me.id == 1037:
            robot.log("Is unit at front: " + str(is_combat_unit_at_front))
        if is_combat_unit_at_front:
            robot.vertical_ratio_satisfied = True
            if (pos_x + pos_y)%2 == 0:
                robot.current_move_destination = None
                utility.default_movement_variables(robot)
            return None # we have reached to battle front, don't move
        else:
            return _stop_movement(robot)
    elif robot.vertical_ratio_satisfied and not robot.even_rule_satisfied:
        if not robot.lattice_dest: # First time
            coordinate = find_lattice_point(robot)
            if coordinate:
                # robot.log("Current pos 1: " + str((pos_x, pos_y)))
                x, y = coordinate
                robot.current_move_destination = (x, y)
                robot.lattice_dest = True
                return _stop_movement(robot)
        else:
            next_move = None
            if occupied_map[dest[1]][dest[0]] > 0:
                coordinate = find_lattice_point(robot)
                if coordinate:
                    x, y = coordinate
                    robot.current_move_destination = (x, y)
                    # robot.log("Current pos 2: " + str((pos_x, pos_y)))
                    return _stop_movement(robot)
                return None
            return _stop_movement(robot)

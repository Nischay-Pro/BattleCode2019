# General tactics for all units
import check
import combat_utility
import constants
import movement
import pathfinding
import utility


def simple_attack(robot, enemy_list):
    None

def choose_target(robot, enemy_list, enemy_distance_list):
    best_target = None
    enemy_score = -99
    for iter_i in range(len(enemy_list)):
        if combat_utility.is_attackable_enemy_unit(robot, enemy_list[iter_i], enemy_distance_list[iter_i]) == 1:
            # Replace with get priority
            unit_score = constants.enemy_unit_priority_for_prophet[enemy_list[iter_i]['unit']]
            if unit_score > enemy_score:
                enemy_score = unit_score
                best_target = enemy_list[iter_i]
    return best_target

def simulate_combat_result(robot):
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
    pos_x, pos_y = robot.me.x, robot.me.y
    find_dir = 0
    find_dir = pathfinding.bug_walk_toward(robot, robot.current_move_destination)
    if robot.me.id == 1037:
        robot.log("Dir is: " + str(find_dir))
    if find_dir != 0:
        # TRAVIS MOVE CHECK 17
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
        pos_x, pos_y = robot.me.x, robot.me.y
        if (pos_x + pos_y) % 2 == 0:
            return None

        else:
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if (not utility.is_cell_occupied(robot.get_visible_robot_map(), pos_x, pos_y)) and robot.passable_map[pos_y + direction[1]][pos_x + direction[0]]:
                    return check.move_check(robot, direction[0], direction[1], 18)

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
    if ratio + delta >= 1:
        ratio = ratio - delta
    if robot.fuel <= 30:
        return None
    if not robot.vertical_ratio_satisfied:
        is_combat_unit_at_front = utility.distance_ratio(robot, dest, ratio, delta)

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

import check
import constants
import mapping
import pathfinding
import utility
import vision
import communications

def command_flow(robot):
    None
    # If no hostile units, arrange lattice formation
    # If core is ready, push
    # If we are fighting for useless land retreat if possible, else attack
    # If outnumbered, try to retreat

def fill_combat_map(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    combat_map_length = len(robot.combat_map)

    min_x = pos_x - (combat_map_length - 1)/2
    max_x = pos_x + (combat_map_length - 1)/2
    min_y = pos_y - (combat_map_length - 1)/2
    max_y = pos_y + (combat_map_length - 1)/2

    visible_units = robot.get_visible_robots()
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)

    for iter_i in range(len(combat_map_length)):
        for iter_j in range(len(combat_map_length)):
            # Impassable or out of bounds
            if utility.is_out_of_bounds(combat_map_length, iter_j + min_x, iter_i + min_y) or passable_map[iter_i][iter_j]!= 1:
                robot.combat_map[iter_i][iter_j] = -1

    for unit in visible_units:
        if robot.is_visible(unit):
            if unit['team']  == robot.me.team:
                # 1 to 4096
                robot.combat_map[unit['y'] - min_y][unit['x'] - min_x] = unit['id']
            else:
                # -2 to -4097
                robot.combat_map[unit['y'] - min_y][unit['x'] - min_x] = -unit['id'] - 1

    # robot.log("1 " + str(is_unit_safe_at_current_position(robot)))
    # robot.log("2 " + str(is_unit_in_enemy_vision_range(robot)))
    # robot.log("3 " + str(is_position_in_enemy_attack_range(robot, 0, 0)))
    # robot.log("4 " + str(is_position_in_enemy_vision_range(robot, 0, 0)))
    # robot.log("5 " + str(give_postions_where_unit_can_evade_enemy_vision(robot)))

    # robot.combat_map

def is_attackable_enemy_unit(robot, enemy, enemy_distance):
    # This data call (give_stats) is for the self_robot i.e the current bot, so you require a ".me" also
    attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(robot.me)
    if enemy_distance >= min_attack_range and enemy_distance <= max_attack_range:
        return 1
    return 0

def is_unit_in_any_enemy_attack_range(robot):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    unit_count = 0
    danger_count = 0
    for iter_i in range(len(visible_enemy_list)):
        unit = visible_enemy_list[iter_i]
        distance = visible_enemy_distance[iter_i]
        attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(unit)
        if distance >= min_attack_range and distance <= max_attack_range:
            danger_count += attack_damage/10 # All damages are multiples of 10
            unit_count += 1
    return danger_count

def is_unit_in_any_enemy_vision_range(robot):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    sighted_count = 0
    for iter_i in range(len(visible_enemy_list)):
        unit = visible_enemy_list[iter_i]
        distance = visible_enemy_distance[iter_i]
        attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(unit)
        if distance <= vision_range:
            sighted_count += 1
    return sighted_count

def is_position_in_any_enemy_attack_range(robot, pos_x, pos_y):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    for iter_i in range(len(visible_enemy_list)):
        unit = visible_enemy_list[iter_i]
        enemy_pos_x = unit['x']
        enemy_pos_y = unit['y']
        distance = utility.distance(robot, (enemy_pos_x, enemy_pos_y), (pos_x, pos_y))
        attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(unit)
        if distance >= min_attack_range and distance <= max_attack_range:
            return 1
    return 0

def is_position_in_any_enemy_vision_range(robot, pos_x, pos_y):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    for iter_i in range(len(visible_enemy_list)):
        unit = visible_enemy_list[iter_i]
        enemy_pos_x = unit['x']
        enemy_pos_y = unit['y']
        distance = utility.distance(robot, (enemy_pos_x, enemy_pos_y), (pos_x, pos_y))
        attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(unit)
        if distance <= vision_range:
            return 1
    return 0

def is_position_in_any_enemy_handicap_range(robot, pos_x, pos_y):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    for iter_i in range(len(visible_enemy_list)):
        unit = visible_enemy_list[iter_i]
        enemy_pos_x = unit['x']
        enemy_pos_y = unit['y']
        distance = utility.distance(robot, (enemy_pos_x, enemy_pos_y), (pos_x, pos_y))
        attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(unit)
        if has_handicapped_area == 1 and distance < min_attack_range:
            return 1
    return 0

def give_postions_where_unit_can_evade_all_enemy_vision(robot):
    directions = None
    vision_evasion_position_list = []
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    if robot.me.unit != constants.unit_crusader:
        directions = constants.non_crusader_move_directions
    else:
        directions = constants.crusader_move_directions
    for direction in directions:
        new_pos_x = pos_x + direction[0]
        new_pos_y = pos_y + direction[1]
        if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y) or passable_map[new_pos_y][new_pos_x] != 1:
            continue
        if is_position_in_any_enemy_vision_range(robot, new_pos_x, new_pos_y) == 0:
            vision_evasion_position_list.append((new_pos_x, new_pos_y))
    return vision_evasion_position_list

def give_postions_where_unit_can_evade_all_enemy_attack(robot):
    directions = None
    attack_evasion_position_list = []
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    if robot.me.unit != constants.unit_crusader:
        directions = constants.non_crusader_move_directions
    else:
        directions = constants.crusader_move_directions
    for direction in directions:
        new_pos_x = pos_x + direction[0]
        new_pos_y = pos_y + direction[1]
        if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y) or passable_map[new_pos_y][new_pos_x] != 1:
            continue
        if is_position_in_any_enemy_attack_range(robot, new_pos_x, new_pos_y) == 0:
            attack_evasion_position_list.append((new_pos_x, new_pos_y))
    return attack_evasion_position_list

def give_postions_where_unit_is_in_handicap_area_of_any_enemy(robot):
    directions = None
    handicap_position_list = []
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    if robot.me.unit != constants.unit_crusader:
        directions = constants.non_crusader_move_directions
    else:
        directions = constants.crusader_move_directions
    for direction in directions:
        new_pos_x = pos_x + direction[0]
        new_pos_y = pos_y + direction[1]
        if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y) or passable_map[new_pos_y][new_pos_x] != 1:
            continue
        if is_position_in_any_enemy_handicap_range(robot, new_pos_x, new_pos_y) == 0:
            handicap_position_list.append((new_pos_x, new_pos_y))
    return handicap_position_list

def can_unit_kite(robot, vision_evasion_position_list):
    if len(vision_evasion_position_list) != 0:
        return 1
    return 0

def executing_kiting(robot, vision_evasion_position_list, attack_evasion_position_list, handicap_position_list):
    None

def can_avoid_damage(robot, attack_evasion_position_list):
    if len(attack_evasion_position_list) != 0:
        return 1
    return 0

def is_attacked_by_hidden_unit(robot, visible_enemy_units):
    if robot.step != 0 and robot.delta_health_reduced!=0 and len(visible_enemy_units)== 0:
        return 1
    return 0

def compare_combat_map(robot):
    None

def retreat_decider(robot):
    #On the ratio of your troops, enemy troops and signal
    None

def attack_location(robot, pos_x, pos_y, flag, fuel, enemy = None):
    robot.is_targeting_robot_with_id = enemy['id']
    if robot.fuel > fuel:
        return check.attack_check(robot, pos_x - robot.me.x, pos_y - robot.me.y, flag)
    return None

def give_crusader_charge_location(robot, visible_enemy_list, visible_enemy_distance):
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    min_distance = 99
    closest_pos = None
    for iter_i in range(len(visible_enemy_list)):
        enemy_unit = visible_enemy_list[iter_i]
        enemy_pos_x = enemy_unit['x']
        enemy_pos_y = enemy_unit['y']
        if visible_enemy_distance[iter_i] > constants.crusader_max_attack_range:
            for direction in constants.crusader_move_directions:
                new_pos_x = robot.me.x + direction[0]
                new_pos_y = robot.me.y + direction[1]
                if not utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y) and passable_map[new_pos_y][new_pos_x] != 0:
                    distance  = utility.distance(robot, (enemy_pos_x, enemy_pos_y), (new_pos_x, new_pos_y))
                    if distance < min_distance:
                        min_distance = distance
                        closest_pos = (new_pos_x, new_pos_y)
    return closest_pos

def enemy_direction_guess_and_move(robot, visible_friendly_distance, visible_friendly_list):
    pos_x = robot.me.x
    pos_y = robot.me.y
    dirc_x, dirc_y = robot.guessing_in_direction
    if str(dirc_x, dirc_y) == str(0,0) and robot.current_combat_move_destination != None:
        dirc_x, dirc_y = robot.current_move_destination
    fin_dir = pathfinding.bug_walk_toward(robot, (pos_x + dirc_x, pos_y + dirc_y))
    if fin_dir != 0:
        # TRAVIS MOVE CHECK 21
        return check.move_check(robot, fin_dir[0], fin_dir[1], 21)
    else:
        return None
    return None

def radio_friends_enemy_location(robot, enemy_pos_x, enemy_pos_y):
    comms = communications.encode_msg_without_direction(enemy_pos_x, enemy_pos_y)
    if comms != 0 and robot.combat_broadcast_level <= 0:
        check.signal_check(robot, comms, 64)
        robot.combat_broadcast_level = constants.combat_broadcast_cooldown

def radio_friends_charge_order(robot):
    mine_location = None
    mine_location = charge_to_nearest_enemy_mine(robot)
    if mine_location != None:
        comms = communications.encode_msg_without_direction(mine_location[0], mine_location[1])
        if comms != 0 and robot.combat_broadcast_level <= 0:
            # robot.log("Charging mine")
            check.signal_check(robot, comms, 64)
            robot.core_is_ready = 1
            robot.combat_broadcast_level = constants.combat_broadcast_cooldown
    comms = 65533
    if comms != 0 and robot.combat_broadcast_level <= 0:
        check.signal_check(robot, comms, 64)
        robot.core_is_ready = 1
        robot.combat_broadcast_level = constants.combat_broadcast_cooldown

def get_min_friendly_influence_direction(robot, visible_friendly_distance, visible_friendly_list):
    influences_value, influences = mapping.get_corner_friendly_influence(robot)
    sorted_influences_value, sorted_influences = utility.insertionSort(influences_value, influences)
    pos_x = robot.me.x
    pos_y = robot.me.y
    dirc_x, dirc_y = sorted_influences[0]
    fin_dir = pathfinding.bug_walk_toward(robot, (pos_x + dirc_x, pos_y + dirc_y))
    if fin_dir != 0:
        # TRAVIS MOVE CHECK 23
        return check.move_check(robot, fin_dir[0], fin_dir[1], 23)
    else:
        return None

    # robot.log(str((sorted_influences_value, sorted_influences)))


def spot_the_weakness_charge(robot):
    if robot.actual_round_number == 10:
        None

def does_enemy_contain_prophet_units(enemy_list):
    for unit in enemy_list:
        if unit['unit'] == constants.unit_prophet:
            return 1
    return 0

def does_enemy_contain_crusader_units(enemy_list):
    for unit in enemy_list:
        if unit['unit'] == constants.unit_crusader:
            return 1
    return 0

def does_enemy_contain_preacher_units(enemy_list):
    for unit in enemy_list:
        if unit['unit'] == constants.unit_preacher:
            return 1
    return 0

def give_crusader_number(friendly_list):
    crusader_count = 0
    for unit in friendly_list:
        if unit['unit'] == constants.unit_crusader:
            crusader_count +=1
    return crusader_count

def give_crusaders_that_can_attack_nearest_enemy(robot, nearest_enemy, friendly_list):
    nearest_enemy_location = (nearest_enemy['x'], nearest_enemy['y'])
    crusader_count = 0
    for unit in friendly_list:
        if unit['unit'] == constants.unit_crusader:
            friendly_unit_location = (friendly_list['x'], friendly_list['y'])
            if utility.distance(robot, nearest_enemy_location, friendly_unit_location):
                crusader_count +=1
    return crusader_count

def is_robot_the_oldest_crusader_in_range(robot, friendly_list):
    turn_number = robot.me.turn
    for unit in friendly_list:
        if unit['unit'] == constants.unit_crusader:
            if unit['turn'] > turn_number + 5:
                # robot.log(" ID is " + str(robot.me.id) + " Old " + str(unit['turn']) + " New " + str(turn_number))
                return 0
    # robot.log('Oldest')
    return 1

def is_crusader_raiding_core_ready(friendly_list):
    crusader_count = give_crusader_number(friendly_list)
    if crusader_count > 6:
        # robot.log("Go charge")
        return 1
    else:
        return 0

def charge_to_nearest_enemy_mine(robot):
    enemy_locations = mapping.get_on_the_ground_enemy_resources(robot, robot.our_castle_base_or_church_base[0], robot.our_castle_base_or_church_base[1])
    min_distance = 999
    targeted_mine = None
    for iter_i in range(len(enemy_locations)):
        enemy_mine_distance = utility.distance(robot, (robot.me.x, robot.me.y), enemy_locations[iter_i])
        if enemy_mine_distance > constants.crusader_vision_range and enemy_mine_distance < min_distance:
            min_distance = enemy_mine_distance
            targeted_mine = enemy_locations[iter_i]
    return targeted_mine

def bequeath_thee_mine_to_theeself(robot):
    if robot.step < 4:
        return None
    enemy_locations = mapping.get_on_the_ground_enemy_resources(robot, robot.our_castle_base_or_church_base[0], robot.our_castle_base_or_church_base[1])
    check_mine = 0
    for iter_i in range(len(enemy_locations)):
        if str(robot.targeted_enemy_mine) == str(enemy_locations[iter_i]):
            check_mine = 1
            # robot.log("This is the mine **** " + str(robot.bequeathed_mine))
    for iter_i in range(len(enemy_locations)):
        if utility.distance(robot, (robot.me.x, robot.me.y), (enemy_locations[iter_i])) < utility.distance(robot, (robot.me.x, robot.me.y), robot.bequeathed_mine):
            robot.bequeathed_mine = (enemy_locations[iter_i])
            robot.log("This is the mine **** " + str(robot.bequeathed_mine))
    if check_mine == 0:
        return None
    mine_location_x = robot.bequeathed_mine[0]
    mine_location_y = robot.bequeathed_mine[1]
    if robot.piligrim_did_i_shout_my_x_cord == False:
        # robot.log(" abc" + str(mine_location_x + 64))
        robot.castle_talk(mine_location_x + 64)
        robot.piligrim_did_i_shout_my_x_cord = True
    elif robot.piligrim_did_i_shout_my_y_cord == False:
        # robot.log("cde " + str(mine_location_y + 64))
        robot.castle_talk(mine_location_y + 64)
        robot.piligrim_did_i_shout_my_y_cord = True
        robot.bequeathed_mine = None
    else:
        robot.piligrim_did_i_shout_my_x_cord == False
        robot.piligrim_did_i_shout_my_y_cord == False

def only_non_combat_enemy_units_are_seen(robot, visible_enemy_list):
    count = 0
    for unit in visible_enemy_list:
        if unit['unit'] != constants.unit_prophet or unit['unit'] != constants.unit_preacher or unit['unit'] != constants.unit_crusader:
            count += 1
            # There should be atleast one crusader, in enemy list no?
    if count == len(visible_enemy_list):
        # robot.log("I see sacrifices for the lord")
        return 1
    else:
        return 0

def all_visible_enemy_combat_units_are_crusaders(robot, visible_enemy_list):
    count = 0
    is_crusader = 0
    for unit in visible_enemy_list:
        if unit['unit'] != constants.unit_prophet or unit['unit'] != constants.unit_preacher:
            count += 1
            # There should be atleast one crusader, in enemy list no?
        if unit['unit'] == constants.unit_crusader:
            is_crusader += 1
    if count == len(visible_enemy_list) and is_crusader > 0:
        # robot.log("I see a sea of steel")
        return 1
    else:
        return 0

def all_visible_enemy_combat_units_are_preachers(robot, visible_enemy_list):
    count = 0
    is_preacher = 0
    for unit in visible_enemy_list:
        if unit['unit'] != constants.unit_prophet or unit['unit'] != constants.unit_crusader:
            count += 1
        if unit['unit'] == constants.unit_preacher:
            is_preacher += 1
    if count == len(visible_enemy_list) and is_preacher > 0:
        # robot.log("I feel a flock of followers")
        return 1
    else:
        return 0

def is_unit_in_position_against_preachers(robot, visible_friendly_list):
    flag = 0
    pos_x = robot.me.x
    pos_y = robot.me.y
    if is_position_in_any_enemy_attack_range(robot, pos_x, pos_y) == 0:
        flag = 1
        potential_distance = 0
        for friendly_unit in visible_friendly_list:
            if str((friendly_unit['x'], friendly_unit['y'])) == str((pos_x, pos_y)) or friendly_unit['unit'] == constants.unit_pilgrim or friendly_unit['unit'] == constants.unit_church:
                continue
            if utility.distance(robot, (pos_x, pos_y), (friendly_unit['x'], friendly_unit['y'])) < 8:
                # robot.log(str((friendly_unit['x'], friendly_unit['y'])) + " " + str((pos_x, pos_y)))
                flag = 0
                break
            else:
                potential_distance += utility.distance(robot, (pos_x, pos_y), (friendly_unit['x'], friendly_unit['y']))
    return flag

def repositioning_against_preachers(robot, visible_friendly_list):
    directions = None
    distance_list = []
    reposition_position_list = []
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    if robot.me.unit != constants.unit_crusader:
        directions = constants.non_crusader_move_directions
    else:
        directions = constants.crusader_move_directions
    for direction in directions:
        # robot.log("------")
        new_pos_x = pos_x + direction[0]
        new_pos_y = pos_y + direction[1]
        if utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y) or passable_map[new_pos_y][new_pos_x] != 1:
            # robot.log("11")
            continue
        # robot.log("22")
        if is_position_in_any_enemy_attack_range(robot, new_pos_x, new_pos_y) == 0:
            flag = 1
            potential_distance = 0
            for friendly_unit in visible_friendly_list:
                if friendly_unit['unit'] == constants.unit_pilgrim or friendly_unit['unit'] == constants.unit_church:
                    continue
                if utility.distance(robot, (new_pos_x, new_pos_y), (friendly_unit['x'], friendly_unit['y'])) < 8:
                    flag = 0
                    break
                else:
                    potential_distance += utility.distance(robot, (new_pos_x, new_pos_y), (friendly_unit['x'], friendly_unit['y']))
            if flag == 1:
                distance_list.append(potential_distance)
                reposition_position_list.append((new_pos_x, new_pos_y))
    sorted_distance, sorted_reposition_position_list = utility.insertionSort(distance_list, reposition_position_list)
    return sorted_reposition_position_list

def evade_vision_position(robot, visible_enemy_list):
    vision_evasion_position_list = give_postions_where_unit_can_evade_all_enemy_vision(robot)
    if len(vision_evasion_position_list) != 0:
        max_distance = -99
        new_position = None
        for iter_i in range(len(vision_evasion_position_list)):
            sum_of_distance = 0
            for enemy_unit in visible_enemy_list:
                enemy_loc = (enemy_unit['x'], enemy_unit['y'])
                sum_of_distance += utility.distance(robot, enemy_loc, vision_evasion_position_list[iter_i])
            if sum_of_distance > max_distance:
                max_distance = sum_of_distance
                new_position = vision_evasion_position_list[iter_i]
        if new_position != None:
            # TRAVIS MOVE CHECK 18
            return check.move_check(robot, new_position[0] - robot.me.x, new_position[1] - robot.me.y, 18)
    return None

def evade_attack_position(robot, visible_enemy_list):
    attack_evasion_position_list = give_postions_where_unit_can_evade_all_enemy_attack(robot)
    if len(attack_evasion_position_list) != 0:
        max_distance = -99
        new_position = None
        for iter_i in range(len(attack_evasion_position_list)):
            sum_of_distance = 0
            for enemy_unit in visible_enemy_list:
                enemy_loc = (enemy_unit['x'], enemy_unit['y'])
                sum_of_distance += utility.distance(robot, enemy_loc, attack_evasion_position_list[iter_i])
            if sum_of_distance > max_distance:
                max_distance = sum_of_distance
                new_position = attack_evasion_position_list[iter_i]
        if new_position != None:
            # TRAVIS MOVE CHECK 19
            return check.move_check(robot, new_position[0] - robot.me.x, new_position[1] - robot.me.y, 19)

def is_non_combat_friendly_unit_in_vision(visible_friendly_list):
    for unit in visible_friendly_list:
        if unit['unit'] != constants.unit_castle or unit['unit'] != constants.unit_church or unit['unit'] != constants.unit_pilgrim:
            return 1
    return 0

def set_guess_direction(robot):
    if robot.delta_health_reduced != 0 and robot.step != 0:
        robot.guessing_in_direction = (robot.me.x - robot.position_at_end_of_turn[0], robot.me.y - robot.position_at_end_of_turn[1])
        robot.has_taken_a_hit = 2
    elif robot.delta_health_reduced == 0 and robot.has_taken_a_hit != 0:
        robot.has_taken_a_hit -= 1

def give_stats(unit):
    if unit['unit'] == constants.unit_castle:
        return _give_castle_stats()
    elif unit['unit'] ==  constants.unit_church:
        return _give_church_stats()
    elif unit['unit'] == constants.unit_pilgrim:
        return _give_pilgrim_stats()
    elif unit['unit'] == constants.unit_prophet:
        return _give_prophet_stats()
    elif unit['unit'] == constants.unit_crusader:
        return _give_crusader_stats()
    elif unit['unit'] == constants.unit_preacher:
        return _give_preacher_stats()

def _give_castle_stats():
    attack_damage = constants.castle_attack_damage
    speed = 0
    min_attack_range = constants.castle_min_attack_range
    max_attack_range = constants.castle_max_attack_range
    vision_range = constants.castle_vision_range
    has_handicapped_area = 0
    max_health = constants.castle_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_church_stats():
    attack_damage = 0
    speed = 0
    min_attack_range = 0
    max_attack_range = 0
    vision_range = constants.church_vision_range
    has_handicapped_area = 0
    max_health = constants.church_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_pilgrim_stats():
    attack_damage = 0
    speed = constants.pilgrim_speed
    min_attack_range = 0
    max_attack_range = 0
    vision_range = constants.pilgrim_vision_range
    has_handicapped_area = 0
    max_health = constants.pilgrim_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_prophet_stats():
    attack_damage = constants.prophet_attack_damage
    speed = constants.prophet_speed
    min_attack_range = constants.prophet_min_attack_range
    max_attack_range = constants.prophet_max_attack_range
    vision_range = constants.prophet_vision_range
    has_handicapped_area = 1
    max_health = constants.prophet_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_crusader_stats():
    attack_damage = constants.crusader_attack_damage
    speed = constants.crusader_speed
    min_attack_range = constants.crusader_min_attack_range
    max_attack_range = constants.crusader_max_attack_range
    vision_range = constants.crusader_vision_range
    has_handicapped_area = 0
    max_health = constants.crusader_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_preacher_stats():
    attack_damage = constants.preacher_attack_damage
    speed = constants.preacher_speed
    min_attack_range = constants.preacher_min_attack_range
    max_attack_range = constants.preacher_max_attack_range
    vision_range = constants.preacher_vision_range
    has_handicapped_area = 0
    max_health = constants.preacher_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

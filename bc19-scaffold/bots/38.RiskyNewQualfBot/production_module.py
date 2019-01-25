import constants
import utility
import check
import vision
import castles_utility
import mapping
import communications


def _build_manager_castle(robot):
    castle_count = 0
    church_count = 0
    crusader_count = 0
    pilgrim_count = 0
    preacher_count = 0
    prophet_count = 0
    karb_miner_pilgrim = 0
    fuel_miner_pilgrim = 0
    friendly_units, enemy_units = castles_utility.castle_all_friendly_units(robot)
    total_karbonite = vision.all_karbonite(robot)
    total_fuel = vision.all_fuel(robot)
    map_size = len(robot.get_passable_map())
    friendly_castles_num = len(robot.friendly_castles)
    skip_turn = int(friendly_castles_num * (40 ** 2) / (map_size ** 2))

    enemy_distance = None
    opposite_enemy = mapping.find_symmetrical_point(robot, robot.me.x, robot.me.y, robot.map_symmetry)
    if robot.me.x == opposite_enemy[0]:
        enemy_distance = abs(robot.me.y - opposite_enemy[1])
    else:
        enemy_distance = abs(robot.me.x - opposite_enemy[0])
    enemy_distance_ratio = enemy_distance / map_size

    castles_utility._is_castle_under_attack(robot, enemy_units)

    # robot.log(mapping.analyze_map(robot.get_passable_map()))

    for f_unit in friendly_units:
        if f_unit.castle_talk == constants.unit_castle: #0
            castle_count+=1
        elif f_unit.castle_talk == constants.unit_church: #1
            church_count+=1
        elif f_unit.castle_talk == constants.unit_crusader: #3
            crusader_count+=1
        elif f_unit.castle_talk == constants.unit_pilgrim: #2
            pilgrim_count+=1
        elif f_unit.castle_talk == constants.unit_preacher: #5
            preacher_count+=1
        elif f_unit.castle_talk == constants.unit_prophet: #4
            prophet_count+=1
        elif f_unit.castle_talk == 6:
            fuel_miner_pilgrim += 1
            pilgrim_count += 1
        elif f_unit.castle_talk == 7:
            karb_miner_pilgrim += 1
            pilgrim_count += 1
        elif f_unit.castle_talk == 12:
            pilgrim_count+= 1
            castles_utility._pilgrim_warned(robot, f_unit['id'])
        elif f_unit.castle_talk == 14:
            pilgrim_count += 1
            if (robot.karbonite < 70 or robot.fuel < 250) and robot.step > 10 and enemy_distance_ratio > constants.critical_enemy_distance_ratio:
                # robot.log("Waiting for karb and fuel stockpile to build church")
                return None

    # Pushing stuff into lockers
    castles_utility.nicely_push_into_storage_lockers(robot, robot.fuel, 2)
    castles_utility.nicely_push_into_storage_lockers(robot, robot.karbonite, 1)
    castles_utility.nicely_push_into_storage_lockers(robot, pilgrim_count, 4)
    castles_utility.nicely_push_into_storage_lockers(robot, crusader_count, 5)
    castles_utility.nicely_push_into_storage_lockers(robot, preacher_count, 7)
    castles_utility.nicely_push_into_storage_lockers(robot, prophet_count, 6)

    # robot.log(str(robot.me.signal))

    if map_size > 50 and robot.step < 100 and robot.step > 10 and friendly_castles_num > 1 and enemy_distance_ratio > constants.critical_enemy_distance_ratio:
        if robot.fuel <= 200 or robot.karbonite <= 50:
            return None
        if skip_turn > 1:
            if robot.step % skip_turn == 0:
                return None

    if robot.step >= constants.dark_age and robot.step < constants.age_one:
        if crusader_count < 4 and robot.karbonite > 40 and robot.fuel > 100:
            robot.signal(1, 2)
            return castles_utility._castle_build(robot, constants.unit_crusader)
        elif castles_utility._any_unalloted_karbonite_in_castle_vision(robot) and robot.last_built_fuel == True:
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_unassigned_karbonite_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_castle_vision(robot) and robot.last_built_fuel == False:
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_unassigned_fuel_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        else:
            if castles_utility.can_build_crusader(robot):
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, robot.default_unit)

    elif robot.step >= constants.age_one and robot.step < constants.age_two:
        if castles_utility._any_unalloted_karbonite_in_castle_vision(robot) and robot.last_built_fuel == True and robot.pilgrim_train_count < 2:
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_unassigned_karbonite_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                robot.pilgrim_train_count += 1
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_castle_vision(robot) and robot.last_built_fuel == False and robot.pilgrim_train_count < 2:
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_unassigned_fuel_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                robot.pilgrim_train_count += 1
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_karbonite_in_contested(robot) and robot.last_built_fuel == True and robot.pilgrim_train_count < 2:
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_contested_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                robot.pilgrim_train_count += 1
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_contested(robot) and robot.last_built_fuel == False and robot.pilgrim_train_count < 2:
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_contested_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                robot.pilgrim_train_count += 1
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_karbonite_in_friendly(robot) and robot.last_built_fuel == True and robot.pilgrim_train_count < 2:
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_friendly_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                robot.pilgrim_train_count += 1
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_friendly(robot) and robot.last_built_fuel == False and robot.pilgrim_train_count < 2:
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_friendly_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                robot.pilgrim_train_count += 1
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        else:
            if castles_utility.can_build_crusader(robot):
                robot.pilgrim_train_count = 0
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, robot.default_unit)

    elif robot.step >= constants.age_two and robot.step < constants.age_three:
        if castles_utility._any_unalloted_karbonite_in_castle_vision(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_unassigned_karbonite_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_castle_vision(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_unassigned_fuel_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_karbonite_in_contested(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_contested_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_contested(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_contested_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_karbonite_in_friendly(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_friendly_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_friendly(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_friendly_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        else:
            if castles_utility.can_build_crusader(robot):
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, robot.default_unit)

    elif robot.step >= constants.age_three and robot.step < constants.age_four:
        if castles_utility._any_unalloted_karbonite_in_castle_vision(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_unassigned_karbonite_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_castle_vision(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_unassigned_fuel_in_castle_vision(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_karbonite_in_contested(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_contested_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_contested(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_contested_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_karbonite_in_friendly(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_friendly_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_unalloted_fuel_in_friendly(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_friendly_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_safe_karbonite_in_enemy(robot):
            if castles_utility.can_build_pilgrim(robot):
                karb_mine = castles_utility._get_closest_enemy_side_karbonite(robot)
                signal = communications.encode_msg_without_direction(karb_mine[0], karb_mine[1])
                castles_utility.allot_karbonite_mine_to_pilgrim(robot, karb_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = False
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        elif castles_utility._any_safe_fuel_in_enemy(robot):
            if castles_utility.can_build_pilgrim(robot):
                fuel_mine = castles_utility._get_closest_enemy_side_fuel(robot)
                signal = communications.encode_msg_without_direction(fuel_mine[0], fuel_mine[1])
                castles_utility.allot_fuel_mine_to_pilgrim(robot, fuel_mine)
                robot.signal(signal, 2)
                robot.last_built_fuel = True
                return castles_utility._castle_build(robot, constants.unit_pilgrim)
        else:
            if castles_utility.can_build_crusader(robot):
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, robot.default_unit)

    elif robot.step >= constants.age_four and robot.step < 900:
        if robot.karbonite >= 50 and robot.fuel >= 100 and castles_utility.can_build_crusader(robot):
            robot.signal(1, 2)
            return castles_utility._castle_build(robot, robot.default_unit)

    elif robot.step >= 900:
        if robot.karbonite >= 50 and robot.fuel >= 100 and castles_utility.can_build_crusader(robot):
            robot.signal(1, 2)
            return castles_utility._castle_build(robot, constants.unit_preacher)

    # Kamikaze Sensor
    if robot.step >= 800 and robot.step % 50 == 0:
        if len(robot.friendly_castles) >= castle_count:
            map_length = len(robot.get_passable_map())
            if robot.fuel >= map_length / 2:
                robot.signal(65532, (map_length / 2) ** 2) 
            else:
                robot.signal(65532, (robot.fuel) ** 2)


    # if robot.castle_under_attack > 0:
    #     None
    #     #TODO Broadcast with Co-ordinates to send troops. Range set to max of map.
    # else:
    #     # Peaceful Conditions
    #     if robot.step >= 3:
    #         if robot.karbonite >= 15 and robot.fuel > 100 and pilgrim_count < (total_fuel + total_karbonite) * .35 and robot.step < 60:
    #             if prophet_count < pilgrim_count/2:
    #                 robot.signal(1, 2)
    #                 return castles_utility._castle_build(robot, constants.unit_prophet)
    #             else:
    #                 robot.pilgrim_build_number += 1
    #                 temp_store = castles_utility._castle_assign_mine_or_scout(robot)
    #                 if temp_store != 0:
    #                     robot.signal(temp_store, 2)
    #                     return castles_utility._castle_build(robot,constants.unit_pilgrim)
    #                 else:
    #                     robot.signal(65534, 2)
    #         elif robot.karbonite > 100 and robot.fuel > 200:
    #             #  if (crusader_count * 3) < pilgrim_count:
    #                 #  # robot.signal(robot.me.signal + 1, 2)
    #                 #  return castle_build(robot,constants.unit_crusader)
    #             # elif (preacher_count * 2) < crusader_count:
    #             #     # robot.signal(robot.me.signal + 1, 2)
    #             #     return castle_build(robot, constants.unit_preacher)
    #             if prophet_count < pilgrim_count and robot.step > 60 and robot.fuel > 600:
    #                 robot.signal(1, 2)
    #                 return castles_utility._castle_build(robot, constants.unit_prophet)
    #             if pilgrim_count < (total_fuel + total_karbonite) * .55:
    #                 robot.pilgrim_build_number += 1
    #                 temp_store = castles_utility._castle_assign_mine_or_scout(robot)
    #                 if temp_store != 0:
    #                     robot.signal(temp_store, 2)
    #                     return castles_utility._castle_build(robot,constants.unit_pilgrim)
    #                 else:
    #                     robot.signal(65534, 2)
    #             elif robot.step > 300 and robot.karbonite > 600 and robot.fuel > 600:
    #                 robot.signal(1, 2)
    #                 return castles_utility._castle_build(robot, constants.unit_prophet)
    #             elif robot.step > 500 and robot.step < 800 and robot.karbonite > 300 and robot.fuel > 300:
    #                 robot.signal(1, 2)
    #                 return castles_utility._castle_build(robot, constants.unit_prophet)
    #             elif robot.step >= 800:
    #                 #TODO At war change production status
    #                 robot.signal(1, 2)
    #                 return castles_utility._castle_build(robot, constants.unit_crusader)
    #     elif prophet_count < 2 and robot.karbonite >= 25 and robot.step < 10:
    #         robot.signal(1, 2)
    #         return castles_utility._castle_build(robot, constants.unit_prophet)

def _build_manager_church(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = utility.random_cells_around()
    if robot.step < 25 or robot.fuel > 1000:
        for direction in directions:
            if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
                # TRAVIS BUILD CHECK 4
                return check.build_check(robot, constants.unit_crusader, direction[1], direction[0], 4)

    # robot.log("No space to build units anymore for churches")
    return None


def default_production_order(robot):
    unit_type = robot.me.unit
    if unit_type == constants.unit_church:
        return _build_manager_church(robot)
    if unit_type == constants.unit_castle:
        return _build_manager_castle(robot)

def age_one(robot):
    None

import check
import combat_utility
import communications
import constants
import pathfinding
import tactics
import utility
import vision

# TODO - Enemy analysis function
# TODO - All archer formation functions

def give_military_command(robot, received_message = 0, self_signal = 0):
    if received_message == 0 and self_signal == 0:
        return default_military_behaviour(robot)

def _prophet_combat(robot):
    # combat_utility.fill_combat_map(robot)
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)
    fuel = constants.prophet_attack_fuel_cost
    attack_safety_check = 0
    vision_safety_check = 0
    target_robot_id = robot.is_targeting_robot_with_id

    # Move to near lattice point if no enemies visibles and no damage taken
    if len(visible_enemy_list) == 0 and robot.delta_health_reduced == 0 and robot.step != 0:
        # Give resources to church/castle/pilgrim/unit via convoy
        return None

    # Attacked by out-of-vision enemy unit

    # We see an enemy
    if len(visible_enemy_list) != 0:
        attack_safety_check = combat_utility.is_unit_in_any_enemy_attack_range(robot)
        vision_safety_check = combat_utility.is_unit_in_any_enemy_vision_range(robot)

        # Enemy doesn't have vision of bot
        if vision_safety_check == 0:
            enemy_unit = tactics.choose_target(robot, visible_enemy_list, visible_enemy_distance)
            if enemy_unit == None:
                return None
            else:
                # TRAVIS ATTACK CHECK 13
                return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 13, fuel, enemy_unit)

        # Enemy cannot attack the bot
        if attack_safety_check == 0:
            enemy_unit = tactics.choose_target(robot, visible_enemy_list, visible_enemy_distance)
            if enemy_unit == None:
                return None
            else:
                # TRAVIS ATTACK CHECK 14
                return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 14, fuel, enemy_unit)

        if attack_safety_check == 1 and combat_utility.does_enemy_contain_prophet_units(visible_enemy_list) == 0:
            vision_evasion_position_list = combat_utility.give_postions_where_unit_can_evade_all_enemy_vision(robot)
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

            attack_evasion_position_list = combat_utility.give_postions_where_unit_can_evade_all_enemy_attack(robot)
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

        # Fall through all the if cases
        enemy_unit = tactics.choose_target(robot, visible_enemy_list, visible_enemy_distance)
        if enemy_unit == None:
            return None
        else:
            # TRAVIS ATTACK CHECK 15
            return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 15, fuel, enemy_unit)
    return None

def _crusader_combat(robot):
    # combat_utility.fill_combat_map(robot)

    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)
    fuel = constants.crusader_attack_fuel_cost
    attack_safety_check = 0
    vision_safety_check = 0
    target_robot_id = robot.is_targeting_robot_with_id

    # Move to near lattice point if no enemies visibles and no damage taken
    if len(visible_enemy_list) == 0 and robot.delta_health_reduced == 0 and robot.step != 0:
        # Give resources to church/castle/pilgrim/unit via convoy
        return None

    if robot.delta_health_reduced != 0 and robot.step != 0:
        robot.guessing_in_direction = (robot.me.x - robot.position_at_end_of_turn[0], robot.me.y - robot.position_at_end_of_turn[1])
        robot.has_taken_a_hit = 3
    elif robot.delta_health_reduced == 0 and robot.has_taken_a_hit != 0:
        robot.has_taken_a_hit -= 1

    # Attacked by out-of-vision enemy unit
    if len(visible_enemy_list) == 0 and robot.step != 0 and (robot.delta_health_reduced != 0 or robot.has_taken_a_hit != 0):
        guess_enemy_direction_and_move = combat_utility.enemy_direction_guess_and_move(robot, visible_friendly_distance, visible_friendly_list)
        if guess_enemy_direction_and_move != None:
            return guess_enemy_direction_and_move

    # We see an enemy
    if len(visible_enemy_list) != 0:

        # Seen a guessed enemy
        if robot.has_taken_a_hit != 0:
            enemy_pox_x = visible_enemy_list[0]['x']
            enemy_pox_y = visible_enemy_list[0]['y']
            comms = communications.encode_msg_without_direction(enemy_pox_x, enemy_pox_y)
            if comms != 0 and robot.combat_broadcast_level <= 0:
                robot.signal(comms, 8)
                robot.combat_broadcast_level = constants.combat_broadcast_cooldown
        # In attack range
        for iter_i in range(len(visible_enemy_list)):
            enemy_unit = visible_enemy_list[iter_i]
            if visible_enemy_distance[iter_i] <= constants.crusader_max_attack_range:
                # TRAVIS ATTACK CHECK 15
                return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 15, fuel, enemy_unit)

        # Move to the nearest enemy to attack
        closest_pos = combat_utility.give_crusader_charge_location(robot, visible_enemy_list, visible_enemy_distance)
        if closest_pos != None:
            # TRAVIS MOVE CHECK 20
            return check.move_check(robot, closest_pos[0] - robot.me.x, closest_pos[1] - robot.me.y, 20)

def _preacher_combat(robot):
    combat_utility.fill_combat_map(robot)
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)
    fuel = constants.preacher_attack_fuel_cost
    attack_safety_check = 0
    vision_safety_check = 0
    target_robot_id = robot.is_targeting_robot_with_id

    # Move to near lattice point if no enemies visibles and no damage taken
    if len(visible_enemy_list) == 0 and robot.delta_health_reduced == 0 and robot.step != 0:
        # Give resources to church/castle/pilgrim/unit via convoy
        return None

    # Attacked by out-of-vision enemy unit

    # We see an enemy
    if len(visible_enemy_list) != 0:
        attack_safety_check = combat_utility.is_unit_in_any_enemy_attack_range(robot)
        vision_safety_check = combat_utility.is_unit_in_any_enemy_vision_range(robot)

        # Enemy doesn't have vision of bot
        if vision_safety_check == 0:
            enemy_unit = tactics.choose_target(robot, visible_enemy_list, visible_enemy_distance)
            if enemy_unit == None:
                return None
            else:
                # TRAVIS ATTACK CHECK 13
                return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 19, fuel, enemy_unit)

        # Enemy cannot attack the bot
        if attack_safety_check == 0:
            enemy_unit = tactics.choose_target(robot, visible_enemy_list, visible_enemy_distance)
            if enemy_unit == None:
                return None
            else:
                # TRAVIS ATTACK CHECK 14
                return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 20, fuel, enemy_unit)

        # Fall through all the if cases
        enemy_unit = tactics.choose_target(robot, visible_enemy_list, visible_enemy_distance)
        if enemy_unit == None:
            return None
        else:
            # TRAVIS ATTACK CHECK 15
            return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 21, fuel, enemy_unit)

def default_military_behaviour(robot):
    unit_type = robot.me.unit

    if unit_type == constants.unit_crusader:
        return _crusader_combat(robot)
    elif unit_type == constants.unit_preacher:
        return _preacher_combat(robot)
    elif unit_type == constants.unit_prophet:
        return _prophet_combat(robot)

def pilgrimpriority():
    return False

def friendlyfire():
    return False

# DUMP FOR REFERENCE

# def _prophet_combat_a(robot):
#     combat_utility.fill_combat_map(robot)
#     # TODO : store the health of enemy assuming that it has full health
#     # TODO : remove from dictionary if the health of an enemy becomes zero
#     visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
#     visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)

#     if len(visible_enemy_list) != 0:

#         unit_current_pos = (robot.me.x, robot.me.y)
#         unit_will_attack_list = []
#         unit_will_attack_pilgrim_list = []
#         unit_will_attack_id = []
#         unit_cant_attack_list  = []

#         for i in range(len(visible_enemy_list)):
#             enemy = visible_enemy_list[i]
#             enemy_distance = visible_enemy_distance[i]
#             # Attack Range Is Vision Range
#             if enemy['id'] not in robot.has_enemy_target_dict:
#                 robot.has_enemy_target_dict[enemy['id']] = enemy

#             # Units In Attack Range
#             if enemy_distance <= constants.prophet_max_attack_range and enemy_distance >= constants.prophet_min_attack_range:
#                 if enemy['unit'] == constants.unit_pilgrim:
#                     unit_will_attack_pilgrim_list.append(enemy)
#                 else:
#                     unit_will_attack_list.append(enemy)
#                 unit_will_attack_id.append(enemy['id'])
#             elif enemy_distance < robot.prophet_attack_range_min:
#                 unit_cant_attack_list.append(enemy['id'])

#         target_robot_id = robot.is_targeting_robot_with_id
#         enemy = None

#         # # TODO - Include friendly units in these calculations
#         # if len(unit_will_attack_list) == 1:
#         #     enemy = tactics.prophet_will_combat_1vs1(robot, unit_will_attack_list[0])

#         if len(unit_will_attack_list) != 0:
#             enemy = unit_will_attack_list[0]
#             robot.is_targeting_robot_with_id = enemy['id']
#             # return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
#         elif len(unit_will_attack_pilgrim_list) != 0:
#             enemy = unit_will_attack_pilgrim_list[0]
#             robot.is_targeting_robot_with_id = enemy['id']
#             # return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
#         else:
#             # Archers should not be moving towards targets!
#             None

#         if target_robot_id in unit_will_attack_id:
#             old_enemy = robot.has_enemy_target_dict[target_robot_id]
#             if robot.fuel > 25:
#                 # TRAVIS ATTACK CHECK 1
#                 return check.attack_check(robot, old_enemy['x'] - unit_current_pos[0], old_enemy['y'] - unit_current_pos[1], 1)
#         if enemy != None:
#             robot.is_targeting_robot_with_id = enemy['id']
#             if robot.fuel > 25:
#                 # TRAVIS ATTACK CHECK 2
#                 return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 2)
#     return None

# def _crusader_combat(robot):
#     visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
#     if len(visible_enemy_list) == 0:
#         return None
#     else:
#         unit_attackrange_max = constants.crusader_max_attack_range
#         unit_attackdamge = constants.crusader_attack_damage
#         unit_current_pos = (robot.me.x, robot.me.y)
#         unit_will_attack_list = []
#         # unit_will_kill_list = []
#         unit_will_attack_pilgrim_list = []

#         for iter_i in range(len(visible_enemy_list)): # As not sure whether enumerate will work
#             enemy = visible_enemy_list[iter_i]
#             enemy_distance = visible_enemy_distance[iter_i]
#             if enemy_distance <= unit_attackrange_max:
#                 if enemy['unit'] == constants.unit_pilgrim:
#                     unit_will_attack_pilgrim_list.append(enemy)
#                 else:
#                     unit_will_attack_list.append(enemy)

#         if len(unit_will_attack_list) !=0:
#             enemy = unit_will_attack_list[0]
#             # robot.log("Crusader f-i-g-h-t-i-n-g`")
#             # TRAVIS ATTACK CHECK 3
#             return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 3)
#         elif len(unit_will_attack_pilgrim_list) != 0 :
#             enemy = unit_will_attack_pilgrim_list[0]
#             # robot.log("Crusader bullying pilgrim")
#             # TRAVIS ATTACK CHECK 4
#             return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 4)
#         else:
#             enemy = visible_enemy_list[0]
#             # robot.log(enemy)
#             # robot.log(unit_current_pos)
#             move_to, robot.burned_out = pathfinding.astar_search(robot, unit_current_pos, (enemy['x'], enemy['y']), 3)[0]
#             if move_to != None and len(move_to) != 0:
#                 # robot.log("Moving to " + str(move_to))
#                 new_pos_x, new_pos_y = move_to
#                 # TRAVIS MOVE CHECK 1
#                 return check.move_check(robot, new_pos_x - unit_current_pos[0], new_pos_y - unit_current_pos[1], 1)
#         return None

# # TODO - Preacher check which direction the friendlies are in and see if it's safe to drop AOE attack
# # If Preacher between Friendly and Enemy, preacher should attack (?)
# def _preacher_combat(robot):
#     visible_friendly_list = []
#     visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
#     if friendlyfire():
#         visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)
#     if len(visible_enemy_list) == 0:
#         return None
#     else:
#         unit_attack_range_max = constants.preacher_max_attack_range
#         unit_attack_range_min = constants.preacher_min_attack_range
#         unit_attack_damage = constants.preacher_attack_damage
#         unit_current_pos = (robot.me.x, robot.me.y)

#         unit_will_attack_list = []
#         unit_will_attack_pilgrim_list = []
#         friendly_list = []
#         for i in range(len(visible_enemy_list)):
#             enemy = visible_enemy_list[i]
#             enemy_distance = visible_enemy_distance[i]
#             if enemy_distance <= unit_attack_range_max and enemy_distance >= unit_attack_range_min:
#                 if enemy['unit'] == constants.unit_pilgrim:
#                     unit_will_attack_pilgrim_list.append(enemy)
#                 else:
#                     unit_will_attack_list.append(enemy)

#         for i in range(len(visible_friendly_list)):
#             friendly = visible_friendly_list[i]
#             friendly_distance = visible_friendly_distance[i]
#             if friendly_distance <= unit_attack_range_max and friendly_distance >= unit_attack_range_min:
#                 friendly_list.append(friendly)

#         if len(friendly_list) != 0:
#             if friendlyfire():
#                 if len(unit_will_attack_list) != 0:
#                     enemy = unit_will_attack_list[0]
#                     # TRAVIS ATTACK CHECK 5
#                     return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 5)
#                 elif len(unit_will_attack_pilgrim_list) != 0:
#                     enemy = unit_will_attack_pilgrim_list[0]
#                     # TRAVIS ATTACK CHECK 6
#                     return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 6)
#                 else:
#                     # Preachers should not be moving towards targets!
#                     None
#         else:
#             if len(unit_will_attack_list) != 0:
#                 enemy = unit_will_attack_list[0]
#                 if robot.fuel > 25:
#                 # TRAVIS ATTACK CHECK 2
#                     return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 2)# TRAVIS ATTACK CHECK 7
#                     return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 7)
#             elif len(unit_will_attack_pilgrim_list) != 0:
#                 enemy = unit_will_attack_pilgrim_list[0]
#                 # TRAVIS ATTACK CHECK 8
#                 return check.attack_check(robot, enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1], 8)
#             else:
#                 # Preachers should not be moving towards targets!
#                 None
#         return None

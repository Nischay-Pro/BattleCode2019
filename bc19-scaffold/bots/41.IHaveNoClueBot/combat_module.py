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
            vision_evasion_position = None
            vision_evasion_position = combat_utility.evade_vision_position(robot, visible_enemy_list)
            if vision_evasion_position != None:
                return vision_evasion_position

            attack_evasion_position_list = None
            attack_evasion_position_list = combat_utility.evade_attack_position(robot, visible_enemy_list)
            if attack_evasion_position_list != None:
                return attack_evasion_position_list

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
    # if len(visible_enemy_list) == 0 and robot.delta_health_reduced == 0 and robot.step != 0:
    #     # Give resources to church/castle/pilgrim/unit via convoy
    #     return None

    # Bequeath a mine
    if robot.bequeathed_mine != None:
        combat_utility.bequeath_thee_mine_to_theeself(robot)

    # If hit by unit of out vision
    # Guess direction via last turn movement
    combat_utility.set_guess_direction(robot)

    # Attacked by out-of-vision enemy unit
    if len(visible_enemy_list) == 0 and robot.step != 0 and (robot.delta_health_reduced != 0 or robot.has_taken_a_hit != 0):
        # Use influence map to calculate enemy directin
        if combat_utility.give_crusader_number(visible_friendly_list) > 1:
            guess_enemy_direction_and_move_via_friends = combat_utility.get_min_friendly_influence_direction(robot, visible_friendly_distance, visible_friendly_list)
            if guess_enemy_direction_and_move_via_friends != None:
                return guess_enemy_direction_and_move_via_friends
        else:
            guess_enemy_direction_and_move = combat_utility.enemy_direction_guess_and_move(robot, visible_friendly_distance, visible_friendly_list)
            if guess_enemy_direction_and_move != None:
                return guess_enemy_direction_and_move

    # We see an enemy
    if len(visible_enemy_list) != 0:

        # Seen a guessed enemy
        if robot.has_taken_a_hit != 0 and robot.core_is_ready != 1 and len(visible_friendly_list) > 2:
            enemy_pos_x = visible_enemy_list[0]['x']
            enemy_pos_y = visible_enemy_list[0]['y']
            combat_utility.radio_friends_enemy_location(robot, enemy_pos_x, enemy_pos_y)

        # All enemy combat units are crusaders
        if combat_utility.all_visible_enemy_combat_units_are_crusaders(robot, visible_enemy_list):
            # If we are in attack range and not charging
            attack_safety_check = combat_utility.is_unit_in_any_enemy_attack_range(robot)
            if robot.core_is_ready == 0 and attack_safety_check == 1:
                number_of_friendly_combat_units = combat_utility.give_crusaders_that_can_attack_nearest_enemy(robot, visible_enemy_list[0], visible_friendly_list)
                # Enemy greater than friends
                if len(visible_enemy_list) > 1 + number_of_friendly_combat_units and combat_utility.is_non_combat_friendly_unit_in_vision(visible_friendly_list) == 0:
                    attack_evasion_position_list = None
                    attack_evasion_position_list = combat_utility.evade_attack_position(robot, visible_enemy_list)
                    if attack_evasion_position_list != None:
                        return attack_evasion_position_list

        # All enemy combat units are preachers
        if combat_utility.all_visible_enemy_combat_units_are_preachers(robot, visible_enemy_list):
            attack_safety_check = combat_utility.is_unit_in_any_enemy_attack_range(robot)
            if attack_safety_check == 0:
                if len(visible_friendly_list) == 0 or combat_utility.is_unit_in_position_against_preachers(robot, visible_friendly_list) == 1:
                    return 0
                reposition_position_list = combat_utility.repositioning_against_preachers(robot, visible_friendly_list)
                # Make space away from other units, to minimise splash damage
                if reposition_position_list != None and len(reposition_position_list) != 0:
                    # robot.log(reposition_position_list)
                    return check.move_check(robot, reposition_position_list[0][0] - robot.me.x, reposition_position_list[0][1] - robot.me.y, 1313)
                else:
                    # robot.log("********************")
                    return 0

        # In attack range and attacked once
        if robot.is_targeting_robot_with_id != None:
            for iter_i in range(len(visible_enemy_list)):
                enemy_unit = visible_enemy_list[iter_i]
                if visible_enemy_distance[iter_i] <= constants.crusader_max_attack_range and enemy_unit['id'] == robot.is_targeting_robot_with_id:
                    # TRAVIS ATTACK CHECK 15
                    return combat_utility.attack_location(robot, enemy_unit['x'], enemy_unit['y'], 15, fuel, enemy_unit)

        # In attack range and haven't attacked yet
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

    # Core is ready to charge (Core == 7 units)
    if len(visible_friendly_list) > 0 and robot.core_is_ready!= 1 and robot.fuel > 8:
        if combat_utility.is_crusader_raiding_core_ready(visible_friendly_list) == 1 and combat_utility.is_robot_the_oldest_crusader_in_range(robot, visible_friendly_list):
            # robot.log("Charge at" + str(robot.current_move_destination))
            combat_utility.radio_friends_charge_order(robot)


    if len(visible_friendly_list) > 0 and robot.core_is_ready == 1 and robot.targeted_enemy_mine != None:
        # robot.log("888 Check")
        robot.switch_core_off +=1
        if robot.switch_core_off == 3:
            robot.bequeathed_mine = robot.targeted_enemy_mine
        if utility.distance(robot, (robot.me.x, robot.me.y), robot.targeted_enemy_mine) < constants.crusader_vision_range and robot.switch_core_off >= 4:
            # robot.log("*** Refurbish")
            robot.core_is_ready = 0
            robot.switch_core_off = 0

    pos_x, pos_y = robot.me.x, robot.me.y
    if utility.is_cell_resourceful(robot.get_karbonite_map(), robot.get_fuel_map(), pos_x, pos_y):
        coordinates = tactics.find_lattice_point(robot)
        if coordinates:
            robot.current_move_destination = None
            # TRAVIS MOVE CHECK 55
            return check.move_check(robot, coordinates[0] - pos_x, coordinates[1] - pos_y, 55)
    return None

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

    if robot.delta_health_reduced != 0 and robot.step != 0:
        robot.guessing_in_direction = (robot.me.x - robot.position_at_end_of_turn[0], robot.me.y - robot.position_at_end_of_turn[1])
        robot.has_taken_a_hit = 2
    elif robot.delta_health_reduced == 0 and robot.has_taken_a_hit != 0:
        robot.has_taken_a_hit -= 1

    # Attacked by out-of-vision enemy unit
    if len(visible_enemy_list) == 0 and robot.step != 0 and (robot.delta_health_reduced != 0 or robot.has_taken_a_hit != 0):
        if combat_utility.give_crusader_number(visible_friendly_list) > 1:
            guess_enemy_direction_and_move_via_friends = combat_utility.get_min_friendly_influence_direction(robot, visible_friendly_distance, visible_friendly_list)
            if guess_enemy_direction_and_move_via_friends != None:
                return guess_enemy_direction_and_move_via_friends
        guess_enemy_direction_and_move = combat_utility.enemy_direction_guess_and_move(robot, visible_friendly_distance, visible_friendly_list)
        if guess_enemy_direction_and_move != None:
            return guess_enemy_direction_and_move

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

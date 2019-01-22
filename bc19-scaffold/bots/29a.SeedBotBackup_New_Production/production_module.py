import constants
import utility
import check
import vision
import castles_utility
import communications


def _build_manager_castle(robot):
    castle_count = 0
    church_count = 0
    crusader_count = 0
    pilgrim_count = 0
    preacher_count = 0
    prophet_count = 0
    friendly_units, enemy_units = castles_utility.castle_all_friendly_units(robot)
    total_karbonite = vision.all_karbonite(robot)
    total_fuel = vision.all_fuel(robot)

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

    # Pushing stuff into lockers
    castles_utility.nicely_push_into_storage_lockers(robot, robot.fuel, 2)
    castles_utility.nicely_push_into_storage_lockers(robot, robot.karbonite, 1)
    castles_utility.nicely_push_into_storage_lockers(robot, pilgrim_count, 4)
    castles_utility.nicely_push_into_storage_lockers(robot, crusader_count, 5)
    castles_utility.nicely_push_into_storage_lockers(robot, preacher_count, 7)
    castles_utility.nicely_push_into_storage_lockers(robot, prophet_count, 6)

    """ Building units -
        Start with 2 pilgrims per castle (as long as karbonite after building remains above 50).
        If sufficient resources(>100 karb, >200 fuel), build, in order -
            1 crusader per 3 pilgrims
            1 preacher per 2 crusaders (per 6 pilgrims)
            1 prophet per 3 crusaders (per 9 pilgrims)
            1 prophet per 2 resources on map
    """

    # robot.log(str(robot.me.signal))

    if robot.step >= constants.dark_age and robot.step < constants.age_one:
        if robot.karbonite >= 15 and robot.fuel > 100 and pilgrim_count >= (total_fuel + total_karbonite) * .35:
            if prophet_count < pilgrim_count/2:
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, constants.unit_prophet)
            else:
                robot.pilgrim_build_number += 1
                temp_store = castles_utility._castle_assign_mine_or_scout(robot)
                if temp_store != 0:
                    robot.signal(temp_store, 2)
                    return castles_utility._castle_build(robot,constants.unit_pilgrim)
                else:
                    robot.pilgrim_build_number -= 1
                    robot.signal(65534, 2)
    elif robot.step >= constants.age_one and robot.step < constants.age_two:
        if robot.rush_mode == False:
            if robot.karbonite >= 15 and robot.fuel > 100 and pilgrim_count < (total_fuel + total_karbonite) * .50 * robot.multiplier:
                if prophet_count < pilgrim_count:
                    robot.signal(1, 2)
                    return castles_utility._castle_build(robot, robot.default_unit)
                else:
                    robot.pilgrim_build_number += 1
                    temp_store = castles_utility._castle_assign_mine_or_scout(robot)
                    if temp_store != 0:
                        robot.signal(temp_store, 2)
                        return castles_utility._castle_build(robot,constants.unit_pilgrim)
                    else:
                        robot.pilgrim_build_number -= 1
                        robot.signal(65534, 2)
            else:
                None

        else:
            if robot.karbonite >= 25 and robot.fuel > 100 and pilgrim_count < (total_fuel + total_karbonite) * .50 * constants.age_one_economy_under_rush_scale:
                if prophet_count < pilgrim_count:
                    robot.signal(1, 2)
                    return castles_utility._castle_build(robot, robot.default_unit)
                else:
                    robot.pilgrim_build_number += 1
                    temp_store = castles_utility._castle_assign_mine_or_scout(robot)
                    if temp_store != 0:
                        robot.signal(temp_store, 2)
                        return castles_utility._castle_build(robot,constants.unit_pilgrim)
                    else:
                        robot.pilgrim_build_number -= 1
                        robot.signal(65534, 2)
    
    elif robot.step >= constants.age_two and robot.step < constants.age_three:
        if robot.rush_mode == False:
            if robot.karbonite >= 100 and robot.fuel >= 100:
                if pilgrim_count < (total_fuel + total_karbonite) * 0.65:
                    if castles_utility.did_we_max_out_initial_karb_sending(robot):
                        assignment = castles_utility._get_closest_karb_mine_never_sent(robot)
                        if assignment != None:
                            signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                            robot.signal(signal_to_broadcast, 2)
                            castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                            robot.pilgrim_build_number += 1
                            return castles_utility._castle_build(robot, constants.unit_pilgrim)
                        else:
                            if castles_utility.did_we_max_out_initial_fuel_sending(robot):
                                assignment = castles_utility._get_closest_fuel_mine_never_sent(robot)
                                if assignment != None:
                                    signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                                    robot.signal(signal_to_broadcast, 2)
                                    castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                                    robot.pilgrim_build_number += 1
                                    return castles_utility._castle_build(robot, constants.unit_pilgrim)
                    else:
                        assignment = castles_utility._get_closest_our_side_unoccupied_karb_mine(robot)
                        if assignment != None:
                            signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                            robot.signal(signal_to_broadcast, 2)
                            castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                            robot.pilgrim_build_number += 1
                            return castles_utility._castle_build(robot, constants.unit_pilgrim)
                        else:
                            if castles_utility.did_we_max_out_initial_fuel_sending(robot):
                                robot.signal(2, 1)
                                return castles_utility._castle_build(robot, robot.default_unit)                                
                            else:
                                assignment = castles_utility._get_closest_our_side_unoccupied_fuel_mine(robot)
                                if assignment != None:
                                    signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                                    robot.signal(signal_to_broadcast, 2)
                                    castles_utility._update_fuel_mine_pilgrim_assignment(robot, assignment)
                                    robot.pilgrim_build_number += 1
                                    return castles_utility._castle_build(robot, constants.unit_pilgrim) 
                else:
                    robot.signal(1, 2)
                    return castles_utility._castle_build(robot, robot.default_unit)

            else:
                if robot.karbonite <= 100 and robot.fuel >= 100:
                    if castles_utility.did_we_max_out_initial_karb_sending(robot):
                        assignment = castles_utility._get_closest_karb_mine_never_sent(robot)
                        if assignment != None:
                            signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                            robot.signal(signal_to_broadcast, 2)
                            castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                            robot.pilgrim_build_number += 1
                            return castles_utility._castle_build(robot, constants.unit_pilgrim)
                        else:
                            None
                            #TODO Troop Building or send a purge request?
                    else:
                        assignment = castles_utility._get_closest_our_side_unoccupied_karb_mine(robot)
                        if assignment != None:
                            signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                            robot.signal(signal_to_broadcast, 2)
                            castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                            robot.pilgrim_build_number += 1
                            return castles_utility._castle_build(robot, constants.unit_pilgrim)
                elif robot.karbonite >= 100 and robot.fuel <= 100:
                    if castles_utility.did_we_max_out_initial_fuel_sending(robot):
                        assignment = castles_utility._get_closest_fuel_mine_never_sent(robot)
                        if assignment != None:
                            signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                            robot.signal(signal_to_broadcast, 2)
                            castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                            robot.pilgrim_build_number += 1
                            return castles_utility._castle_build(robot, constants.unit_pilgrim)
                    else:
                        assignment = castles_utility._get_closest_our_side_unoccupied_fuel_mine(robot)
                        if assignment != None:
                            signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                            robot.signal(signal_to_broadcast, 2)
                            castles_utility._update_fuel_mine_pilgrim_assignment(robot, assignment)
                            robot.pilgrim_build_number += 1
                            return castles_utility._castle_build(robot, constants.unit_pilgrim) 
                elif robot.karbonite <= 100 and robot.fuel <= 100:
                    if castles_utility.did_we_max_out_initial_karb_sending(robot):
                        if castles_utility.did_we_max_out_initial_fuel_sending(robot):
                            assignment = castles_utility._get_closest_fuel_mine_never_sent(robot)
                            if assignment != None:
                                signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                                robot.signal(signal_to_broadcast, 2)
                                castles_utility._update_karb_mine_pilgrim_assignment(robot, assignment)
                                robot.pilgrim_build_number += 1
                                return castles_utility._castle_build(robot, constants.unit_pilgrim)
                        else:
                            assignment = castles_utility._get_closest_our_side_unoccupied_fuel_mine(robot)
                            if assignment != None:
                                signal_to_broadcast = communications.encode_msg_without_direction(assignment[0], assignment[1])
                                robot.signal(signal_to_broadcast, 2)
                                castles_utility._update_fuel_mine_pilgrim_assignment(robot, assignment)
                                robot.pilgrim_build_number += 1
                                return castles_utility._castle_build(robot, constants.unit_pilgrim) 
                    else:
                        None
        else:
            if robot.karbonite >= 15 and robot.fuel > 50 and pilgrim_count > (total_fuel + total_karbonite) * (1 - constants.age_two_economy_under_rush_scale):
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, robot.default_unit)
            
    elif robot.step >= constants.age_three and robot.step < constants.age_four:

        None
    elif robot.step >= constants.age_four:
        if robot.karbonite >= 100 and robot.fuel >= 500:
            robot.signal(1, 2)
            return castles_utility._castle_build(robot, robot.default_unit)
                




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
                return check.build_check(robot, constants.unit_prophet, direction[1], direction[0], 4)

    # robot.log("No space to build units anymore for churches")
    return None


def default_production_order(robot):
    unit_type = robot.me.unit
    if unit_type == constants.unit_church:
        return _build_manager_church(robot)
    if unit_type == constants.unit_castle:
        return _build_manager_castle(robot)

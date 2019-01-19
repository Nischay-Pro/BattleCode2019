import constants
import utility
import check
import vision
import castles_utility


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
        if f_unit.castle_talk == constants.unit_castle:
            castle_count+=1
        elif f_unit.castle_talk == constants.unit_church:
            church_count+=1
        elif f_unit.castle_talk == constants.unit_crusader:
            crusader_count+=1
        elif f_unit.castle_talk == constants.unit_pilgrim:
            pilgrim_count+=1
        elif f_unit.castle_talk == constants.unit_preacher:
            preacher_count+=1
        elif f_unit.castle_talk == constants.unit_prophet:
            prophet_count+=1

    """ Building units -
        Start with 2 pilgrims per castle (as long as karbonite after building remains above 50).
        If sufficient resources(>100 karb, >200 fuel), build, in order -
            1 crusader per 3 pilgrims
            1 preacher per 2 crusaders (per 6 pilgrims)
            1 prophet per 3 crusaders (per 9 pilgrims)
            1 prophet per 2 resources on map
    """

    # robot.log(str(robot.me.signal))

    if robot.castle_under_attack > 0:
        None
        #TODO Broadcast with Co-ordinates to send troops. Range set to max of map.
    else:
        # Peaceful Conditions
        if prophet_count < 2 and robot.karbonite >= 25 and robot.step < 10:
            robot.signal(1, 2)
            return castles_utility._castle_build(robot, constants.unit_prophet)
        elif robot.karbonite >= 15 and robot.fuel > 100 and pilgrim_count < (total_fuel + total_karbonite) * .35 and robot.step < 60:
            if prophet_count < pilgrim_count/2:
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, constants.unit_prophet)
            else:
                robot.pilgrim_build_number += 1
                temp_store = castles_utility._castle_assign_mine_or_scout(robot)
                if temp_store != 0:
                    robot.signal(temp_store, 2)
                else:
                    robot.signal(65534, 2)
                return castles_utility._castle_build(robot,constants.unit_pilgrim)
        elif robot.karbonite > 100 and robot.fuel > 200:
            #  if (crusader_count * 3) < pilgrim_count:
                #  # robot.signal(robot.me.signal + 1, 2)
                #  return castle_build(robot,constants.unit_crusader)
            # elif (preacher_count * 2) < crusader_count:
            #     # robot.signal(robot.me.signal + 1, 2)
            #     return castle_build(robot, constants.unit_preacher)
            if prophet_count < pilgrim_count and robot.step > 60:
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, constants.unit_prophet)
            if pilgrim_count < (total_fuel + total_karbonite) * .55:
                robot.pilgrim_build_number += 1
                temp_store = castles_utility._castle_assign_mine_or_scout(robot)
                if temp_store != 0:
                    robot.signal(temp_store, 2)
                else:
                    robot.signal(65534, 2)
                return castles_utility._castle_build(robot,constants.unit_pilgrim)
            elif robot.step > 300 and robot.karbonite > 600 and robot.fuel > 600:
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, constants.unit_prophet)
            elif robot.step > 500 and robot.step < 800 and robot.karbonite > 300 and robot.fuel > 300:
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, constants.unit_prophet)
            elif robot.step >= 800:
                #TODO At war change production status
                robot.signal(1, 2)
                return castles_utility._castle_build(robot, constants.unit_crusader)

def _build_manager_church(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = utility.random_cells_around()
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

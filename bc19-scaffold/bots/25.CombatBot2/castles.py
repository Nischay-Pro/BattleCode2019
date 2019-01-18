import utility
import communications
import vision
import mapping
import constants
import check

# Add code for locked castles

#TODO Stockpile
#TODO Pass on total umber of units from last round

def castle(robot):
    # if robot.step % 10 == 0:
    #     robot.log("Script Helper Turn@" + str(robot.step))

    # if robot.step % 10 == 0:
    #     robot.log("Turn Number" + str(robot.step))

    if robot.step < 1:
        _castle_initial_check(robot)

    castle_count = 0
    church_count = 0
    crusader_count = 0
    pilgrim_count = 0
    preacher_count = 0
    prophet_count = 0
    friendly_units, enemy_units = castle_all_friendly_units(robot)
    total_karbonite = vision.all_karbonite(robot)
    total_fuel = vision.all_fuel(robot)

    # TODO - Build combat units, link with production modules?
    _is_castle_under_attack(robot, enemy_units)
    if robot.castle_under_attack > 0:
        None

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

    if prophet_count < 2 and robot.karbonite >= 25 and robot.step < 10:
        robot.signal(1, 2)
        return _castle_build(robot, constants.unit_prophet)
    elif robot.karbonite >= 15 and robot.fuel > 200 and pilgrim_count < (total_fuel + total_karbonite) * .35 and robot.step < 60:
        if prophet_count < pilgrim_count/2:
            robot.signal(1, 2)
            return _castle_build(robot, constants.unit_prophet)
        else:
            robot.pilgrim_build_number += 1
            temp_store = _castle_assign_mine_or_scout(robot)
            if temp_store != 0:
                robot.signal(temp_store, 2)
            else:
                robot.signal(65534, 2)
            return _castle_build(robot,constants.unit_pilgrim)
    elif robot.karbonite > 100 and robot.fuel > 200:
        #  if (crusader_count * 3) < pilgrim_count:
            #  # robot.signal(robot.me.signal + 1, 2)
            #  return castle_build(robot,constants.unit_crusader)
        # elif (preacher_count * 2) < crusader_count:
        #     # robot.signal(robot.me.signal + 1, 2)
        #     return castle_build(robot, constants.unit_preacher)
        if prophet_count < pilgrim_count and robot.step > 60:
            robot.signal(1, 2)
            return _castle_build(robot, constants.unit_prophet)
        if pilgrim_count < (total_fuel + total_karbonite) * .55:
            robot.pilgrim_build_number += 1
            temp_store = _castle_assign_mine_or_scout(robot)
            if temp_store != 0:
                robot.signal(temp_store, 2)
            else:
                robot.signal(65534, 2)
            return _castle_build(robot,constants.unit_pilgrim)
        elif robot.step > 300 and robot.karbonite > 600 and robot.fuel > 600:
            robot.signal(1, 2)
            return _castle_build(robot, constants.unit_prophet)
        elif robot.step > 500 and robot.karbonite > 300 and robot.fuel > 300:
            robot.signal(1, 2)
            return _castle_build(robot, constants.unit_prophet)

    # robot.log(str(robot.me.signal))

def _castle_initial_check(robot):
    if len(robot.fuel_mine_locations_from_this_castle) == 0:
        unused_store, robot.fuel_mine_locations_from_this_castle = utility.get_relative_fuel_mine_positions(robot)
        robot.fuel_mine_occupancy_from_this_castle = [-1 for i in range(len(robot.fuel_mine_locations_from_this_castle))]

    if len(robot.karb_mine_locations_from_this_castle) == 0:
        unused_store, robot.karb_mine_locations_from_this_castle = utility.get_relative_karbonite_mine_positions(robot)
        robot.karb_mine_occupancy_from_this_castle = [-1 for i in range(len(robot.karb_mine_locations_from_this_castle))]

    if robot.castle_health == None:
        robot.castle_health = constants.castle_max_health
    # Castle Damaged This Turn

    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    if len(robot.enemy_castles) == 0:
        robot.enemy_castles.append(mapping.find_symmetrical_point(robot, robot.me.x, robot.me.y, robot.map_symmetry))
        # robot.log(str(robot.enemy_castles))

def _is_castle_under_attack(robot, enemy_units):
    if robot.me.health < robot.castle_health:
        robot.castle_health = robot.me.health
        robot.castle_under_attack = 1
        robot.castle_under_attack_turn = robot.step
    elif robot.castle_under_attack and robot.castle_under_attack_turn + 5 < robot.step and len(enemy_units) == 0:
        # No longer under attack
        robot.castle_under_attack = 0

def _castle_assign_mine_or_scout(robot):
    # TODO - Change as per our requirements of fuel or karbonite
    # TODO - Change occupancy to robot id when reached mine
    # TODO - Add scouts
    # Build a karb mine
    karb_mine_assigned = -1
    fuel_mine_assigned = -1

    for iter_i in range(len(robot.karb_mine_occupancy_from_this_castle)):
        if robot.karb_mine_occupancy_from_this_castle[iter_i] == -1:
            karb_mine_assigned = iter_i
            break

    for iter_j in range(len(robot.fuel_mine_occupancy_from_this_castle)):
        if robot.fuel_mine_occupancy_from_this_castle[iter_j] == -1:
            fuel_mine_assigned = iter_j
            break

    if (robot.pilgrim_build_number % 2 == 1 or fuel_mine_assigned == -1) and karb_mine_assigned != -1:
        robot.karb_mine_occupancy_from_this_castle[karb_mine_assigned] = 0
        mine_pos = robot.karb_mine_locations_from_this_castle[karb_mine_assigned]
        comms = communications.encode_msg_without_direction(mine_pos[0], mine_pos[1])
        return comms
    # Build a fuel mine
    elif (robot.pilgrim_build_number % 2 == 0 or karb_mine_assigned == -1) and fuel_mine_assigned !=-1:
        robot.fuel_mine_occupancy_from_this_castle[fuel_mine_assigned] = 0
        mine_pos = robot.fuel_mine_locations_from_this_castle[fuel_mine_assigned]
        comms = communications.encode_msg_without_direction(mine_pos[0], mine_pos[1])
        return comms

    return 0
def _castle_build(robot, unit_type):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = utility.random_cells_around()

    for direction in directions:
        if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x + direction[1],  pos_y + direction[0]) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            # robot.log("Building unit of type " + str(unit_type) + " at " + str(direction))
            # TRAVIS BUILD CHECK 1
            return check.build_check(robot, unit_type, direction[1], direction[0], 1)

    for direction in directions:
        if not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0]) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            # robot.log("Building unit of type " + str(unit_type) + " at " + str(direction))
            # TRAVIS BUILD CHECK 2
            return check.build_check(robot, unit_type, direction[1], direction[0], 2)
    # robot.log("No space to build units anymore for castles")
    return None

def castle_all_friendly_units(robot):
    all_units = robot.get_visible_robots()

    friendly_units = []
    enemy_units = []
    for unit in all_units:
        if unit.team == None:
            friendly_units.append(unit)
        elif robot.me.team == unit.team:
            friendly_units.append(unit)
        else:
            enemy_units.append(unit)

    return friendly_units, enemy_units

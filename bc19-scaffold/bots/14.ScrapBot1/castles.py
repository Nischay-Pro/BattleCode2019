import utility
import communications
import vision
import mapping
import constants

# Add code for locked castles

#TODO Stockpile
#TODO Pass on total umber of units from last round

def castle(robot):
    # if robot.step % 10 == 0:
    #     robot.log("Script Helper Turn@" + str(robot.step))

    # if robot.step % 10 == 0:
    #    robot.log("Turn Number" + str(robot.step))

    castle_intial_check(robot)

    castle_count = 0
    church_count = 0
    crusader_count = 0
    pilgrim_count = 0
    preacher_count = 0
    prophet_count = 0
    friendly_units = castle_all_friendly_units(robot)
    total_karbonite = vision.all_karbonite(robot)
    total_fuel = vision.all_fuel(robot)


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

    communications.self_communicate_loop(robot)

    """ Building units -
        Start with 2 pilgrims per castle (as long as karbonite after building remains above 50).
        If sufficient resources(>100 karb, >200 fuel), build, in order -
            1 crusader per 3 pilgrims
            1 preacher per 2 crusaders (per 6 pilgrims)
            1 prophet per 3 crusaders (per 9 pilgrims)
            1 prophet per 2 resources on map
    """

    if robot.step < 2 and robot.karbonite > 60:
        robot.signal(robot.me.signal + 1, 2)
        return castle_build(robot, constants.unit_pilgrim)
    elif robot.karbonite > 100 and robot.fuel > 200:
        #  if (crusader_count * 3) < pilgrim_count:
            #  # robot.signal(robot.me.signal + 1, 2)
            #  return castle_build(robot,constants.unit_crusader)
        # elif (preacher_count * 2) < crusader_count:
        #     # robot.signal(robot.me.signal + 1, 2)
        #     return castle_build(robot, constants.unit_preacher)
        if prophet_count < pilgrim_count:
           return castle_build(robot, constants.unit_prophet)
        elif pilgrim_count < (total_fuel + total_karbonite) * .55:
            robot.signal(robot.me.signal + 1, 2)
            return castle_build(robot,constants.unit_pilgrim)
        elif robot.step > 500 and robot.karbonite > 300 and robot.fuel > 300:
            return castle_build(robot, constants.unit_prophet)

    # robot.log(str(robot.me.signal))

def castle_intial_check(robot):
    if len(robot.fuel_mine_location_from_this_castle) == 0:
        robot.fuel_mine_locations_from_this_castle = utility.get_relative_fuel_mine_positions
        robot.fuel_mine_occupancy_from_this_castle = [0 for i in range(len(robot.fuel_mine_locations_from_this_castle))]
    if len(robot.karb_mine_location_from_this_castle) == 0:
        robot.karb_mine_locations_from_this_castle = utility.get_relative_karbonite_mine_positions
        robot.karb_mine_occupancy_from_this_castle = [0 for i in range(len(robot.karbonite_mine_locations_from_this_castle))]
    
    if robot.castle_health == None:
        robot.castle_health = constants.castle_max_health
    # Castle Damaged This Turn
    elif robot.me.health < robot.castle_health:
        robot.castle_health = robot.me.health
        robot.castle_under_attack = 1
        robot.castle_under_attack_turn = robot.step
    elif robot.castle_under_attack and robot.castle_under_attack_turn + 5 < robot.step:
        # No longer under attack
        robot.castle_under_attack = 0


def castle_build(robot, unit_type):
    pos_x = robot.me.x
    pos_y = robot.me.y
    occupied_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()
    directions = utility.random_cells_around()

    for direction in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            # robot.log("Building unit of type " + str(unit_type) + " at " + str(direction))
            return robot.build_unit(unit_type, direction[1], direction[0])
    robot.log("No space to build units anymore for castles")
    return None

def castle_all_friendly_units(robot):
    all_units = robot.get_visible_robots()

    friendly_units = []
    for unit in all_units:
        if unit.team == None:
            friendly_units.append(unit)
        elif robot.me.team == unit.team:
            friendly_units.append(unit)

    return friendly_units


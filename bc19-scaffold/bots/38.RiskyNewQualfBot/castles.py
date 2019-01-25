import utility
import mapping
import constants
import check
import production_module
import castles_utility
import communications
import comm_analyzer

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
        # robot.log(len(mapping.get_friendly_fuel(robot)))
        # robot.log(len(mapping.get_friendly_karbonite(robot)))

    if robot.step < 3:
        comm_analyzer.broadcast_castle_position(robot)

    if robot.step < 4:
        comm_analyzer.get_initial_castle_position(robot)

    if robot.step == 3:
        robot.friendly_castles.append((robot.me['x'], robot.me['y']))
        if robot.other_castle_index_1 != 0:
            robot.friendly_castles.append(tuple(robot.other_castle_1_co_ordinates))
            if robot.other_castle_index_2 != 0:
                robot.friendly_castles.append(tuple(robot.other_castle_2_co_ordinates))
        castles_utility.get_enemy_castles(robot)

    if robot.step >= 4:
        castles_utility._castle_mine_and_karb_processor(robot)

    castles_utility._castle_monitor_mode(robot)

    response = castles_utility._castle_attack_when_attack_range(robot)
    if response != None:
        return response

    a = production_module.default_production_order(robot)
    return a

    # robot.log(str(robot.me.signal))

def _castle_initial_check(robot):
    my_x = robot.me['x']
    my_y = robot.me['y']
    if len(robot.fuel_mine_locations_from_this_castle) == 0:
        unused_store, robot.fuel_mine_locations_from_this_castle = utility.get_sorted_list_from_a_point(my_x, my_y, mapping.get_friendly_fuel(robot))
        robot.fuel_mine_occupancy_from_this_castle = [-1 for i in range(len(robot.fuel_mine_locations_from_this_castle))]

    if len(robot.karb_mine_locations_from_this_castle) == 0:
        unused_store, robot.karb_mine_locations_from_this_castle = utility.get_sorted_list_from_a_point(my_x, my_y, mapping.get_friendly_karbonite(robot))
        robot.karb_mine_occupancy_from_this_castle = [-1 for i in range(len(robot.karb_mine_locations_from_this_castle))]

    if robot.castle_health == None:
        robot.castle_health = constants.castle_max_health
    # Castle Damaged This Turn

    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    temp, fuel = utility.get_relative_fuel_mine_positions(robot)
    enemy_fuel = mapping.get_enemy_fuel(robot)
    for i in range(len(fuel)):
        addable = True
        for j in range(len(enemy_fuel)):
            if fuel[i][0] == enemy_fuel[j][0] and fuel[i][1] == enemy_fuel[j][1]:
                addable = False
        if addable:
            robot.fuel_manager[fuel[i]] = [0, False, False]
        else:
            robot.fuel_manager[fuel[i]] = [0, False, True]

    temp, karb = utility.get_relative_karbonite_mine_positions(robot)
    enemy_karb = mapping.get_enemy_karbonite(robot)
    for i in range(len(karb)):
        addable = True
        for j in range(len(enemy_karb)):
            if karb[i][0] == enemy_karb[j][0] and karb[i][1] == enemy_karb[j][1]:
                addable = False
        if addable:
            robot.karb_manager[karb[i]] = [0, False, False]
        else:
            robot.karb_manager[karb[i]] = [0, False, True]

    # if len(robot.enemy_castles) == 0:
    #     robot.enemy_castles.append(mapping.find_symmetrical_point(robot, robot.me.x, robot.me.y, robot.map_symmetry))
        # robot.log(str(robot.enemy_castles))

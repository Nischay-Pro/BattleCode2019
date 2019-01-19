import utility
import mapping
import constants
import check
import production_module
import signal_module

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

    if robot.step < 3:
        signal_module.broadcastCastlePosition(robot)
    
    if robot.step < 4:
        signal_module.getInitialCastlePosition(robot)

    if robot.step == 4:
        if robot.other_castle_index_1 != 0:
            robot.friendly_castles.append(tuple(robot.other_castle_1_co_ordinates))
            if robot.other_castle_index_2 != 0:
                robot.friendly_castles.append(tuple(robot.other_castle_2_co_ordinates))

    return production_module.default_production_order(robot)

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

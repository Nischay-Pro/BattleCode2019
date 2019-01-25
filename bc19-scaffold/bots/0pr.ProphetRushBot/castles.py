import utility
import mapping
import constants
import check

# Add code for locked castles

#TODO Stockpile
#TODO Pass on total umber of units from last round

def castle(robot):
    pos_x, pos_y = robot.me.x, robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = constants.directions
    # if robot.step <= 20:
    #     for direction in directions:
    #         if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x + direction[1],  pos_y + direction[0]) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
    #             # robot.log("Building unit of type " + str(unit_type) + " at " + str(direction))
    #             # TRAVIS BUILD CHECK 5
    #             return check.build_check(robot, constants.unit_prophet, direction[1], direction[0], 5)
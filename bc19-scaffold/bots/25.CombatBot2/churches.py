import utility
import constants
import production_module
import check

# Add code for locked castles

def church(robot):
    if robot.step < 4 and robot.fuel >= 50 and robot.karbonite >=40:
        # self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
        return production_module.default_production_order(robot)
    elif robot.step > 300 and robot.karbonite > 100 and robot.fuel > 200:
        return _church_build(robot, constants.unit_prophet)
    else:
        None
        # self.log("Castle health: " + self.me['health'])

def _church_build(robot, unit_type):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = utility.random_cells_around()

    for direction in directions:
        if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x + direction[1],  pos_y + direction[0]) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            # robot.log("Building unit of type " + str(unit_type) + " at " + str(direction))
            # TRAVIS BUILD CHECK 5
            return check.build_check(robot, unit_type, direction[1], direction[0], 5)

    for direction in directions:
        if not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0]) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            # robot.log("Building unit of type " + str(unit_type) + " at " + str(direction))
            # TRAVIS BUILD CHECK 6
            return check.build_check(robot, unit_type, direction[1], direction[0], 6)
    # robot.log("No space to build units anymore for castles")
    return None

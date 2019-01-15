import constants
import utility
import communications


def _build_manager_castle(robot, requested_unit_type):
    if robot.step == 0:
        nearest_castles = robot.enemy_castles
        point_data = [robot.me.x, robot.me.y]
        least_distance = utility.get_closest_distance(point_data, nearest_castles)
        robot.log(least_distance)
        robot.nearest_enemy_castle_distance = least_distance
        return robot.castle_talk(least_distance)

    if robot.step == 1:
        robot.log("Checking Danger Levels")
        utility.castle_danger_level(robot)
        danger_level = robot.early_danger_level
        robot.log(danger_level)
        if danger_level == 1:
            robot.log("Danger Level 1")
            robot.early_army_build_queue.append(constants.unit_prophet)
            robot.early_army_build_queue.append(constants.unit_prophet)
            robot.early_army_build_queue.append(constants.unit_prophet)
        elif danger_level == 2:
            robot.log("Danger Level 2")
            robot.early_army_build_queue.append(constants.unit_prophet)
        # Based on Danger Level build counter measures
    
    robot.log(robot.early_army_build_queue)
    if robot.step >= 1:
        if len(robot.early_army_build_queue) != 0:
            robot.log("Emergency Mode")
            unit_type = constants.unit_prophet
            pos_x = robot.me.x
            pos_y = robot.me.y
            occupied_map = robot.get_visible_robot_map()
            passable_map = robot.get_passable_map()
            directions = utility.random_cells_around()
            for direction in directions:
                if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
                    robot.early_army_build_queue.pop(0)
                    robot.log("Building Emergency Unit")
                    if len(robot.early_army_build_queue) == 0:
                        robot.early_danger_level = 0
                        robot.log("Emergency Cleanup")
                    return robot.build_unit(unit_type, direction[1], direction[0])
            robot.log("No space to build emergency units for castles")
        else:
            robot.log("Doing my usual shit")
            robot.log(requested_unit_type)
            unit_type = requested_unit_type
            pos_x = robot.me.x
            pos_y = robot.me.y
            occupied_map = robot.get_visible_robot_map()
            passable_map = robot.get_passable_map()
            directions = utility.random_cells_around()
            for direction in directions:
                if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
                    if unit_type == constants.unit_pilgrim:
                        robot.pilgrim_build_number += 1
                        temp_store = _castle_assign_mine_or_scout(robot)
                        if temp_store != 0:
                            robot.signal(temp_store, 2)
                        else:
                            robot.signal(65534, 2)
                    return robot.build_unit(unit_type, direction[1], direction[0])
            robot.log("No space to build units anymore for churches")
            return None

    #TODO Need to add castle production logic

def _build_manager_church(robot, requested_unit_type):
    unit_type = requested_unit_type
    pos_x = robot.me.x
    pos_y = robot.me.y
    occupied_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()
    directions = utility.random_cells_around()
    for direction in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.build_unit(unit_type, direction[1], direction[0])
    robot.log("No space to build units anymore for churches")
    return None

def default_production_order(robot, requested_unit_type):
    unit_type = robot.me.unit
    if unit_type == constants.unit_church:
        return _build_manager_church(robot, requested_unit_type)
    if unit_type == constants.unit_castle:
        return _build_manager_castle(robot, requested_unit_type)



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
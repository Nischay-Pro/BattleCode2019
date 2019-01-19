import check
import communications
import mapping
import utility
import vision

def recieve_initial_signal(robot):
    unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
    for friendly_unit in friendly_units:
        if friendly_unit.unit == 2 and friendly_unit.signal > 0:
            _prophets_initial_check(robot, friendly_unit)
            break

def _prophets_initial_check(robot, friendly_unit):
    if friendly_unit.signal == 65534:
        robot.our_castle_or_church_base = None
    else:
        robot.our_castle_or_church_base = communications.decode_msg_without_direction(friendly_unit.signal)
        # robot.log("Base castle is "  + str(robot.our_castle_or_church_base))

    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    if len(robot.enemy_castles) == 0 and robot.built_by_a_castle == 1:
        robot.enemy_castles.append(mapping.find_symmetrical_point(robot, robot.our_castle_or_church_base[0], robot.our_castle_or_church_base[1], robot.map_symmetry))

def church_build(robot, unit_type):
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

import utility
import vision
import communications
import constants
import pathfinding
import movement
import mapping

def pilgrim(robot):

    # TODO - Fix random difficult to find timeout errors happening for some pilgrims in large maps (-s 56)
    # TODO - Add scout bots, who scout if no mine to mine
    # communications.self_communicate_loop(robot)

    carry_karb = robot.me.karbonite
    carry_fuel = robot.me.fuel

    # The pilgrim is on a mine and wants to deposit resources
    if carry_fuel > 80 or carry_karb > 18:
        # robot.log("Nearing capacity")
        return pilgrim_full(robot)

    # The pilgrim checks if it has a mine on it's current position
    pilgrim_is_mining = pilgrim_mine(robot)
    if pilgrim_is_mining !=0:
        return pilgrim_is_mining

    # Recieve signal from castle on which mine to go to
    if robot.step == 0:
        unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
        for friendly_unit in friendly_units:
            if friendly_unit.unit == 0 and friendly_unit.signal > 0:
                robot.built_by_a_castle = 1
                robot.built_by_a_church = 0
                _pilgrims_initial_check(robot, friendly_unit)
                break

    if utility.fuel_less_check(robot):
        return None

    # TODO - Add code to make pilgrim move to church or castle rather just building a new church
    # Move Section
    pilgrim_is_moving = pilgrim_move(robot)
    if pilgrim_is_moving !=0:
        return pilgrim_is_moving

#
def _pilgrims_initial_check(robot, friendly_unit):
    if friendly_unit.signal == 65534:
        robot.current_move_destination = None
    else:
        robot.current_move_destination = communications.decode_msg_without_direction(friendly_unit.signal)
        robot.pilgrim_mine_ownership = 1

    robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    if len(robot.enemy_castles) == 0 and robot.built_by_a_castle == 1:
        robot.enemy_castles.append(mapping.find_symmetrical_point(robot, friendly_unit['x'], friendly_unit['y'], robot.map_symmetry))

def pilgrim_move(robot):
    # Emergency case, allows pilgrims to mine
    if robot.fuel <= 2:
        return 0
    pos_x = robot.me.x
    pos_y = robot.me.y

    passable_map = robot.get_passable_map()
    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()
    occupied_map = robot.get_visible_robot_map()
    random_directions = utility.random_cells_around()
    # May change for impossible resources

    if robot.burned_out > 2:
        robot.current_move_destination = None

    if movement.is_completely_surrounded(robot):
        robot.attained_nirvana_on_turn = robot.step
        robot.burned_out += 1
        # robot.log("Completely surrounded pilgrim or attained Nirvana")
        return 0
    elif robot.attained_nirvana_on_turn + constants.pilgrim_nirvana_age > robot.step:
        return 0
    else:
        robot.attained_nirvana_on_turn = -1

    # Capture and start mining any resource if more than 50 turns since creation and no mine
    # TODO - Improve this code snippet to mine, if in visible region and empty
    if robot.me.turn > constants.pilgrim_will_scavenge_closeby_mines_after_turns and robot.me.turn < constants.pilgrim_will_scavenge_closeby_mines_before_turns:
        for direction in random_directions:
            if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and utility.is_cell_resourceful(karb_map, fuel_map, pos_x + direction[1],  pos_y + direction[0]):
                return robot.move(direction[1], direction[0])

    # TODO - Make into scout if too old, which will scout enemy bases
    # If the mine is already occupied
    _is_pilgrim_scavenging(robot)

    # Just move
    if robot.step < robot.pilgrim_mine_age_limt:
        move_command = movement.move_to_destination(robot)
        if move_command != None:
            return move_command


    # Random Movement when not enough time
    for direction in random_directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            robot.has_made_random_movement = 1
            return robot.move(direction[1], direction[0])

    return 0

def _is_pilgrim_scavenging(robot):
    occupied_map = robot.get_visible_robot_map()

    if robot.current_move_destination != None and robot.step < robot.pilgrim_mine_age_limt:
        final_pos_x = robot.current_move_destination[0]
        final_pos_y = robot.current_move_destination[1]
        # TODO - Occupied by pilgrim condition
        if utility.is_cell_occupied(occupied_map, final_pos_x, final_pos_y):
            robot.pilgrim_mine_age_limt -= constants.pilgrim_fails_to_get_mine_aging # Time befells those who have mine impotency
            if robot.pilgrim_type != 2:
                robot.pilgrim_type = 2 # Become a scavenger
                unused_store, robot.pilgrim_scavenge_mine_location_list = utility.get_relative_mine_positions(robot)
                robot.pilgrim_scavenge_mine_occupancy_list = [-1 for i in range(len(robot.pilgrim_scavenge_mine_location_list))]
            for iter_i in range(len(robot.pilgrim_scavenge_mine_location_list)):
                if robot.pilgrim_scavenge_mine_occupancy_list[iter_i] == -1:
                    robot.pilgrim_scavenge_mine_occupancy_list[iter_i] = 0
                    if str(robot.current_move_destination) != str(robot.pilgrim_scavenge_mine_location_list[iter_i]):
                        robot.current_move_destination = robot.pilgrim_scavenge_mine_location_list[iter_i]
                        # Check if new mine is in vision and occupied, then move to next. Counters aging by using good eyes.
                        final_pos_x = robot.current_move_destination[0]
                        final_pos_y = robot.current_move_destination[1]
                        robot.mov_path_between_location_and_destination = None
                        if not utility.is_cell_occupied(occupied_map, final_pos_x, final_pos_y):
                            # robot.log("Scavenger -> " + str(robot.pilgrim_scavenge_mine_occupancy_list))
                            break
    # One more try old man
    if robot.step > robot.pilgrim_mine_age_limt and robot.pilgrim_has_been_revitalised == 0:
        robot.pilgrim_has_been_revitalised = 1
        robot.pilgrim_mine_age_limt += constants.pilgrim_revitalise
        midway_point = len(robot.pilgrim_scavenge_mine_location_list) // 2
        if robot.pilgrim_scavenge_mine_occupancy_list[midway_point] != -1:
            for iter_i in range(midway_point):
                robot.pilgrim_scavenge_mine_occupancy_list[iter_i] = 0
            robot.current_move_destination = robot.pilgrim_scavenge_mine_location_list[midway_point]
            robot.mov_path_between_location_and_destination = None


def pilgrim_mine(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y

    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()

    if utility.is_cell_resourceful(karb_map, fuel_map, pos_x, pos_y):
        robot.signal(0, 0)
        return robot.mine()
    else:
        return 0

def pilgrim_full(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    carry_karb = robot.me.karbonite
    carry_fuel = robot.me.fuel

    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    directions = constants.directions

    if utility.is_cell_resourceful(karb_map, fuel_map, pos_x, pos_y):
        unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
        if friendly_units != None or len(friendly_units) != 0:
            for f_unit in friendly_units:
                dx = f_unit.x - pos_x
                dy = f_unit.y - pos_y
                if f_unit.unit == constants.unit_church or f_unit.unit == constants.unit_castle:
                    for direction in directions:
                        if direction[1] == dx and direction[0] == dy:
                            robot.signal(0, 0)
                            return robot.give(dx, dy, carry_karb, carry_fuel)

                    if robot.step < 50:
                        robot.resource_depot = f_unit
                        dockspots = movement.find_dockspots(robot, robot.resource_depot)
                        fin_dir = (0, 0)
                        for direction in constants.non_crusader_move_directions:
                            for pos in dockspots:
                                if pos[0] == pos_x + direction[0] and pos[1] == pos_y + direction[1]:
                                    if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x, pos_y):
                                        fin_dir = direction
                                    else:
                                        return None

                        if fin_dir[0] != 0 and fin_dir[1] != 0:
                            return robot.move(fin_dir[0], fin_dir[1])

                        fin_dir = pathfinding.bug_walk(passable_map, occupied_map, robot.resource_depot.x, robot.resource_depot.y, pos_x, pos_y)
                        return robot.move(fin_dir[0], fin_dir[1])

    else:
        for direction in directions:
            if pos_x == robot.resource_depot.x + direction[0] and pos_y == robot.resource_depot.y + direction[1]:
                return robot.give(-direction[0], -direction[1], carry_karb, carry_fuel)
        dockspots = movement.find_dockspots(robot, robot.resource_depot)
        fin_dir = (0, 0)
        for direction in constants.non_crusader_move_directions:
            for pos in dockspots:
                if pos[0] == pos_x + direction[0] and pos[1] == pos_y + direction[1]:
                    if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x, pos_y):
                        fin_dir = direction
                    else:
                        return None

        if fin_dir[0] != 0 and fin_dir[1] != 0:
            return robot.move(fin_dir[0], fin_dir[1])

        fin_dir = pathfinding.bug_walk(passable_map, robot.get_visible_robot_map(), robot.resource_depot.x, robot.resource_depot.y, pos_x, pos_y)
        return robot.move(fin_dir[0], fin_dir[1])

    # FIXME - Make churches not be built if castle /other church is in reasonable travel range
    if robot.karbonite > 50 and robot.fuel > 200:
        return _make_church(robot)

def _make_church(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y

    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    directions = constants.directions

    # FIXME - Don't build churches next to each other
    potential_church_postitons = []
    for p_church_pos in directions:
        if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x + p_church_pos[1], pos_y + p_church_pos[0]):
            count = 0
            for direction in directions:
                if not utility.is_out_of_bounds(len(occupied_map), pos_x + p_church_pos[1] + direction[1], pos_y + p_church_pos[0] + direction[0]):
                    if utility.is_cell_resourceful(karb_map, fuel_map, pos_x + p_church_pos[1] + direction[1], pos_y + p_church_pos[0] + direction[0]):
                        count += 1
            potential_church_postitons.append((p_church_pos[0], p_church_pos[1], count))

    max_resource_pos = (0, 0, 0)
    for pos in potential_church_postitons:
        if pos[2] > max_resource_pos[2]:
            max_resource_pos = pos

    # TODO - Build a church at a chokepoint so that enemy pilgrim cannot get into a research rich area

    robot.log("Making a church at (" + int(pos_x + max_resource_pos[1]) + ", " + int(pos_y + max_resource_pos[0]) + ")")
    robot.signal(0, 0)
    return robot.build_unit(constants.unit_church, max_resource_pos[1], max_resource_pos[0])
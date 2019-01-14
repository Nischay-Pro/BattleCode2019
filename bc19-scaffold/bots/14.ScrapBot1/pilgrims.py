import utility
import vision
import communications
import constants
import pathfinding

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

    # Recieve signal from castle on which mine to go to and start self broadcasting
    if robot.me.signal == 0 and robot.current_move_destination == None:
        unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
        for friendly_unit in friendly_units:
            if friendly_unit.unit == 0 and friendly_unit.signal > 0:
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
    robot.built_by_a_castle = 1
    robot.current_move_destination = communications.decode_msg_without_direction(friendly_unit.signal)
    robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
    robot.our_original_castle_location = robot.our_castle_or_church_base

    robot.pilgrim_mine_ownership = 1

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

    # Capture and start mining any resource if more than 50 turns since creation and no mine
    # TODO - Improve this code snippet to mine, if in visible region and empty
    if robot.me.turn > constants.pilgrim_will_scavenge_closeby_mines_after_turns and robot.me.turn < constants.pilgrim_will_scavenge_closeby_mines_before_turns:
        for direction in random_directions:
            if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and (karb_map[pos_y + direction[0]][pos_x + direction[1]] == 1 or fuel_map[pos_y + direction[0]][pos_x + direction[1]] == 1):
                return robot.move(direction[1], direction[0])
    
    # Just move
    if robot.current_move_destination != None:
        # robot.log("Current mov destination is " + str(robot.current_move_destination))
        # Initial search
        if robot.mov_path_between_base_and_mine == None:
            robot.mov_path_between_base_and_mine = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
            if robot.mov_path_between_base_and_mine != None:
                robot.mov_path_index = 0
                new_pos_x, new_pos_y = robot.mov_path_between_base_and_mine[robot.mov_path_index]
                # robot.log("First block , list " + str(robot.mov_path_between_base_and_mine) + " index " + str(robot.mov_path_index))
                return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
        # Reached end of move list
        elif len(robot.mov_path_between_base_and_mine) - 1 == robot.mov_path_index + 1:
            robot.mov_path_index = robot.mov_path_index + 1
            if str(robot.mov_path_between_base_and_mine[robot.mov_path_index]) == str(robot.current_move_destination):
                new_pos_x, new_pos_y = robot.mov_path_between_base_and_mine[robot.mov_path_index]
                # robot.log("Second block , list " + str(robot.mov_path_between_base_and_mine) + " index " + str(robot.mov_path_index))
                robot.mov_path_index = 0
                robot.current_move_destination = None
                return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
            else:
                robot.mov_path_between_base_and_mine = pathfinding.astar_search(robot, (robot.me.x, robot.me.y), robot.current_move_destination, 2)
                robot.mov_path_index = 0
                new_pos_x, new_pos_y = robot.mov_path_between_base_and_mine[robot.mov_path_index]
                # robot.log("Third block , list " + str(robot.mov_path_between_base_and_mine) + " index " + str(robot.mov_path_index))
                return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)
        # In middle of the list    
        else:
            robot.mov_path_index = robot.mov_path_index + 1
            # robot.log(robot.mov_path_between_base_and_mine[robot.mov_path_index])
            new_pos_x, new_pos_y = robot.mov_path_between_base_and_mine[robot.mov_path_index]
            # robot.log("Fourth block , list " + str(robot.mov_path_between_base_and_mine) + " index " + str(robot.mov_path_index))
            return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)

    # Random Movement when not enough time
    for direction in random_directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.move(direction[1], direction[0])

    return 0

def pilgrim_mine(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y

    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()

    if karb_map[pos_y][pos_x] == 1 or fuel_map[pos_y][pos_x] == 1:
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

    if karb_map[pos_y][pos_x] == 1 or fuel_map[pos_y][pos_x] == 1:
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

    # FIXME - Make churches not be built if castle /other church is in vision range
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
        if not utility.is_cell_occupied(occupied_map, pos_x + p_church_pos[1], pos_y + p_church_pos[0]) and passable_map[pos_y + p_church_pos[0]][pos_x + p_church_pos[1]] == 1 and karb_map[pos_y + p_church_pos[0]][pos_x + p_church_pos[1]] != 1 and fuel_map[pos_y + p_church_pos[0]][pos_x + p_church_pos[1]] != 1:
            count = 0
            for direction in directions:
                if not utility.is_out_of_bounds(len(occupied_map), pos_x + p_church_pos[1] + direction[1], pos_y + p_church_pos[0] + direction[0]):
                    if karb_map[pos_y + p_church_pos[0] + direction[0]][pos_x + p_church_pos[1] + direction[1]] == 1 or fuel_map[pos_y + p_church_pos[0] + direction[0]][pos_x + p_church_pos[1] + direction[1]] == 1:
                        count += 1
            potential_church_postitons.append((p_church_pos[0], p_church_pos[1], count))

    max_resource_pos = (0, 0, 0)
    for pos in potential_church_postitons:
        if pos[2] > max_resource_pos[2]:
            max_resource_pos = pos

    robot.log("Making a church at (" + int(pos_x + max_resource_pos[1]) + ", " + int(pos_y + max_resource_pos[0]) + ")")
    robot.signal(0, 0)
    return robot.build_unit(constants.unit_church, max_resource_pos[1], max_resource_pos[0])
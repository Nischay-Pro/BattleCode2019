import utility
import vision
import communications
import constants
import movement

def pilgrim(robot):

    # TODO - Fix random difficult to find timeout errors happening for some pilgrims in large maps (-s 56)
    # TODO - Add scout bots, who scout if no mine to mine
    communications.self_communicate_loop(robot)

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
    if robot.me.signal == 0:
        unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
        for friendly_unit in friendly_units:
            if friendly_unit.unit == 0 and friendly_unit.signal > -1:
                robot.signal(friendly_unit.signal, 0)
                break

    if utility.fuel_less_check(robot):
        return None

    # TODO - Add code to make pilgrim move to church or castle rather just building a new church
    # Move Section
    unit_signal = robot.me.signal
    # If signal is for mine postion, then start self broadcasting that position, edge case is (0,0) mine
    if unit_signal < 6464 and unit_signal > 0:
        robot.signal(add_mine_position_to_signal(robot, unit_signal), 0)

    # robot.log('Position is ' + str(pos_x) + ' ' + str(pos_y))

    pilgrim_is_moving = pilgrim_move(robot, unit_signal)
    if pilgrim_is_moving !=0:
        return pilgrim_is_moving

def add_mine_position_to_signal(robot, unit_signal):
    # Do nothing
    if unit_signal == 0:
        return 0
    # TODO - Implement emergency measures
    elif unit_signal == 65536 - 1:
        # Find new mine to mine
        None
    else:
        unused_store , mine_positons = utility.get_relative_mine_positions(robot)
        return communications.convert_position_to_message(*(mine_positons[unit_signal - 1]))

def pilgrim_move(robot, unit_signal):
    if robot.fuel <= 2 :
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
    if unit_signal >= 6464:
        move_to = move_to_specified_mine(robot, unit_signal)
        if move_to != None:
            # robot.log("check")
            new_pos_x, new_pos_y = move_to
            return robot.move(new_pos_x - pos_x, new_pos_y - pos_y)

    # Random Movement when not enough time
    for direction in random_directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.move(direction[1], direction[0])

    return 0

def move_to_specified_mine(robot, unit_signal):
    return movement.move_to_specified_position(robot, unit_signal)

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
        if friendly_units:
            for f_unit in friendly_units:
                dx = f_unit.x - pos_x
                dy = f_unit.y - pos_y
                if f_unit.unit == constants.unit_church or f_unit.unit == constants.unit_castle:
                    if (dy, dx in directions) and abs(dx) <= 1 and abs(dy) <= 1 and (robot.get_visible_robot_map()[pos_y + dy][pos_x + dx] > 0):
                        robot.signal(0, 0)
                        return robot.give(dx, dy, carry_karb, carry_fuel)

    # FIXME - Make churches not be built if castle /other church is in vision range
    _make_church(robot)

def _make_church(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y

    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()
    directions = constants.directions

    potential_church_postitons = []
    for church_pos in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + church_pos[1],  pos_y + church_pos[0])) and passable_map[pos_y + church_pos[0]][pos_x + church_pos[1]] == 1 and karb_map[pos_y + church_pos[0]][pos_x + church_pos[1]] != 1 and fuel_map[pos_y + church_pos[0]][pos_x + church_pos[1]] != 1:
            count = 0
            for direction in directions:
                if not utility.is_out_of_bounds(len(occupied_map), pos_x + church_pos[1] + direction[1], pos_y + church_pos[0] + direction[0]):
                    if karb_map[pos_y + church_pos[0] + direction[0]][pos_x + church_pos[0] + direction[1]] == 1 or fuel_map[pos_y + church_pos[0] + direction[0]][pos_x + church_pos[0] + direction[1]] == 1:
                        count += 1
            potential_church_postitons.append((church_pos[0], church_pos[1], count))

    # robot.log((pos_y, pos_x))
    # robot.log(potential_church_postitons)

    max_resource_pos = (0, 0, 0)
    for pos in potential_church_postitons:
        if pos[2] > max_resource_pos[2]:
            max_resource_pos = pos

    # robot.log(max_resource_pos)

    if robot.karbonite > 50 and robot.fuel > 200:
        # robot.log("Making a church at [(x, y)](" + int(pos_x + max_resource_pos[1]) + ", " + int(pos_y + max_resource_pos[0]) + ")")
        robot.signal(0, 0)
        return robot.build_unit(constants.unit_church, max_resource_pos[1], max_resource_pos[0])
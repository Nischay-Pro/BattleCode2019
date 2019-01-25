import utility
import constants
import mapping

# ONLY FOR NON CRUSADER UNITS
def bug_walk_toward(robot, destination):
    pos_x, pos_y = robot.me.x, robot.me.y
    # robot.log("pos " + str((pos_x, pos_y)))
    # robot.log("des " + str(destination))

    i_direction = _choose_ideal_direction(destination[0], destination[1], pos_x, pos_y, robot)
    # robot.log("idir " + str(i_direction))

    return _walker(robot, i_direction)

def bug_walk_away(robot, destination):
    pos_x, pos_y = robot.me.x, robot.me.y

    i_direction_toward = _choose_ideal_direction(destination[0], destination[1], pos_x, pos_y, robot)
    i_direction = (-i_direction_toward[0], -i_direction_toward[1])

    return _walker(robot, i_direction)

def _choose_ideal_direction(des_x, des_y, pos_x, pos_y, robot = None):
    unit_type = None
    diff_x = des_x - pos_x
    diff_y = des_y - pos_y
    # Normalise
    dir_x = 0
    dir_y = 0
    if diff_x != 0:
        dir_x = diff_x//abs(diff_x)
    if diff_y != 0:
        dir_y = diff_y//abs(diff_y)

    if robot != None:
        unit_type = robot.me.unit

    # Objective - Go diagonal until one coordinate matches then straight to destination
    # Diagonal movement
    if diff_x != 0 and diff_y != 0:
        if unit_type == constants.unit_crusader:
            if abs(diff_x) > 1 and abs(diff_y) > 1:
                return (dir_x * 2, dir_y * 2)
            if abs(diff_x) > 1 and abs(diff_y) == 1:
                return (dir_x * 2, dir_y)
            if abs(diff_x) == 1 and abs(diff_y) > 1:
                return (dir_x, dir_y * 2)
        else:
            return (dir_x, dir_y)
    # Movement on x_axis
    if diff_x == 0 and diff_y != 0:
        # If two steps away, move one step so as to not move into occupied
        if unit_type == constants.unit_crusader:
            if abs(diff_y) > 2:
                return (0, dir_y * 3)
        if abs(diff_y) > 1:
            return (0, dir_y * 2)
        else:
            return (0, dir_y)
    # Same for y_axis
    if diff_x != 0 and diff_y == 0:
        if unit_type == constants.unit_crusader:
            if abs(diff_x) > 2:
                return (dir_x * 3, 0)
        if abs(diff_x) > 1:
            return (dir_x * 2, 0)
        else:
            return (dir_x, 0)

    return 0

def _walker(robot, i_direction):
    if i_direction == 0:
        # robot.log("0 " + 0)
        return 0

    pos_x, pos_y = robot.me.x, robot.me.y
    passable_map = robot.get_passable_map()
    occupied_map = robot.get_visible_robot_map()

    if robot.bug_walk_c_w == None:
        if not utility.is_cell_occupied(occupied_map, pos_x + i_direction[0], pos_y + i_direction[1]):
            if passable_map[pos_y + i_direction[1]][pos_x + i_direction[0]] == 1:
                robot.bug_walk_index = None
                robot.bug_walk_c_w = None
                # robot.log("1 " + str(i_direction))
                return i_direction

    directions = constants.non_crusader_move_directions
    if robot.me.unit == constants.unit_crusader:
        directions = constants.crusader_move_directions
    size = len(directions)
    itr_num = size // 2

    if robot.bug_walk_index == None:
        index = -1

        for i in range(size):
            if directions[i][0] == i_direction[0] and directions[i][1] == i_direction[1]:
                index = i

        if index == -1:
            # robot.log("2 " + 0)
            return 0

        robot.bug_walk_index = index
        _iter = 0
        while _iter < itr_num:
            _iter += 1
            i = index + _iter
            if i >= size:
                i -= size
            j = index - _iter
            if j < 0:
                j += size
            if not utility.is_cell_occupied(occupied_map, pos_x + directions[i][0], pos_y + directions[i][1]):
                if passable_map[pos_y + directions[i][1]][pos_x + directions[i][0]]:
                    if not utility.is_cell_occupied(occupied_map, pos_x + directions[j][0], pos_y + directions[j][1]):
                        if passable_map[pos_y + directions[j][1]][pos_x + directions[j][0]]:
                            a_c_w_occupiability = mapping.get_area_occupiability(pos_x + directions[i][0], pos_y + directions[i][1], robot)
                            c_w_occupiability = mapping.get_area_occupiability(pos_x + directions[j][0], pos_y + directions[j][1], robot)
                            if a_c_w_occupiability > c_w_occupiability:
                                robot.bug_walk_c_w = False
                                # robot.log("3 " + str(directions[i]))
                                return directions[i]
                            else:
                                robot.bug_walk_c_w = True
                                # robot.log("4 " + str(directions[j]))
                                return directions[j]
                    robot.bug_walk_c_w = False
                    # robot.log("5 " + str(directions[i]))
                    return directions[i]
            if not utility.is_cell_occupied(occupied_map, pos_x + directions[j][0], pos_y + directions[j][1]):
                if passable_map[pos_y + directions[j][1]][pos_x + directions[j][0]]:
                    robot.bug_walk_c_w = True
                    # robot.log("6 " + str(directions[j]))
                    return directions[j]

    else:
        index = robot.bug_walk_index
        _iter = -1
        while _iter < itr_num:
            _iter += 1
            if robot.bug_walk_c_w:
                i = index - _iter
                if i < 0:
                    i += size
            else:
                i = index + _iter
                if i >= size:
                    i -= size
            if not utility.is_cell_occupied(occupied_map, pos_x + directions[i][0], pos_y + directions[i][1]):
                if passable_map[pos_y + directions[i][1]][pos_x + directions[i][0]]:
                    if _iter == 0:
                        robot.bug_walk_c_w = None
                    # robot.log("7 " + str(directions[i]))
                    return (directions[i])

        index = robot.bug_walk_index
        _iter = -1

        while _iter < itr_num:
            _iter += 1
            if not robot.bug_walk_c_w:
                i = index - _iter
                if i < 0:
                    i += size
            else:
                i = index + _iter
                if i >= size:
                    i -= size
            if not utility.is_cell_occupied(occupied_map, pos_x + directions[i][0], pos_y + directions[i][1]):
                if passable_map[pos_y + directions[i][1]][pos_x + directions[i][0]]:
                    if _iter == 0:
                        robot.bug_walk_c_w = None
                    robot.bug_walk_c_w = not robot.bug_walk_c_w
                    # robot.log("8 " + str(directions[i]))
                    return (directions[i])

    # robot.log("9 " + 0)
    return 0

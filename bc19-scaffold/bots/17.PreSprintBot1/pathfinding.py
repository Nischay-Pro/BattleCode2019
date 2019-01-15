import math
import utility
import constants
import random

# Since no collection
def _is_higher_than(a, b):
    if a == None or b == None:
        return True
    return a[1] > b[1] or (a[1] == b[1] and a[2] < b[2])

# TODO - Add a fuel option and initialise the dirs vector, do stuff to it on the basis of that
def astar_search(robot, pos_initial, pos_final, unit_type_move = 2):

    if unit_type_move == 2:
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1), (0, 2), (0, -2), (2, 0), (-2, 0)]
    elif unit_type_move == 1:
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)]
    elif unit_type_move == 3:
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1),
                (0, 2), (0, -2), (2, 0), (-2, 0), (-1, 2), (1, 2), (1, -2), (-1, -2),
                (2, -1), (2, 1), (-2, 1), (-2, -1), (2, 2), (2, -2), (-2, 2), (-2, -2),
                (0, 3), (0, -3), (3, 0), (-3, 0)]
    nodes = [None]
    insert_counter = 0
    block_kicker = 0

    came_from = {}
    cost_so_far = {}
    came_from[pos_initial] = None
    cost_so_far[pos_initial] = 0
    occupied_map = robot.get_visible_robot_map()
    passable_map = robot.get_passable_map()

    if utility.is_out_of_bounds(occupied_map, pos_final[0], pos_final[1]) or not passable_map[pos_final[1]][pos_final[0]]:
        return None

    def retrace_path(pos_initial, pos_final, came_from):
        current = pos_final
        path = []
        while current != pos_initial:
           path.append(current)
           current = came_from[current]
        # path.append(pos_initial)
        path.reverse()
        return path

    def neighbours(pos_intermediate):
        pos_x, pos_y = pos_intermediate
        result = []
        for dirc in dirs:
            new_pos_x = pos_x + dirc[1]
            new_pos_y = pos_y + dirc[0]
            if not utility.is_cell_occupied(occupied_map, new_pos_x, new_pos_y) and passable_map[new_pos_y][new_pos_x]:
                result.append((new_pos_x , new_pos_y))
        return result

    def _heapify(nodes, new_node_index):
        while 1 < new_node_index:
            new_node = nodes[new_node_index]
            if new_node_index % 2 == 0:
                parent_index = new_node_index / 2
            else:
                parent_index = (new_node_index - 1) / 2
            parent_node = nodes[parent_index]
            # Parent too big?
            if _is_higher_than(parent_node, new_node):
                break
            # Swap with parent
            tmp_node = parent_node
            nodes[parent_index] = new_node
            nodes[new_node_index] = tmp_node
            # Continue further up
            new_node_index = parent_index
        return nodes

    # Add a new node with a given priority
    def add(nodes, value, priority, insert_counter):
        new_node_index = len(nodes)
        insert_counter += 1
        nodes.append((value, priority, insert_counter))
        # Move the new node up in the hierarchy
        _heapify(nodes, new_node_index)
        return insert_counter

    # Remove the top element and return it
    def pop(nodes):
        if len(nodes) == 1:
            raise LookupError("Heap is empty")
        result = nodes[1][0]
        # Move empty space down
        empty_space_index = 1
        while empty_space_index * 2 < len(nodes):
            left_child_index = empty_space_index * 2
            right_child_index = empty_space_index * 2 + 1
            # Left child wins
            if (len(nodes) <= right_child_index or _is_higher_than(nodes[left_child_index], nodes[right_child_index])):
                nodes[empty_space_index] = nodes[left_child_index]
                empty_space_index = left_child_index
            # Right child wins
            else:
                nodes[empty_space_index] = nodes[right_child_index]
                empty_space_index = right_child_index
        # Swap empty space with the last element and heapify
        last_node_index = len(nodes) - 1
        nodes[empty_space_index] = nodes[last_node_index]
        _heapify(nodes, empty_space_index)
        # Throw out the last element
        nodes.pop()
        return result

    # Will be really important later
    def astar_heuristic(pos_intermediate, pos_final):
        (x1, y1) = pos_intermediate
        (x2, y2) = pos_final
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        heuristic = (dx + dy)
        return heuristic * (constants.pathfinding_heuristic_multiplier)

    insert_counter = add(nodes, pos_initial, 0, insert_counter)


    while len(nodes) > 1:
        current = pop(nodes)
        if str(current) == str(pos_final) or block_kicker > constants.pathfinding_power or insert_counter > 1.5 * constants.pathfinding_power:
            # robot.log("=> * " + str(len(nodes)))
            return retrace_path(pos_initial, current, came_from)
        for iter_a in neighbours(current):
            new_cost = cost_so_far[current] + 1
            if len(iter_a) != 0 and (iter_a not in cost_so_far or new_cost < cost_so_far[iter_a]):
                cost_so_far[iter_a] = new_cost
                priority = new_cost + astar_heuristic(iter_a, pos_final)
                # robot.log(str(priority))
                insert_counter =  add(nodes, iter_a, -priority, insert_counter)
                came_from[iter_a] = current
        block_kicker += 1
    # robot.log(came_from)

    return retrace_path(pos_initial, pos_final, came_from)

def _choose_bug_walk_direction(des_x, des_y, pos_x, pos_y):
    diff_x = des_x - pos_x
    diff_y = des_y - pos_y
    dir_x = diff_x/abs(diff_x)
    dir_y = diff_y/abs(diff_y)

    if diff_x != 0 and diff_y != 0:
        return (dir_x, dir_y)
    elif diff_x == 0 and diff_y != 0:
        if abs(diff_y) == 2:
            return (0, dir_y)
        else:
            return (0, 2 * dir_y)
    elif diff_x != 0 and diff_y == 0:
        if abs(diff_x) == 2:
            return (dir_x, 0)
        else:
            return (2 * dir_x, 0)

def bug_walk(passable_map, occupied_map, des_x, des_y, pos_x, pos_y):
    direction = _choose_bug_walk_direction(des_x, des_y, pos_x, pos_y)

    diff_x = des_x - pos_x
    diff_y = des_y - pos_y
    dir_x = diff_x/abs(diff_x)
    dir_y = diff_y/abs(diff_y)

    if not utility.is_cell_occupied(occupied_map, pos_x + direction[0], pos_y + direction[1]):
        if passable_map[pos_y + direction[1]][pos_x + direction[0]] == 1:
            return (direction[0], direction[1])
    elif abs(direction[0]) == 1 and abs(direction[1]) == 1:
        if not utility.is_cell_occupied(occupied_map, pos_x, pos_y + direction[1] * 2):
            if passable_map[pos_y + direction[1] * 2][pos_x] == 1:
                return (0, direction[1] * 2)
        elif not utility.is_cell_occupied(occupied_map, pos_x + direction[0] * 2, pos_y):
            if passable_map[pos_y][pos_x + direction[0] * 2] == 1:
                return (direction[0] * 2, 0)
    elif direction[0] == 0:
        if not utility.is_cell_occupied(occupied_map, pos_x + dir_x, pos_y + dir_y):
            if passable_map[pos_y + dir_y][pos_x + dir_x] == 1:
                return (dir_x, dir_y)
        elif not utility.is_cell_occupied(occupied_map, pos_x + dir_x * 2, pos_y):
            if passable_map[pos_y][pos_x + dir_x * 2] == 1:
                return (dir_x * 2, 0)
        elif not utility.is_cell_occupied(occupied_map, pos_x + dir_x, pos_y):
            if passable_map[pos_y][pos_x + dir_x] == 1:
                return (dir_x, 0)
    elif direction[1] == 0:
        if not utility.is_cell_occupied(occupied_map, pos_x + dir_x, pos_y + dir_y):
            if passable_map[pos_y + dir_y][pos_x + dir_x] == 1:
                return (dir_x, dir_y)
        elif not utility.is_cell_occupied(occupied_map, pos_x, pos_y + dir_y * 2):
            if passable_map[pos_y + dir_y * 2][pos_x ] == 1:
                return (0, dir_y * 2)
        elif not utility.is_cell_occupied(occupied_map, pos_x, pos_y + dir_y):
            if passable_map[pos_y + dir_y][pos_x ] == 1:
                return (0, dir_y)
    random_movements = list(constants.non_crusader_move_directions)
    random.shuffle(random_movements, random.random)
    for movement in random_movements:
        if not utility.is_cell_occupied(occupied_map, pos_x + movement[0], pos_y + movement[1]):
            if passable_map[pos_y + movement[1]][pos_x + movement[0]] == 1:
                return (movement[0], movement[1])
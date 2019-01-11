import utility

def prophet(robot):
    prophet_move(robot)

def prophet_move(robot):
    directions = utility.cells_around()

    for direction in directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            return robot.move(direction[1], direction[0])
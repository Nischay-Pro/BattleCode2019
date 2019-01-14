import utility

def message_to_castles(robot, mesg_type):
    robot.castleTalk(mesg_type)
    # # Position requesting for pilgrims
    # if mesg_type == 0:
    #     temp_store = ((robot.me.x * 1000) + robot.me.y) * 1000 + 0
    #     robot.castleTalk(temp_store)
    # # Position requesting for combat units
    # if mesg_type == 1:
    #     temp_store = ((robot.me.x * 1000) + robot.me.y) * 1000 + 1
    #     robot.castleTalk(temp_store)

def self_communicate_loop(robot):
    robot.signal(robot.me.signal, 0)

def convert_position_to_message(pos_x, pos_y):
    return pos_x * 100 + pos_y + 6464

def convert_message_to_position(message):
    message = message - 6464
    return (message //100, message % 100)

def can_compute_others(message: int) -> bool:
    bin_str = utility.convert_to_binary(message)
    if bin_str[0] == "0":
        return False
    else:
        return True

def message_parsing(message: int, flag: int) -> bool:
    if flag == 1:
        return can_compute_others(message)
    else:
        # TODO: implement other flag logic
        return False

def _store_destination(dest_x: int, dest_y: int, bin_list: list) -> None:
    '''
    dest_x: abscissa of mine's location (decimal)
    dest_y: ordinate of mine's location (decimal)
    bin_list: self loop message of pilgrim as a list of string (binary
    representation)

    First 4 bits of bin_list are reserved for storing information about next
    move.
    '''
    x_bin = utility.convert_to_binary(dest_x)
    y_bin = utility.convert_to_binary(dest_y)
    start = 4
    # copy binary of x to self loop message
    for i in range(10, 16):
        bin_list[start] = x_bin[i]
        start += 1
    # copy binary of y to self loop message
    for i in range(10, 16):
        bin_list[start] = y_bin[i]
        start += 1

def _store_next_step(astar_path: list, bin_list: list, directions: list) -> None:
    '''
    The first 4 bits are used to store the next step
    directions (list): 12 movements of pilgrim (check pilgrim_directions in
    constant module)
    '''
    if len(astar_path) == 1:
        bin_list[3] = '1'
        for i in range(3):
            bin_list[i] = '0'
        return None

    step = astar_path[0]
    second_step = astar_path[1]
    dx = second_step[0] - step[0]
    dy = second_step[1] - step[1]
    ans = None
    for i in range(len(directions)):
        direction = directions[i]
        if (dx, dy) == direction:
            ans = i
            break
    step_byte = utility.convert_to_binary(ans)
    iter_ = 0
    for i in range(12, 16):
        bin_list[iter_] = step_byte[i]
        iter_ += 1

def encode_msg_with_direction(dest_x: int, dest_y: int,
        astar_path: list, directions: list) -> int:
    bin_list = ['0' for i in range(16)]
    _store_destination(dest_x, dest_y, bin_list)
    _store_next_step(astar_path, bin_list, directions)
    return utility.convert_to_decimal("".join(bin_list))

def encode_msg_without_direction(dest_x: int, dest_y: int) -> int:
    bin_list = ['0' for i in range(16)]
    _store_destination(dest_x, dest_y, bin_list)
    return utility.convert_to_decimal("".join(bin_list))

def decode_msg_with_direction(message: int, directions: list) -> tuple:
    binary_str = utility.convert_to_binary(message)
    direction = utility.convert_to_decimal(binary_str[0:4])
    x_destination = utility.convert_to_decimal(binary_str[4:10])
    y_destination = utility.convert_to_decimal(binary_str[10:16])
    return (direction, x_destination, y_destination)

def decode_msg_without_direction(message: int) -> tuple:
    binary_str = utility.convert_to_binary(message)
    x_destination = utility.convert_to_decimal(binary_str[4:10])
    y_destination = utility.convert_to_decimal(binary_str[10:16])
    return (x_destination, y_destination)

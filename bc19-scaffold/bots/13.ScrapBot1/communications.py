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


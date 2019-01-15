import utility
import movement
import pathfinding


# General tactics for all units

def simple_attack(robot):
    None

def simulate_conbat_result(robot):
    None

def increase_influence_at_submap(robot, pos_x, pos_y):
    None

# Specific tactics for units
def kiting_by_prophet(robot):
    None

def should_combat_unit_be_at_battle_front(robot) -> bool:
    '''
    To check if a combat unit should be sent to battle front.
    The combat unit should be sent to battle front if and only if it is given
    birth by castle and it has a destination.
    '''
    robot.log("Destination " + str(robot.current_move_destination))
    # robot.log(str(robot.mov_path_between_location_and_destination))
    # robot.log("Build by castle: " + str(robot.built_by_a_castle))
    # robot.log("Home loc: " + str(robot.our_castle_or_church_base))
    if not robot.current_move_destination: return False
    # elif not robot.mov_path_between_location_and_destination: return False
    elif robot.built_by_a_church: return False
    else: return True

def send_combat_unit_to_battle_front(robot, ratio: float, delta: float):
    dest = robot.current_move_destination
    origin = robot.our_castle_or_church_base
    pos_x, pos_y = robot.me.x, robot.me.y
    is_combat_unit_at_front = utility.distance_ratio(robot, dest, ratio, delta)
    if is_combat_unit_at_front:
        robot.log("Inside if")
        robot.current_move_destination = None
        robot.mov_path_between_location_and_destination = None
        return None # we have reached to battle front, don't move
    else:
        # robot.log("Inside else")
        ans = movement.move_to_destination(robot)
        robot.log("Return value: " + str(ans))
        return ans

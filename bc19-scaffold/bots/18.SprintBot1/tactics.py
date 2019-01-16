# General tactics for all units
import utility
import movement
import pathfinding
import constants


def prophet_will_combat_1vs1(robot, enemy):
    passable_map = robot.get_passable_map()
    if enemy['unit'] == constants.unit_prophet:
        if robot.me.health == constants.prophet_max_health:
            robot.is_targeting_robot_with_id = enemy['id']
            return enemy
        elif robot.me.health < constants.prophet_max_health:
            if enemy['id'] == robot.is_targeting_robot_with_id:
                robot.is_targeting_robot_with_id = enemy['id']
                return enemy
            else:
                new_pos_x = 0
                new_pos_y = 0
                
                # Can move out of bot vision
                max_distance = constants.prophet_max_attack_range
                for directions in constants.non_crusader_move_directions:
                    guessing_new_pos_x = robot.me.x + directions[0]
                    guessing_new_pos_y = robot.me.y + directions[1]
                    guessing_distance = (guessing_new_pos_x - enemy['x'])**2 + (guessing_new_pos_y- enemy['y'])**2
                    if guessing_distance > max_distance and not utility.is_cell_occupied(passable_map, guessing_new_pos_x, guessing_new_pos_y):
                        guessing_distance = max_distance
                        new_pos_x = guessing_new_pos_x
                        new_pos_y = guessing_new_pos_y
                if max_distance > constants.prophet_max_attack_range:
                    return robot.move(new_pos_x - robot.me.x, new_pos_y - robot.me.y)

                # Can move into non-attack region
                min_distance = constants.prophet_min_attack_range
                for directions in constants.non_crusader_move_directions:
                    guessing_new_pos_x = robot.me.x + directions[0]
                    guessing_new_pos_y = robot.me.y + directions[1]
                    guessing_distance = (guessing_new_pos_x - enemy['x'])**2 + (guessing_new_pos_y- enemy['y'])**2
                    
                    if guessing_distance < min_distance and not utility.is_cell_occupied(passable_map, guessing_new_pos_x, guessing_new_pos_y):
                        guessing_distance = min_distance
                        new_pos_x = guessing_new_pos_x
                        new_pos_y = guessing_new_pos_y
                if min_distance < constants.prophet_min_attack_range:
                    return robot.move()

            # robot.is_targeting_robot_with_id = enemy['id']

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
        # robot.log("Inside if")
        robot.current_move_destination = None
        robot.mov_path_between_location_and_destination = None
        return None # we have reached to battle front, don't move
    else:
        # robot.log("Inside else")
        ans = movement.move_to_destination(robot)
        # robot.log("Return value: " + str(ans))
        return ans

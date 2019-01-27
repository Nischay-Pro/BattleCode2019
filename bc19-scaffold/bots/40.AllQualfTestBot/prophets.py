import check
import combat_module
import movement
import pathfinding
import prophet_utility
import tactics
import utility

def prophet(robot):
    if robot.step == 0:
        prophet_utility.receive_initial_signal(robot)

    prophet_attack_aggr_mode = combat_module.give_military_command(robot)
    if prophet_attack_aggr_mode != None:
        return prophet_attack_aggr_mode

    move_check = 0

    if robot.step > 40 and robot.step < 50:
        move_check = prophet_move(robot)

    if move_check != 0 and move_check != None:
        return move_check

    if robot.step > 10:
        give_direction = utility.give_to_adjacent_robot(robot)
        if give_direction != None:
            carry_karb = robot.me.karbonite
            carry_fuel = robot.me.fuel
            return robot.give(give_direction[0], give_direction[1], carry_karb, carry_fuel)

    return None

def prophet_move(robot):

    # prophet_utility.did_prophet_burn_out(robot)

    # if robot.step > 300:
    #     march_increment = (robot.step - 200) // 100

    if robot.current_move_destination != None and not movement.is_completely_surrounded(robot): #and tactics.should_combat_unit_be_at_battle_front(robot):
        destination = robot.current_move_destination
        move_dir = pathfinding.bug_walk_toward(robot, destination)
        return check.move_check(robot, move_dir[0], move_dir[1], 45)
    return 0

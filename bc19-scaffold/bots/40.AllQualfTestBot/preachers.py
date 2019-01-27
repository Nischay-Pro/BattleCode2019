import combat_module
import preachers_utility

def preacher(robot):
    if robot.step == 0:
        preachers_utility.receive_initial_signal(robot)

    preachers_utility.combat_channel(robot)
    crusader_attack_aggr_mode = combat_module.give_military_command(robot)
    if crusader_attack_aggr_mode != None:
        return crusader_attack_aggr_mode

    move_check = preachers_utility.preachers_move(robot)

    if move_check != 0:
        return move_check

    if robot.step > 10:
        give_direction = utility.give_to_adjacent_robot(robot)
        if give_direction != None:
            carry_karb = robot.me.karbonite
            carry_fuel = robot.me.fuel
            return robot.give(give_direction[0], give_direction[1], carry_karb, carry_fuel)

    return None

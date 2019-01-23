import combat_module
import crusaders_utility

def crusader(robot):
    if robot.step == 0:
        crusaders_utility.receive_initial_signal(robot)

    crusader_attack_aggr_mode = combat_module.give_military_command(robot)
    if crusader_attack_aggr_mode != None:
        return crusader_attack_aggr_mode
    return crusaders_utility.crusader_move(robot)

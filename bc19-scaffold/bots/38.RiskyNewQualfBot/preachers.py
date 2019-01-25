import combat_module
import preachers_utility

def preacher(robot):
    if robot.step == 0:
        preachers_utility.receive_initial_signal(robot)

    preachers_utility.combat_channel(robot)
    crusader_attack_aggr_mode = combat_module.give_military_command(robot)
    if crusader_attack_aggr_mode != None:
        return crusader_attack_aggr_mode
    return preachers_utility.preachers_move(robot)

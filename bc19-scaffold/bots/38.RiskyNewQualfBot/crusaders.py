import combat_module
import crusaders_utility

def crusader(robot):
    if robot.step == 0:
        crusaders_utility.receive_initial_signal(robot)

    crusaders_utility.combat_channel(robot)
    # if robot.core_is_ready == 1:
    #     robot.log("C1 " + str(robot.current_move_destination))
    crusader_attack_aggr_mode = combat_module.give_military_command(robot)
    if crusader_attack_aggr_mode != None:
        return crusader_attack_aggr_mode
    # if robot.core_is_ready == 1:
    #     robot.log("C1 " + str(robot.current_move_destination))
    return crusaders_utility.crusader_move(robot)

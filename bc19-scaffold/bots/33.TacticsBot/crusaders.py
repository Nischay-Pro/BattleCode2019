import combat_module
import crusaders_utility

def crusader(robot):
    if robot.step == 0:
        crusaders_utility.receive_initial_signal(robot)

    # robot.log("Check1 " + str(robot.current_move_destination) + " " + str(robot.following_crusader_command))
    crusaders_utility.combat_channel(robot)
    # robot.log("Check2 " + str(robot.current_move_destination) + " " + str(robot.following_crusader_command))
    crusader_attack_aggr_mode = combat_module.give_military_command(robot)
    if crusader_attack_aggr_mode != None:
        return crusader_attack_aggr_mode
    # robot.log("Check3 " + str(robot.current_move_destination) + " " + str(robot.following_crusader_command))
    return crusaders_utility.crusader_move(robot)

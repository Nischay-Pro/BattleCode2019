import combat_module
import movement
import prophet_utility
import tactics

def prophet(robot):
    if robot.step == 0:
        prophet_utility.receive_initial_signal(robot)

    prophet_attack_aggr_mode = combat_module.give_military_command(robot)
    if prophet_attack_aggr_mode != None:
        return prophet_attack_aggr_mode

    return prophet_move(robot)

def prophet_move(robot):

    # prophet_utility.did_prophet_burn_out(robot)

    # if robot.step > 300:
    #     march_increment = (robot.step - 200) // 100

    if robot.current_move_destination != None and not movement.is_completely_surrounded(robot): #and tactics.should_combat_unit_be_at_battle_front(robot):
        return tactics.send_combat_unit_to_battle_front(robot, 0.5, 0.08)
    return 0

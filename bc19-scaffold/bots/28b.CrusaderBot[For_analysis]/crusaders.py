import combat_module
import movement
import tactics

def crusader(robot):
    prophet_attack_aggr_mode = combat_module.give_military_command(robot)
    if prophet_attack_aggr_mode != None:
        return prophet_attack_aggr_mode

    return crusader_move(robot)

def crusader_move(robot):
    if robot.current_move_destination != None and not movement.is_completely_surrounded(robot): #and tactics.should_combat_unit_be_at_battle_front(robot):
        return tactics.send_combat_unit_to_battle_front(robot, 0.35, 0.15)
    return 0

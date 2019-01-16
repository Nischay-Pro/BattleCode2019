import combat_module
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
    
    prophet_utility.did_prophet_burn_out(robot)

    if robot.step > 300:
        march_increment = (robot.step - 200) // 100

    if robot.current_move_destination != None: #and tactics.should_combat_unit_be_at_battle_front(robot):
        return tactics.send_combat_unit_to_battle_front(robot, 0.5 + march_increment/10 , 0.08)
    return 0
    #  for direction in directions:
        #  if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            #  return robot.move(direction[1], direction[0])
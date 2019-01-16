import utility
import vision
import mapping
import movement
import constants
import combat_module
import tactics

def prophet(robot):

    if robot.step == 0:
        unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
        for friendly_unit in friendly_units:
            if friendly_unit.unit == 0 and friendly_unit.signal > 0:
                robot.built_by_a_castle = 1
                robot.built_by_a_church = 0
                _prophet_initial_check(robot, friendly_unit)
                break
    prophet_attack_aggr_mode = combat_module.give_military_command(robot)
    
    if prophet_attack_aggr_mode != None:
        return prophet_attack_aggr_mode
    
    return prophet_move(robot)

def prophet_move(robot):
    
    if robot.burned_out > 2:
        robot.current_move_destination = None
    
    if movement.is_completely_surrounded(robot):
        robot.attained_nirvana_on_turn = robot.step
        robot.burned_out += 1
        # robot.log("Completely surrounded pilgrim or attained Nirvana")
        return 0
    elif robot.attained_nirvana_on_turn + constants.pilgrim_nirvana_age > robot.step:
        return 0
    else:
        robot.attained_nirvana_on_turn = -1

    if utility.fuel_less_check(robot):
        return None

    if robot.current_move_destination != None: #and tactics.should_combat_unit_be_at_battle_front(robot):
        return tactics.send_combat_unit_to_battle_front(robot, 0.5, 0.08)
    return 0
    #  for direction in directions:
        #  if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            #  return robot.move(direction[1], direction[0])

def _prophet_initial_check(robot, friendly_unit):
    robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
    if robot.built_by_a_castle == 1:
        robot.friendly_castles.append(robot.our_castle_or_church_base)
    else:
        robot.friendly_churches.append(robot.our_castle_or_church_base)
    
    if robot.prophet_health == None:
        robot.prophet_health = constants.prophet_max_health

    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    if len(robot.enemy_castles) == 0 and robot.built_by_a_castle == 1:
        robot.enemy_castles.append(mapping.find_symmetrical_point(robot, friendly_unit['x'], friendly_unit['y'], robot.map_symmetry))
        robot.current_move_destination = robot.enemy_castles[0]
    

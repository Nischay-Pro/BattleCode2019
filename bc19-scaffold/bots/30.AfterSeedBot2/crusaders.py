import communications
import combat_module
import constants
import mapping
import movement
import tactics
import vision

def crusader(robot):
    if robot.step == 0:
        receive_initial_signal(robot)


    crusader_attack_aggr_mode = combat_module.give_military_command(robot)
    if crusader_attack_aggr_mode != None:
        return crusader_attack_aggr_mode

    return crusader_move(robot)

def crusader_move(robot):
    if robot.current_move_destination != None and not movement.is_completely_surrounded(robot): #and tactics.should_combat_unit_be_at_battle_front(robot):
        return tactics.send_combat_unit_to_battle_front(robot, 0.55, 0.15)
    return 0

def combat_channel(robot):
    unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
    for friendly_unit in friendly_units:
        if friendly_unit.unit == 3 and friendly_unit.signal > 0:
            robot.current_move_destination = communications.decode_msg_without_direction(friendly_unit.signal)

def receive_initial_signal(robot):
    unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
    for friendly_unit in friendly_units:
        if friendly_unit.unit == 0 and friendly_unit.signal > 0:
            robot.built_by_a_castle = 1
            robot.built_by_a_church = 0
            _crusader_initial_check(robot, friendly_unit)
        elif friendly_unit.unit == 1 and friendly_unit.signal > 0:
            robot.built_by_a_castle = 0
            robot.built_by_a_church = 1
            _crusader_initial_check(robot, friendly_unit)

def _crusader_initial_check(robot, friendly_unit):

    if robot.built_by_a_castle == 1:
        robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
        robot.friendly_castles.append(robot.our_castle_or_church_base)
    else:
        robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
        robot.friendly_churches.append(robot.our_castle_or_church_base)

    if robot.crusader_health == None:
        robot.crusader_health = constants.crusader_max_health

    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    if len(robot.enemy_castles) == 0 and robot.built_by_a_castle == 1:
        robot.enemy_castles.append(mapping.find_symmetrical_point(robot, friendly_unit['x'], friendly_unit['y'], robot.map_symmetry))

    robot.current_move_destination = mapping.find_symmetrical_point(robot, robot.our_castle_or_church_base[0], robot.our_castle_or_church_base[1], robot.map_symmetry)

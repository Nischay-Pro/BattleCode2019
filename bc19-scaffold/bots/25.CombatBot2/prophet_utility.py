import constants
import mapping
import movement
import utility
import vision

def receive_initial_signal(robot):
    unused_store, friendly_units = vision.sort_visible_friendlies_by_distance(robot)
    for friendly_unit in friendly_units:
        if friendly_unit.unit == 0 and friendly_unit.signal > 0:
            robot.built_by_a_castle = 1
            robot.built_by_a_church = 0
            _prophet_initial_check(robot, friendly_unit)
        elif friendly_unit.unit == 1 and friendly_unit.signal > 0:
            robot.built_by_a_castle = 0
            robot.built_by_a_church = 1
            _prophet_initial_check(robot, friendly_unit)
            break

def did_prophet_burn_out(robot):
    # Can't move around, don't do astar
    if movement.is_completely_surrounded(robot):
        robot.burned_out = 1

    if robot.burned_out == 1:
        if robot.burned_out_on_turn == -1:
            robot.burned_out_on_turn = 0
        elif robot.burned_out_on_turn == 0:
            robot.burned_out_on_turn = robot.step
        robot.burned_out = 0
    elif robot.burned_out_on_turn + constants.prophet_burnout_period <= robot.step:
        robot.burned_out_on_turn = -1

def _prophet_initial_check(robot, friendly_unit):

    if robot.built_by_a_castle == 1:
        robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
        robot.friendly_castles.append(robot.our_castle_or_church_base)
    else:
        robot.our_castle_or_church_base = (friendly_unit['x'], friendly_unit['y'])
        robot.friendly_churches.append(robot.our_castle_or_church_base)

    if robot.prophet_health == None:
        robot.prophet_health = constants.prophet_max_health

    if robot.map_symmetry == None:
        mapping.return_map_symmetry(robot)

    if len(robot.enemy_castles) == 0 and robot.built_by_a_castle == 1:
        robot.enemy_castles.append(mapping.find_symmetrical_point(robot, friendly_unit['x'], friendly_unit['y'], robot.map_symmetry))

    robot.current_move_destination = mapping.find_symmetrical_point(robot, robot.our_castle_or_church_base[0], robot.our_castle_or_church_base[1], robot.map_symmetry)

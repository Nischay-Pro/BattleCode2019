import utility
import check
import mapping
import constants
import communications

def castle_all_friendly_units(robot):
    all_units = robot.get_visible_robots()

    friendly_units = []
    enemy_units = []
    for unit in all_units:
        if unit.team == None:
            friendly_units.append(unit)
        elif robot.me.team == unit.team:
            friendly_units.append(unit)
        else:
            enemy_units.append(unit)

    return friendly_units, enemy_units

def castle_all_friendly_units_but_not_me(robot):
    all_units = robot.get_visible_robots()

    friendly_units = []
    enemy_units = []
    for unit in all_units:
        if unit.team == None and robot.me['id'] != unit['id']:
            friendly_units.append(unit)
        elif robot.me.team == unit.team and robot.me['id'] != unit['id']:
            friendly_units.append(unit)
        else:
            enemy_units.append(unit)

    return friendly_units, enemy_units

def _is_castle_under_attack(robot, enemy_units):
    if robot.me.health < robot.castle_health:
        robot.castle_health = robot.me.health
        robot.castle_under_attack = 1
        robot.castle_under_attack_turn = robot.step
    elif robot.castle_under_attack and robot.castle_under_attack_turn + 5 < robot.step and len(enemy_units) == 0:
        # No longer under attack
        robot.castle_under_attack = 0

def _castle_build(robot, unit_type):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    directions = constants.directions

    res_list = []
    res_max = (0, 0, 0)

    for direction in directions:
        if utility.is_cell_occupiable_and_resourceless(occupied_map, passable_map, karb_map, fuel_map, pos_x + direction[0],  pos_y + direction[1]) and passable_map[pos_y + direction[1]][pos_x + direction[0]] == 1:
            res_list.append((direction[0], direction[1], mapping.get_map_ratio(pos_x + direction[0],  pos_y + direction[1], passable_map, 1)))

    if len(res_list) == 0:
        for direction in directions:
            if not utility.is_cell_occupied(occupied_map, pos_x + direction[0],  pos_y + direction[1]) and passable_map[pos_y + direction[1]][pos_x + direction[0]] == 1:
                res_list.append((direction[0], direction[1], mapping.get_map_ratio(pos_x + direction[0],  pos_y + direction[1], passable_map, 1)))
    # robot.log("No space to build units anymore for castles")

    for res in res_list:
        if res[2] > res_max[2]:
            res_max = res

    if not (res_max[0] == 0 and res_max[1] == 0):
        # robot.log("Building unit of type " + str(unit_type) + " at " + str(res_max))
        # TRAVIS BUILD CHECK 1
        return check.build_check(robot, unit_type, res_max[0], res_max[1], 1)

    robot.log("Castle surrounded, no space to build.")
    return None

def _castle_assign_mine_or_scout(robot):
    # TODO - Change as per our requirements of fuel or karbonite
    # TODO - Change occupancy to robot id when reached mine
    # TODO - Add scouts
    # Build a karb mine
    karb_mine_assigned = -1
    fuel_mine_assigned = -1

    for iter_i in range(len(robot.karb_mine_occupancy_from_this_castle)):
        if robot.karb_mine_occupancy_from_this_castle[iter_i] == -1:
            karb_mine_assigned = iter_i
            break

    for iter_j in range(len(robot.fuel_mine_occupancy_from_this_castle)):
        if robot.fuel_mine_occupancy_from_this_castle[iter_j] == -1:
            fuel_mine_assigned = iter_j
            break

    if (robot.pilgrim_build_number % 2 == 1 or fuel_mine_assigned == -1) and karb_mine_assigned != -1:
        robot.karb_mine_occupancy_from_this_castle[karb_mine_assigned] = 0
        mine_pos = robot.karb_mine_locations_from_this_castle[karb_mine_assigned]
        comms = communications.encode_msg_without_direction(mine_pos[0], mine_pos[1])
        return comms
    # Build a fuel mine
    elif (robot.pilgrim_build_number % 2 == 0 or karb_mine_assigned == -1) and fuel_mine_assigned !=-1:
        robot.fuel_mine_occupancy_from_this_castle[fuel_mine_assigned] = 0
        mine_pos = robot.fuel_mine_locations_from_this_castle[fuel_mine_assigned]
        comms = communications.encode_msg_without_direction(mine_pos[0], mine_pos[1])
        return comms

    return 0

def get_enemy_castles(robot):
    my_castles = robot.friendly_castles
    for i in range(len(my_castles)):
        current_castle = mapping.find_symmetrical_point(robot, my_castles[i][0], my_castles[i][1], robot.map_symmetry)
        robot.enemy_castles.append(current_castle)

def _check_if_piligrim_spoke_with_me_already(robot, id):
    keys_to_check = list(robot.co_ordinate_storage_locker.keys())
    if len(keys_to_check) > 0:
        for i in range(len(keys_to_check)):
            if keys_to_check[i] == id:
                return True
        return None
    else:
        return None
    return None
    # for i in range(len())

def _check_if_co_ordinate_exists_in_karb_manager(robot, with_what, also_who):
    keys_to_check = list(robot.karb_manager.keys())
    for i in range(len(keys_to_check)):
        if keys_to_check[i] == with_what:
            robot.karb_manager[with_what] = [also_who, True]
            return True
    return False

def _check_if_co_ordinate_exists_in_fuel_manager(robot, with_what, also_who):
    keys_to_check = list(robot.fuel_manager.keys())
    for i in range(len(keys_to_check)):
        if keys_to_check[i] == with_what:
            robot.fuel_manager[with_what] = [also_who, True]
            return True
    return False

def _castle_mine_and_karb_processor(robot):
    visible_robots,_ = castle_all_friendly_units_but_not_me(robot)
    if len(visible_robots) != 0:
        for i in range(len(visible_robots)):
            current_unit = visible_robots[i]
            if current_unit['signal'] == -1:
                # Don't put the conditions as AND. Consult Nischay for info on why
                if current_unit['castle_talk'] >= 64:
                    what_say_you = current_unit['castle_talk']
                    response = _check_if_piligrim_spoke_with_me_already(robot, current_unit['id'])
                    if response == True:
                        # Yeah. So you spoke to me, let me fetch your x coord from storage locker and check against the managers.
                        piligrim_x_cord = robot.co_ordinate_storage_locker[current_unit['id']][0]
                        piligrim_y_cord = what_say_you - 64
                        robot.co_ordinate_storage_locker[current_unit['id']].append(piligrim_y_cord)
                        if _check_if_co_ordinate_exists_in_karb_manager(robot, (piligrim_x_cord, piligrim_y_cord), current_unit['id']):
                            None
                            # mi casa es su casa
                        elif _check_if_co_ordinate_exists_in_fuel_manager(robot, (piligrim_x_cord, piligrim_y_cord), current_unit['id']):
                            # mi casa es su casa
                            None
                        else:
                            robot.log("This shouldn't have happened")

                    else:
                        # My man you did not speak to me so I guess you are shouting the x coords. I shall handle them gladly.
                        robot.co_ordinate_storage_locker[current_unit['id']] = [what_say_you - 64]



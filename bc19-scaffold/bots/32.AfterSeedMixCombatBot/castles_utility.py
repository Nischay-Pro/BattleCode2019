import utility
import check
import mapping
import constants
import communications
import vision

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
    # Build a karb mine
    karb_mine_assigned = -1
    fuel_mine_assigned = -1

    for iter_i in range(len(robot.karb_mine_occupancy_from_this_castle)):
        if robot.karb_mine_occupancy_from_this_castle[iter_i] == -1:
            if am_i_the_nearest_castle_to_this(robot, robot.karb_mine_locations_from_this_castle[iter_i][0], robot.karb_mine_locations_from_this_castle[iter_i][1]):
                karb_mine_assigned = iter_i
                break
            else:
                robot.karb_mine_occupancy_from_this_castle[iter_i] = 0

    for iter_j in range(len(robot.fuel_mine_occupancy_from_this_castle)):
        if robot.fuel_mine_occupancy_from_this_castle[iter_j] == -1:
            if am_i_the_nearest_castle_to_this(robot, robot.fuel_mine_locations_from_this_castle[iter_j][0], robot.fuel_mine_locations_from_this_castle[iter_j][1]):
                fuel_mine_assigned = iter_j
                break
            else:
                robot.karb_mine_occupancy_from_this_castle[iter_i] = 0

    if (robot.pilgrim_build_number % 2 == 1 or fuel_mine_assigned == -1) and karb_mine_assigned != -1:
        robot.karb_mine_occupancy_from_this_castle[karb_mine_assigned] = 0
        mine_pos = robot.karb_mine_locations_from_this_castle[karb_mine_assigned]
        _update_karb_mine_pilgrim_assignment(robot, mine_pos)
        comms = communications.encode_msg_without_direction(mine_pos[0], mine_pos[1])
        return comms
    # Build a fuel mine
    elif (robot.pilgrim_build_number % 2 == 0 or karb_mine_assigned == -1) and fuel_mine_assigned !=-1:
        robot.fuel_mine_occupancy_from_this_castle[fuel_mine_assigned] = 0
        mine_pos = robot.fuel_mine_locations_from_this_castle[fuel_mine_assigned]
        _update_fuel_mine_pilgrim_assignment(robot, mine_pos)
        comms = communications.encode_msg_without_direction(mine_pos[0], mine_pos[1])
        return comms

    # robot.log(robot.fuel_mine_occupancy_from_this_castle)
    # robot.log(robot.karb_mine_occupancy_from_this_castle)
    return 0

def _allot_enemy_mine(robot):
    return True


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
                if robot.co_ordinate_storage_locker[id][0] != -1 and robot.co_ordinate_storage_locker[id][1] != -1:
                    return True
                return None
        return None
    else:
        return None
    return None
    # for i in range(len())

def _check_if_co_ordinate_exists_in_karb_manager(robot, with_what, also_who):
    keys_to_check = list(robot.karb_manager.keys())
    for i in range(len(keys_to_check)):
        if keys_to_check[i] == with_what:
            robot.karb_manager[with_what] = [also_who, True, True]
            return True
    return False

def _check_if_co_ordinate_exists_in_fuel_manager(robot, with_what, also_who):
    keys_to_check = list(robot.fuel_manager.keys())
    for i in range(len(keys_to_check)):
        if keys_to_check[i] == with_what:
            robot.fuel_manager[with_what] = [also_who, True, True]
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
                            if piligrim_x_cord == piligrim_y_cord:
                                _pilgrim_warned(robot, current_unit['id'])
                            else:
                                robot.log("This shouldn't have happened")

                    else:
                        # My man you did not speak to me so I guess you are shouting the x coords. I shall handle them gladly.
                        robot.co_ordinate_storage_locker[current_unit['id']] = [what_say_you - 64]

def _get_controlled_karb_mines(robot):
    karbs = robot.karb_manager
    keys_to_check = list(robot.karb_manager.keys())
    mines = []
    if len(karbs) > 0:
        for i in range(len(robot.karb_manager)):
            data = karbs[keys_to_check[i]]
            if data[0] != 0 and data[1] == True and data[2] == True:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_controlled_fuel_mines(robot):
    fuels = robot.fuel_manager
    keys_to_check = list(robot.fuel_manager.keys())
    mines = []
    if len(fuels) > 0:
        for i in range(len(robot.fuel_manager)):
            data = fuels[keys_to_check[i]]
            if data[0] != 0 and data[1] == True and data[2] == True:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_closest_fuel_mine_never_sent(robot):
    mines = _get_free_fuel_mines_never_sent(robot)
    if len(mines) > 0:
        temp, mines = utility.get_sorted_list_from_a_point(robot.me['x'], robot.me['y'], mines)
        for i in range(len(mines)):
            if am_i_the_nearest_castle_to_this(robot, mines[i][0], mines[i][1]):
                return mines[i]
        return None
    else:
        return None

def _update_fuel_mine_pilgrim_assignment(robot, fuel_mine):
    fuel_keys = list(robot.fuel_manager.keys())
    for i in range(len(fuel_keys)):
        if str(fuel_keys[i]) == str(fuel_mine[0]) + "," + str(fuel_mine[1]):
            robot.fuel_manager[fuel_keys[i]][1] = True
            robot.fuel_manager[fuel_keys[i]][2] = True
            break    

def _get_free_fuel_mines_never_sent(robot):
    fuels = robot.fuel_manager
    keys_to_check = list(robot.fuel_manager.keys())
    mines = []
    if len(fuels) > 0:
        for i in range(len(robot.fuel_manager)):
            data = fuels[keys_to_check[i]]
            if data[0] == 0 and data[1] == False and data[2] == False:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_closest_karb_mine_never_sent(robot):
    mines = _get_free_karb_mines_never_sent(robot)
    if len(mines) > 0:
        temp, mines = utility.get_sorted_list_from_a_point(robot.me['x'], robot.me['y'], mines)
        for i in range(len(mines)):
            if am_i_the_nearest_castle_to_this(robot, mines[i][0], mines[i][1]):
                return mines[i]
        return None
    else:
        return None

def _update_karb_mine_pilgrim_assignment(robot, karb_mine):
    karb_keys = list(robot.karb_manager.keys())
    for i in range(len(karb_keys)):
        if str(karb_keys[i]) == str(karb_mine[0]) + "," + str(karb_mine[1]):
            robot.karb_manager[karb_keys[i]][1] = True
            robot.karb_manager[karb_keys[i]][2] = True
            break        

def _get_free_karb_mines_never_sent(robot):
    karbs = robot.karb_manager
    keys_to_check = list(robot.karb_manager.keys())
    mines = []
    if len(karbs) > 0:
        for i in range(len(robot.karb_manager)):
            data = karbs[keys_to_check[i]]
            if data[0] == 0 and data[1] == False and data[2] == False:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_free_fuel_mines_never_sent(robot):
    fuels = robot.fuel_manager
    keys_to_check = list(robot.fuel_manager.keys())
    mines = []
    if len(fuels) > 0:
        for i in range(len(robot.fuel_manager)):
            data = fuels[keys_to_check[i]]
            if data[0] == 0 and data[1] == False and data[2] == False:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_free_karb_mines_now_unsafe(robot):
    karbs = robot.karb_manager
    keys_to_check = list(robot.karb_manager.keys())
    mines = []
    if len(karbs) > 0:
        for i in range(len(robot.karb_manager)):
            data = karbs[keys_to_check[i]]
            if data[0] == 0 and data[1] == True and data[2] == False:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_free_fuel_mines_now_unsafe(robot):
    fuels = robot.fuel_manager
    keys_to_check = list(robot.fuel_manager.keys())
    mines = []
    if len(fuels) > 0:
        for i in range(len(robot.fuel_manager)):
            data = fuels[keys_to_check[i]]
            if data[0] == 0 and data[1] == True and data[2] == False:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _get_unoccupied_fuel_in_general(robot):
    fuels = robot.fuel_manager
    keys_to_check = list(robot.fuel_manager.keys())
    mines = []
    if len(fuels) > 0:
        for i in range(len(robot.fuel_manager)):
            data = fuels[keys_to_check[i]]
            if data[0] == 0 and data[1] == False and data[2] == False:
                mines.append((int(keys_to_check[i].split(",")[0]), int(keys_to_check[i].split(",")[1])))
    return mines

def _is_fuel_mine_occupied_or_allocated(robot, cord_x, cord_y):
    fuel = robot.fuel_manager
    fuel_keys = list(fuel.keys())
    cord_comb = str(cord_x) + "," + str(cord_y)
    for i in range(len(fuel_keys)):
        if str(fuel_keys[i]) == cord_comb:
            selected_fuel = fuel[fuel_keys[i]]
            if selected_fuel[0] == 0 and selected_fuel[1] == False and selected_fuel[2] == False:
                return False
            else:
                return True
            break

def _get_closest_our_side_unoccupied_fuel_mine(robot):
    our_side_fuel_mines = mapping.get_friendly_fuel(robot)
    temp, our_side_fuel_mines = utility.get_sorted_list_from_a_point(robot.me['x'], robot.me['y'], our_side_fuel_mines)
    for i in range(len(our_side_fuel_mines)):
        if (not _is_fuel_mine_occupied_or_allocated(robot, our_side_fuel_mines[i][0], our_side_fuel_mines[i][1])) and am_i_the_nearest_castle_to_this(robot, our_side_fuel_mines[i][0], our_side_fuel_mines[i][1]):
            return our_side_fuel_mines[i]
    return None

def _is_karb_mine_occupied_or_allocated(robot, cord_x, cord_y):
    karbs = robot.karb_manager
    karb_keys = list(karbs.keys()) 
    cord_comb = str(cord_x) + "," + str(cord_y)
    for i in range(len(karb_keys)):
        if str(karb_keys[i]) == cord_comb:
            selected_karb = karbs[karb_keys[i]]
            if selected_karb[0] == 0 and selected_karb[1] == False and selected_karb[2] == False:
                return False
            else:
                return True
            break

def _get_closest_our_side_unoccupied_karb_mine(robot):
    our_side_karb_mines = mapping.get_friendly_karbonite(robot)
    temp, our_side_karb_mines = utility.get_sorted_list_from_a_point(robot.me['x'], robot.me['y'], our_side_karb_mines)
    if len(our_side_karb_mines) > 0:
        for i in range(len(our_side_karb_mines)):
           if (not _is_karb_mine_occupied_or_allocated(robot, our_side_karb_mines[i][0], our_side_karb_mines[i][1])) and am_i_the_nearest_castle_to_this(robot, our_side_karb_mines[i][0], our_side_karb_mines[i][1]):
                return our_side_karb_mines[i]
        return None
    return None


def _castle_attack_when_attack_range(robot):
    enemies_dist, enemies = vision.sort_visible_enemies_by_distance(robot)
    if len(enemies_dist) > 0:
        distance = enemies_dist[0]
        my_enemy = enemies[0]
        if distance <= constants.castle_max_attack_range and distance >= constants.castle_min_attack_range:
            # TRAVIS ATTACK CHECK 9
            return check.attack_check(robot, my_enemy['x'] - robot.me['x'], my_enemy['y'] - robot.me['y'], 9)
    return None

def am_i_the_nearest_castle_to_this(robot, xcord, ycord):
    castle_list = robot.friendly_castles
    if len(castle_list) > 0:
        am_i_the_closest = True
        my_x = robot.me['x']
        my_y = robot.me['y']
        how_far_is_it_from_me = ((my_x - xcord) ** 2) + ((my_y - ycord) ** 2)
        for i in range(len(castle_list)):
            castle_x = castle_list[i][0]
            castle_y = castle_list[i][1]
            how_far_is_it_from_other = ((castle_x - xcord) ** 2) + ((castle_y - ycord) ** 2)
            if how_far_is_it_from_other < how_far_is_it_from_me:
                am_i_the_closest = False
        return am_i_the_closest
    else:
        # This shouldn't have happened
        robot.log("This shouldn't have happened")

def nicely_push_into_storage_lockers(robot, value_to_push, locker):
    if locker == 1:
        # Karb Locker
        if len(robot.karb_resource_locker) == constants.resource_locker_capacity:
            robot.karb_resource_locker.pop(0)
            robot.karb_resource_locker.append(value_to_push)
        else:
            robot.karb_resource_locker.append(value_to_push)
    elif locker == 2:
        # Fuel Locker
        if len(robot.fuel_resource_locker) == constants.resource_locker_capacity:
            robot.fuel_resource_locker.pop(0)
            robot.fuel_resource_locker.append(value_to_push)
        else:
            robot.fuel_resource_locker.append(value_to_push)
    elif locker == 3:
        # Enemy Locker
        if len(robot.enemy_unit_locker) == constants.enemy_locker_capacity:
            robot.enemy_unit_locker.pop(0)
            robot.enemy_unit_locker.append(value_to_push)
        else:
            robot.enemy_unit_locker.append(value_to_push)
    elif locker == 4:
        # Pilgrim Locker
        if len(robot.pilgrim_unit_history) == constants.unit_locker_capacity:
            robot.pilgrim_unit_history.pop(0)
            robot.pilgrim_unit_history.append(value_to_push)
        else:
            robot.pilgrim_unit_history.append(value_to_push)
    elif locker == 5:
        # Crusader Locker
        if len(robot.crusader_unit_history) == constants.unit_locker_capacity:
            robot.crusader_unit_history.pop(0)
            robot.crusader_unit_history.append(value_to_push)
        else:
            robot.crusader_unit_history.append(value_to_push)
    elif locker == 6:
        # Prophet Locker
        if len(robot.prophet_unit_history) == constants.unit_locker_capacity:
            robot.prophet_unit_history.pop(0)
            robot.prophet_unit_history.append(value_to_push)
        else:
            robot.prophet_unit_history.append(value_to_push)
    elif locker == 7:
        # Preacher Locker
        if len(robot.preacher_unit_history) == constants.unit_locker_capacity:
            robot.preacher_unit_history.pop(0)
            robot.preacher_unit_history.append(value_to_push)
        else:
            robot.preacher_unit_history.append(value_to_push)


def get_percent_karbs_controlled(robot):
    controlled = len(_get_controlled_karb_mines(robot))
    available = vision.all_karbonite(robot)
    return (controlled / available)

def get_percent_fuel_controlled(robot):
    controlled = len(_get_controlled_fuel_mines(robot))
    available = vision.all_fuel(robot)
    return (controlled / available)

def did_we_max_out_initial_karb_sending(robot):
    #FIXME Switch to Karb Manager
    check_this = robot.karb_mine_occupancy_from_this_castle
    counter = 0
    for i in range(check_this):
        if check_this[i] == 0:
            counter += 1
    if counter == len(check_this):
        return True
    else:
        return False

def did_we_max_out_initial_fuel_sending(robot):
    #FIXME Switch to Fuel Manager
    check_this = robot.fuel_mine_occupancy_from_this_castle
    counter = 0
    for i in range(check_this):
        if check_this[i] == 0:
            counter += 1
    if counter == len(check_this):
        return True
    else:
        return False

def are_we_greater_than_average(locker):
    total = 0
    for i in range(len(locker)):
        total += locker[i]
    total = total / len(locker)
    if total > locker[len(locker) - 1]:
        return False
    else:
        return True

def dist_between(x1, x2, y1, y2):
    return ((x1 - x2) ** 2) + ((y1 - y2) ** 2)

def get_the_furthest_mine_from_list(robot, available_list):
    enemy_location = robot.enemy_castles
    farthest_dist = 0
    selected_itm = []
    if len(available_list) != 0:
        for i in range(len(available_list)):
            for j in range(len(enemy_location)):
                dist = dist_between(enemy_location[j][0], available_list[i][0], enemy_location[j][1], available_list[i][1])
                if farthest_dist < dist:
                    farthest_dist = dist
                    selected_itm = enemy_location[j]
        return selected_itm
    else:
        return None

def _castle_monitor_mode(robot):
    if robot.enemy_unit_locker_turn == constants.enemy_locker_capacity:
        robot.enemy_unit_locker = []
        enemy_unit_locker_turn = 0
    visible = robot.get_visible_robots()
    for i in range(len(visible)):
        if visible[i]['team'] != robot.me['team']:
            unit_type = visible[i]['unit']
            if unit_type == 0:
                unit_type == constants.unit_castle
            elif unit_type == 1:
                unit_type == constants.unit_church
            elif unit_type == 2:
                unit_type = constants.unit_pilgrim
            elif unit_type == 3:
                unit_type == constants.unit_crusader
            elif unit_type == 4:
                unit_type == constants.unit_prophet
            elif unit_type == 5:
                unit_type == constants.unit_preacher
            robot.enemy_unit_locker.append(unit_type)
    enemy_unit_locker_turn += 1

def can_build_pilgrim(robot):
    if robot.karbonite >= 15 and robot.fuel >= 50:
        return True
    else: 
        return False

def _pilgrim_warned(robot, id):
    keys_to_check = list(robot.co_ordinate_storage_locker.keys())
    if len(keys_to_check) > 0:
        for i in range(len(keys_to_check)):
            if keys_to_check[i] == id:
                robot.co_ordinate_storage_locker[keys_to_check[i]] = [-1, -1]
    fuel = robot.fuel_manager
    karb = robot.karb_manager
    fuel_keys = list(fuel.keys())
    karb_keys = list(karb.keys())
    for i in range(len(fuel_keys)):
        if fuel[fuel_keys[i]][0] == id:
            robot.log(robot.fuel_manager[fuel_keys[i]])
            robot.fuel_manager[fuel_keys[i]][0] = 0
            robot.fuel_manager[fuel_keys[i]][2] = False
            robot.log(robot.fuel_manager[fuel_keys[i]])
            return None
    for i in range(len(karb_keys)):
        if karb[karb_keys[i]][0] == id:
            robot.karb_manager[karb_keys[i]][0] = 0
            robot.karb_manager[karb_keys[i]][2] = False
            robot.log(robot.karb_manager[karb_keys[i]])
            return None
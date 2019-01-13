import constants
import vision
import pathfinding
# TODO - Enemy analysis function
# TODO - All archer formation functions

def give_military_command(robot, recieved_message = 0, self_signal = 0):
    if recieved_message == 0 and self_signal == 0:
        return default_military_behaviour(robot)

def _crusader_combat(robot):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    if len(visible_enemy_list) == 0:
        return None
    else:
        unit_attackrange_max = constants.crusader_max_attack_range
        unit_attackdamge = constants.crusader_attack_damage
        unit_current_pos = (robot.me.x, robot.me.y)
        unit_will_attack_list = []
        # unit_will_kill_list = []
        unit_will_attack_pilgrim_list = []

        for iter_i in range(len(visible_enemy_list)): # As not sure whether enumerate will work
            enemy = visible_enemy_list[iter_i]
            enemy_distance = visible_enemy_distance[iter_i]
            if enemy_distance <= unit_attackrange_max:
                if enemy['unit'] == constants.unit_pilgrim:
                    unit_will_attack_pilgrim_list.append(enemy)
                else:
                    unit_will_attack_list.append(enemy)

        if len(unit_will_attack_list) !=0:
            enemy = unit_will_attack_list[0]
            # robot.log("Crusader f-i-g-h-t-i-n-g`")
            return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        elif len(unit_will_attack_pilgrim_list) != 0 :
            enemy = unit_will_attack_pilgrim_list[0]
            # robot.log("Crusader bullying pilgrim")
            return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        else:
            enemy = visible_enemy_list[0]
            # robot.log(enemy)
            # robot.log(unit_current_pos)
            move_to = pathfinding.astar_search(robot, unit_current_pos, (enemy['x'], enemy['y']), 3)[0]
            if move_to != None and len(move_to) != 0:
                # robot.log("Moving to " + str(move_to))
                new_pos_x, new_pos_y = move_to
                return robot.move(new_pos_x - unit_current_pos[0], new_pos_y - unit_current_pos[1])
        return None

def _prophet_combat(robot):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    if len(visible_enemy_list) == 0:
        return None
    else:
        unit_attack_range_max = constants.prophet_max_attack_range
        unit_attack_range_min = constants.prophet_min_attack_range
        unit_attack_damage = constants.prophet_attack_damage
        unit_current_pos = (robot.me.x, robot.me.y)

        unit_will_attack_list = []
        unit_will_attack_pilgrim_list = []
        for i in range(len(visible_enemy_list)):
            enemy = visible_enemy_list[i]
            enemy_distance = visible_enemy_distance[i]
            if enemy_distance <= unit_attack_range_max and enemy_distance >= unit_attack_range_min:
                if enemy['unit'] == constants.unit_pilgrim:
                    unit_will_attack_pilgrim_list.append(enemy)
                else:
                    unit_will_attack_list.append(enemy)

        if len(unit_will_attack_list) != 0:
            enemy = unit_will_attack_list[0]
            return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        elif len(unit_will_attack_pilgrim_list) != 0:
            enemy = unit_will_attack_pilgrim_list[0]
            return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        else:
            # Archers should not be moving towards targets!
            None
        return None


def default_military_behaviour(robot):
    unit_type = robot.me.unit

    if unit_type == constants.unit_crusader:        
        return _crusader_combat(robot)
    elif unit_type == constants.unit_preacher:
        return None
    elif unit_type == constants.unit_prophet:
        return _prophet_combat(robot)

def pilgrimpriority():
    return False

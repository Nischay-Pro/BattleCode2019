import constants
import vision
import pathfinding
import tactics
# TODO - Enemy analysis function
# TODO - All archer formation functions

def give_military_command(robot, recieved_message = 0, self_signal = 0):
    if recieved_message == 0 and self_signal == 0:
        return default_military_behaviour(robot)

def _prophet_combat(robot):
    # TODO : store the health of enemy assuming that it has full health
    # TODO : remove from dictionary if the health of an enemy becomes zero
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)

    if len(visible_enemy_list) != 0:

        unit_current_pos = (robot.me.x, robot.me.y)
        unit_will_attack_list = []
        unit_will_attack_pilgrim_list = []
        unit_will_attack_id = []
        unit_cant_attack_list  = []

        for i in range(len(visible_enemy_list)):
            enemy = visible_enemy_list[i]
            enemy_distance = visible_enemy_distance[i]
            # Attack Range Is Vision Range
            if enemy['id'] not in robot.has_enemy_target_dict:
                robot.has_enemy_target_dict[enemy['id']] = enemy
            
            # Units In Attack Range
            if enemy_distance <= robot.prophet_attack_range_max and enemy_distance >= robot.prophet_attack_range_min:
                if enemy['unit'] == constants.unit_pilgrim:
                    unit_will_attack_pilgrim_list.append(enemy)
                else:
                    unit_will_attack_list.append(enemy)
                unit_will_attack_id.append(enemy['id'])
            elif enemy_distance < robot.prophet_attack_range_min:
                unit_cant_attack_list.append(enemy['id'])

        target_robot_id = robot.is_targeting_robot_with_id
        enemy = None

        # # TODO - Include friendly units in these calculations
        # if len(unit_will_attack_list) == 1:
        #     enemy = tactics.prophet_will_combat_1vs1(robot, unit_will_attack_list[0])
            
        if len(unit_will_attack_list) != 0:
            enemy = unit_will_attack_list[0]
            robot.is_targeting_robot_with_id = enemy['id']
            # return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        elif len(unit_will_attack_pilgrim_list) != 0:
            enemy = unit_will_attack_pilgrim_list[0]
            robot.is_targeting_robot_with_id = enemy['id']
            # return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        else:
            # Archers should not be moving towards targets!
            None

        if target_robot_id in unit_will_attack_id:
            old_enemy = robot.has_enemy_target_dict[target_robot_id]
            return robot.attack(old_enemy['x'] - unit_current_pos[0], old_enemy['y'] - unit_current_pos[1])
        if enemy:
            robot.is_targeting_robot_with_id = enemy['id']
            return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
        return None
    else:
        return None

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
            move_to, robot.burned_out = pathfinding.astar_search(robot, unit_current_pos, (enemy['x'], enemy['y']), 3)[0]
            if move_to != None and len(move_to) != 0:
                # robot.log("Moving to " + str(move_to))
                new_pos_x, new_pos_y = move_to
                return robot.move(new_pos_x - unit_current_pos[0], new_pos_y - unit_current_pos[1])
        return None

# TODO - Preacher check which direction the friendlies are in and see if it's safe to drop AOE attack
# If Preacher between Friendly and Enemy, preacher should attack (?)
def _preacher_combat(robot):
    visible_friendly_list = []
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    if friendlyfire():
        visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)
    if len(visible_enemy_list) == 0:
        return None
    else:
        unit_attack_range_max = constants.preacher_max_attack_range
        unit_attack_range_min = constants.preacher_min_attack_range
        unit_attack_damage = constants.preacher_attack_damage
        unit_current_pos = (robot.me.x, robot.me.y)

        unit_will_attack_list = []
        unit_will_attack_pilgrim_list = []
        friendly_list = []
        for i in range(len(visible_enemy_list)):
            enemy = visible_enemy_list[i]
            enemy_distance = visible_enemy_distance[i]
            if enemy_distance <= unit_attack_range_max and enemy_distance >= unit_attack_range_min:
                if enemy['unit'] == constants.unit_pilgrim:
                    unit_will_attack_pilgrim_list.append(enemy)
                else:
                    unit_will_attack_list.append(enemy)

        for i in range(len(visible_friendly_list)):
            friendly = visible_friendly_list[i]
            friendly_distance = visible_friendly_distance[i]
            if friendly_distance <= unit_attack_range_max and friendly_distance >= unit_attack_range_min:
                friendly_list.append(friendly)

        if len(friendly_list) != 0:
            if friendlyfire():
                if len(unit_will_attack_list) != 0:
                    enemy = unit_will_attack_list[0]
                    return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
                elif len(unit_will_attack_pilgrim_list) != 0:
                    enemy = unit_will_attack_pilgrim_list[0]
                    return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
                else:
                    # Preachers should not be moving towards targets!
                    None
        else:
            if len(unit_will_attack_list) != 0:
                enemy = unit_will_attack_list[0]
                return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
            elif len(unit_will_attack_pilgrim_list) != 0:
                enemy = unit_will_attack_pilgrim_list[0]
                return robot.attack(enemy['x'] - unit_current_pos[0], enemy['y'] - unit_current_pos[1])
            else:
                # Preachers should not be moving towards targets!
                None
        return None

def default_military_behaviour(robot):
    unit_type = robot.me.unit

    if unit_type == constants.unit_crusader:
        return _crusader_combat(robot)
    elif unit_type == constants.unit_preacher:
        return _preacher_combat(robot)
    elif unit_type == constants.unit_prophet:
        return _prophet_combat(robot)

def pilgrimpriority():
    return False

def friendlyfire():
    return False

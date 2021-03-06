import constants
import utility
import vision

def fill_combat_map(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y
    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    combat_map_length = len(robot.combat_map)

    min_x = pos_x - (combat_map_length - 1)/2
    max_x = pos_x + (combat_map_length - 1)/2
    min_y = pos_y - (combat_map_length - 1)/2
    max_y = pos_y + (combat_map_length - 1)/2

    visible_units = robot.get_visible_robots()
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    visible_friendly_distance, visible_friendly_list = vision.sort_visible_friendlies_by_distance(robot)

    for iter_i in range(len(combat_map_length)):
        for iter_j in range(len(combat_map_length)):
            # Impassable or out of bounds
            if utility.is_out_of_bounds(combat_map_length, iter_j + min_x, iter_i + min_y) or passable_map[iter_i][iter_j]!= 1:
                robot.combat_map[iter_i][iter_j] = -1

    for unit in visible_units:
        if robot.is_visible(unit):
            if unit['team']  == robot.me.team:
                # 1 to 4096
                robot.combat_map[unit['y'] - min_y][unit['x'] - min_x] = unit['id']
            else:
                # -2 to -4097
                robot.combat_map[unit['y'] - min_y][unit['x'] - min_x] = -unit['id'] - 1

    # robot.combat_map


def is_unit_safe_at_current_position(robot):
    visible_enemy_distance, visible_enemy_list = vision.sort_visible_enemies_by_distance(robot)
    danger_count = 0
    for iter_i in range(len(visible_enemy_list)):
        unit = visible_enemy_list[iter_i]
        distance = visible_enemy_distance[iter_i]
        attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health = give_stats(unit)
        if distance >= min_attack_range and distance <= max_attack_range:
            danger_count += 1
    return danger_count

def is_unit_in_enemy_unit_vision_range(robot):
    None

def is_unit_in_enemy_unit_attack_range(robot):
    None

def give_postions_where_unit_can_evade_enemy_vision(robot):
    None

def give_postions_where_unit_can_unit_evade_attack(robot):
    None

def give_postions_where_unit_is_in_handicapped_area(robot):
    None

def can_unit_kite(robot):
    None

def compare_combat_map(robot):
    None

def retreat_decider(robot):
    #On the ratio of your troops, enemy troops and signal
    None


def give_stats(unit):
    if unit['unit'] == constants.unit_castle:
        return _give_castle_stats()
    elif unit['unit'] ==  constants.unit_church:
        return _give_church_stats()
    elif unit['unit'] == constants.unit_pilgrim:
        return _give_pilgrim_stats()
    elif unit['unit'] == constants.unit_prophet:
        return _give_prophet_stats()
    elif unit['unit'] == constants.unit_crusader:
        return _give_crusader_stats()
    elif unit['unit'] == constants.unit_preacher:
        return _give_preacher_stats()

def _give_castle_stats():
    attack_damage = constants.castle_attack_damage
    speed = 0
    min_attack_range = constants.castle_min_attack_range
    max_attack_range = constants.castle_max_attack_range
    vision_range = constants.castle_vision_range
    has_handicapped_area = 0
    max_health = constants.castle_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_church_stats():
    attack_damage = 0
    speed = 0
    min_attack_range = 0
    max_attack_range = 0
    vision_range = constants.church_vision_range
    has_handicapped_area = 0
    max_health = constants.church_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_pilgrim_stats():
    attack_damage = 0
    speed = constants.pilgrim_speed
    min_attack_range = 0
    max_attack_range = 0
    vision_range = constants.pilgrim_vision_range
    has_handicapped_area = 0
    max_health = constants.pilgrim_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_prophet_stats():
    attack_damage = constants.prophet_attack_damage
    speed = constants.prophet_speed
    min_attack_range = constants.prophet_min_attack_range
    max_attack_range = constants.prophet_max_attack_range
    vision_range = constants.prophet_vision_range
    has_handicapped_area = 1
    max_health = constants.prophet_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_crusader_stats():
    attack_damage = constants.crusader_attack_damage
    speed = constants.crusader_speed
    min_attack_range = constants.crusader_min_attack_range
    max_attack_range = constants.crusader_max_attack_range
    vision_range = constants.crusader_vision_range
    has_handicapped_area = 0
    max_health = constants.crusader_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

def _give_preacher_stats():
    attack_damage = constants.preacher_attack_damage
    speed = constants.preacher_speed
    min_attack_range = constants.preacher_min_attack_range
    max_attack_range = constants.preacher_max_attack_range
    vision_range = constants.preacher_vision_range
    has_handicapped_area = 0
    max_health = constants.preacher_max_health
    return attack_damage, speed, min_attack_range, max_attack_range, vision_range, has_handicapped_area, max_health

from battlecode import SPECS

pathfinding_heuristic_multiplier = 1.1

convoy_age_end_round = 50
convoy_radius = 6
convoy_step_limit = 10
pilgrim_aging_factor = .3 # Weight for the age of pilgrim after whihc it won't try to search for new mines
pilgrim_will_scavenge_closeby_mines_after_turns = 5
pilgrim_will_scavenge_closeby_mines_before_turns = 150
pilgrim_will_scavenge_closeby_mines = pilgrim_aging_factor * 500
pilgrim_fails_to_get_mine_aging = 25
pilgrim_revitalise = 50
pilgrim_burnout_period = 5
prophet_burnout_period = 5

chokepoint_modifier = .4

karbonite_modifier = .05
fuel_modifier = .05

anti_unit_build_factor = 1.2

dark_age = 3
age_one = 10
age_one_economy_under_rush_scale = 0.5
age_two = 50
age_two_economy_under_rush_scale = 0.75
age_three = 100
age_four = 800
resource_locker_capacity = 10
unit_locker_capacity = 10
enemy_locker_capacity = 5

combat_broadcast_cooldown = 50

enemy_unit_priority_for_prophet = [
    2, # Castle
    2, # Church
    3, # Pilgrim
    4, # Crusader
    4, # Prophet
    10, # Preacher
]

# MAYBE TRY CHANGING THIS
pathfinding_power = 100

# DO NOT CHANGE THIS

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

crusader_move_directions = [(0, 3),
    (0, 2),
    (0, 1),
    (1, 2),
    (2, 2),
    (1, 1),
    (2, 1),
    (3, 0),
    (2, 0),
    (1, 0),
    (2, -1),
    (2, -2),
    (1, -1),
    (1, -2),
    (0, -3),
    (0, -2),
    (0, -1),
    (-1, -2),
    (-2, -2),
    (-1, -1),
    (-2, -1),
    (-3, 0),
    (-2, 0),
    (-1, 0),
    (-2, 1),
    (-2, 2),
    (-1, 1),
    (-1, 2)]

non_crusader_move_directions = [(0, 2),
    (0, 1),
    (1, 1),
    (2, 0),
    (1, 0),
    (1, -1),
    (0, -2),
    (0, -1),
    (-1, -1),
    (-2, 0),
    (-1, 0),
    (-1, 1)]

unit_castle = SPECS['CASTLE']
unit_church = SPECS['CHURCH']
unit_crusader = SPECS['CRUSADER']
unit_pilgrim = SPECS['PILGRIM']
unit_preacher = SPECS['PREACHER']
unit_prophet = SPECS['PROPHET']

# Vision Radius
castle_vision_range = SPECS['UNITS'][SPECS["CASTLE"]]['VISION_RADIUS']
church_vision_range = SPECS['UNITS'][SPECS["CHURCH"]]['VISION_RADIUS']
pilgrim_vision_range = SPECS['UNITS'][SPECS["PILGRIM"]]['VISION_RADIUS']
crusader_vision_range = SPECS['UNITS'][SPECS["CRUSADER"]]['VISION_RADIUS']
prophet_vision_range = SPECS['UNITS'][SPECS["PROPHET"]]['VISION_RADIUS']
preacher_vision_range = SPECS['UNITS'][SPECS["PREACHER"]]['VISION_RADIUS']

# Move Fuel Cost
pilgrim_move_fuel_cost = SPECS['UNITS'][SPECS["PILGRIM"]]['FUEL_PER_MOVE']
prophet_move_fuel_cost = SPECS['UNITS'][SPECS["PROPHET"]]['FUEL_PER_MOVE']
crusader_move_fuel_cost = SPECS['UNITS'][SPECS["CRUSADER"]]['FUEL_PER_MOVE']
preacher_move_fuel_cost = SPECS['UNITS'][SPECS["PREACHER"]]['FUEL_PER_MOVE']

# Attack Fuel Cost
prophet_attack_fuel_cost = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_FUEL_COST']
preacher_attack_fuel_cost = SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_FUEL_COST']
crusader_attack_fuel_cost = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_FUEL_COST']
castle_attack_fuel_cost = SPECS['UNITS'][SPECS["CASTLE"]]['ATTACK_FUEL_COST']

# Speed Check
pilgrim_speed = SPECS['UNITS'][SPECS["PILGRIM"]]['SPEED']
prophet_speed = SPECS['UNITS'][SPECS["PROPHET"]]['SPEED']
crusader_speed = SPECS['UNITS'][SPECS["CRUSADER"]]['SPEED']
preacher_speed = SPECS['UNITS'][SPECS["PREACHER"]]['SPEED']

# Attack Damage
castle_attack_damage = SPECS['UNITS'][SPECS["CASTLE"]]['ATTACK_DAMAGE']
crusader_attack_damage = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_DAMAGE']
prophet_attack_damage = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_DAMAGE']
preacher_attack_damage = SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_DAMAGE']

# Attack Range
castle_min_attack_range = SPECS['UNITS'][SPECS["CASTLE"]]['ATTACK_RADIUS'][0]
castle_max_attack_range = SPECS['UNITS'][SPECS["CASTLE"]]['ATTACK_RADIUS'][1]
crusader_min_attack_range = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][0]
crusader_max_attack_range = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][1]
prophet_min_attack_range = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_RADIUS'][0]
prophet_max_attack_range = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_RADIUS'][1]
preacher_min_attack_range = SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][0]
preacher_max_attack_range = SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][1]

# Initial Health
castle_max_health = SPECS['UNITS'][SPECS["CASTLE"]]['STARTING_HP']
church_max_health = SPECS['UNITS'][SPECS["CHURCH"]]['STARTING_HP']
pilgrim_max_health = SPECS['UNITS'][SPECS["PILGRIM"]]['STARTING_HP']
crusader_max_health = SPECS['UNITS'][SPECS["CRUSADER"]]['STARTING_HP']
prophet_max_health = SPECS['UNITS'][SPECS["PROPHET"]]['STARTING_HP']
preacher_max_health = SPECS['UNITS'][SPECS["PREACHER"]]['STARTING_HP']

# Construction Cost
castle_construction_karbonite = SPECS['UNITS'][SPECS["CASTLE"]]['CONSTRUCTION_KARBONITE']
castle_construction_fuel = SPECS['UNITS'][SPECS["CASTLE"]]['CONSTRUCTION_FUEL']
church_construction_karbonite = SPECS['UNITS'][SPECS["CHURCH"]]['CONSTRUCTION_KARBONITE']
church_construction_fuel = SPECS['UNITS'][SPECS["CHURCH"]]['CONSTRUCTION_FUEL']
pilgrim_construction_karbonite = SPECS['UNITS'][SPECS["PILGRIM"]]['CONSTRUCTION_KARBONITE']
pilgrim_construction_fuel = SPECS['UNITS'][SPECS["PILGRIM"]]['CONSTRUCTION_FUEL']
prophet_construction_karbonite = SPECS['UNITS'][SPECS["PROPHET"]]['CONSTRUCTION_KARBONITE']
prophet_construction_fuel = SPECS['UNITS'][SPECS["PROPHET"]]['CONSTRUCTION_FUEL']
crusader_construction_karbonite = SPECS['UNITS'][SPECS["CRUSADER"]]['CONSTRUCTION_KARBONITE']
crusader_construction_fuel = SPECS['UNITS'][SPECS["CRUSADER"]]['CONSTRUCTION_FUEL']
preacher_construction_karbonite = SPECS['UNITS'][SPECS["PREACHER"]]['CONSTRUCTION_KARBONITE']
preacher_construction_fuel = SPECS['UNITS'][SPECS["PREACHER"]]['CONSTRUCTION_FUEL']

# SPEC API
# public int CONSTRUCTION_KARBONITE;
# public int CONSTRUCTION_FUEL;
# public int KARBONITE_CAPACITY;
# public int FUEL_CAPACITY;
# public int SPEED;
# public int FUEL_PER_MOVE;
# public int STARTING_HP;
# public int VISION_RADIUS;
# public int ATTACK_DAMAGE;
# public int[] ATTACK_RADIUS;
# public int ATTACK_FUEL_COST;
# public int DAMAGE_SPREAD;


# directions of pilgrim
pilgrim_directions = [
        None, # self signal is "0"
        (0, 0), # 1: no step
        (0, 1), # 2: one step east
        (0, 2), # 3: two steps east
        (0, -1), # 4: one step west
        (0, -2), # 5: two steps west
        (-1, 0), # 6: one step north
        (-2, 0), # 7: two steps north
        (1, 0), # 8: one step south
        (2, 0), # 9: two steps south
        (-1, 1), # 10: one step north-east
        (-1, -1), # 11: one step north-west
        (1, -1), # 12: one step south-west
        (1, 1) # 13: one step south-east
    ]

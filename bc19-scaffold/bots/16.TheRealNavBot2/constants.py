from battlecode import SPECS

pathfinding_heuristic_multiplier = 1.1

pilgrim_aging_factor = .3 # Weight for the age of pilgrim after whihc it won't try to search for new mines
pilgrim_will_scavenge_closeby_mines_after_turns = 30
pilgrim_will_scavenge_closeby_mines_before_turns = 150
pilgrim_will_scavenge_closeby_mines = pilgrim_aging_factor * 500
pilgrim_fails_to_get_mine_aging = 25
pilgrim_revitalise = 50
chokepoint_modifier = .4
karbonite_modifier = .05
fuel_modifier = .05


enemy_unit_priority_for_prophet = [ 
    2, # Castle
    2, # Church
    3, # Pilgrim
    4, # Crusader
    4, # Prophet
    10, # Preacher
]

# MAYBE TRY CHANGING THIS
pathfinding_power = 60 

# DO NOT CHANGE THIS
 
directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

crusader_move_directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1), 
                (0, 2), (0, -2), (2, 0), (-2, 0), (-1, 2), (1, 2), (1, -2), (-1, -2),
                (2, -1), (2, 1), (-2, 1), (-2, -1), (2, 2), (2, -2), (-2, 2), (-2, -2),
                (0, 3), (0, -3), (3, 0), (-3, 0)]

non_crusader_move_directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1), (0, 2), (0, -2), (2, 0), (-2, 0)]


unit_castle = SPECS['CASTLE']
unit_church = SPECS['CHURCH']
unit_crusader = SPECS['CRUSADER']
unit_pilgrim = SPECS['PILGRIM']
unit_preacher = SPECS['PREACHER']
unit_prophet = SPECS['PROPHET']

# Attack Damage
crusader_attack_damage = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_DAMAGE']
prophet_attack_damage = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_DAMAGE']
preacher_attack_damage = SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_DAMAGE']

# Attack Range
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

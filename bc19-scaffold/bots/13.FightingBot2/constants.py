from battlecode import SPECS

pilgrim_will_scavenge_closeby_mines_before_turns = 10
pilgrim_will_scavenge_closeby_mines = 50
chokepoint_modifier = .4
karbonite_modifier = .05
fuel_modifier = .05

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

enemy_unit_priority_for_prophet = [ 
    2, # Castle
    2, # Church
    3, # Pilgrim
    4, # Crusader
    4, # Prophet
    10, # Preacher
]

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
crusader_max_attack_range = SPECS['UNITS'][SPECS["CRUSADER"]]['ATTACK_RADIUS'][1]
prophet_min_attack_range = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_RADIUS'][0]
prophet_max_attack_range = SPECS['UNITS'][SPECS["PROPHET"]]['ATTACK_RADIUS'][1]
preacher_max_attack_range = SPECS['UNITS'][SPECS["PREACHER"]]['ATTACK_RADIUS'][1]

# Initial Health
crusader_max_health = SPECS['UNITS'][SPECS["CRUSADER"]]['STARTING_HP']
prophet_max_health = SPECS['UNITS'][SPECS["PROPHET"]]['STARTING_HP']
preacher_max_health = SPECS['UNITS'][SPECS["PREACHER"]]['STARTING_HP']

pilgrim_will_scavenge_closeby_mines_after_turns = 50


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

def get_required_constant():
    None
from battlecode import BCAbstractRobot
import battlecode as bc
import utility
import constants
import communications

import castles
import churches
import crusaders
import pilgrims
import preachers
import prophets


__pragma__('iconv')
__pragma__('tconv')
#__pragma__('opov')

# don't try to use global variables!!

# Helper Function

def find_unit_type(self, map):
    None

# TODO - Add condition that team has fuel before making it move
# TODO - Before final turn, make sure that as much resources has been consumed
# TODO - Symmetry variable use
class MyRobot(BCAbstractRobot):

    step = -1

    unit_spawn_loc = None # Give location of unit spwaned -> Tuple
    current_move_destination = None # Give the current destination to move to -> Tuple
    built_by_a_castle = 0 # Boolean
    built_by_a_church = 0 # Boolean
    our_castle_or_church_base = None # Give location of home castle/church -> Tuple
    friendly_castles = []
    friendly_churches = []
    enemy_castles = []
    enemy_churches = []

    mov_path_between_location_and_destination = None # So we can go back and forth by reversing list
    mov_path_index = 0 # to keep track of movement in the above index
    map_symmetry = None # 0 - Horizontal, 1 is vertical


    # Pilgrims
    pilgrim_type = 0 # 0 for miner, 1 for transporter, 2 for scavenger and 3 for scout
    pilgrim_mine_ownership = None # Does pilgrim own a mine or is traversing back and forth -> Tuple denotes mine position
    pilgrim_in_danger = 0 # Boolean, true if it has seen enemy unit and no friendly combat units in vision
    has_made_random_movement = 0
    pilgrim_scavenge_mine_location_list = []
    pilgrim_scavenge_mine_occupancy_list = []
    pilgrim_mine_age_limt = constants.pilgrim_aging_factor * 300

    # Castles
    castle_unit_build_log = [] # Maintain the ids of robots, pop and push every turn
    fuel_mine_locations_from_this_castle = [] # Compute once and store forever
    fuel_mine_occupancy_from_this_castle = [] # When you assign a unit to mine , make that element id 0 or more else it is -1. TODO - Pilgrim retrun signal telling mine is occupied
    karb_mine_locations_from_this_castle = []
    karb_mine_occupancy_from_this_castle = []
    castle_health = None
    pilgrim_assign_to_mine_type = 0 # 0 for karbonite, 1 for fuel
    castle_under_attack = 0 # Boolean, if for 5 turn no more decrease in health,
    castle_under_attack_turn = None # Change to turn number of attack
    pilgrim_build_number = 0

    # Church
    church_unit_build_log = [] # Maintains ids of nearby robots
    home_castle_location = None # TODO - Given by pilgrim that built church

    # Combat Units
    is_targeting_robot_with_id = None # Remember robot to kill, after current turn
    has_enemy_target_dict = {} # Pop and
    is_fleeing_to_home_base = 0 # Boolean, switch to one if routed
    has_unit_value = 1 # Decreases if less health or too much danger

    # Misc

    def turn(self):

        self.step += 1
        unit_type = self.me['unit']

        # DEBUG
        # self.log("START TURN " + self.step)
        # self.log("Running pathfinding")

        # Get spawn location
        if self.unit_spawn_loc is None:
            # first turn!
            self.unit_spawn_loc = (self.me['x'], self.me['y'])

        self.castle_talk(self.me.unit)


        if self.step % 200 == 3 and unit_type == constants.unit_castle:
            # robot.log(str(self.me))
            self.log("Total current karbonite is " + str(self.karbonite) + " turn " + (str(self.step)))

        if unit_type == constants.unit_castle:
            return castles.castle(self)
        # elif unit_type == unit_church:
        #     return churches.church(self)
        # elif unit_type == constants.unit_crusader:
        #     return crusaders.crusader(self)
        # elif unit_type == constants.unit_preacher:
        #     return preachers.preacher(self)
        elif unit_type == constants.unit_prophet:
            return prophets.prophet(self)
        elif unit_type == constants.unit_pilgrim:
            return pilgrims.pilgrim(self)

robot = MyRobot()

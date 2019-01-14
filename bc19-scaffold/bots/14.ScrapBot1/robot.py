from battlecode import BCAbstractRobot
import battlecode as bc
import utility
import constants

import castles
import churches
import crusaders
import pilgrims
import preachers
import prophets
import communications

__pragma__('iconv')
__pragma__('tconv')
#__pragma__('opov')

# don't try to use global variables!!

# Helper Function

def find_unit_type(self, map):
    None

# TODO - Add condition that team has fuel before making it move
# TODO - Before final turn, make sure that as much resources has been consumed
class MyRobot(BCAbstractRobot):

    step = -1
    
    unit_spawn_loc = None # Give location of unit spwaned -> Tuple
    current_move_destination = None # Give the current destination to move to -> Tuple
    built_by_a_castle = 0 # Boolean
    built_by_a_church = 0 # Boolean
    our_castle_or_church_base = None # Give location of initial castles-> Tuple
    our_original_castle_location = None # Equivalent to `our_castle_or_church_base` if built by castle, otherwise given by church

    # Pilgrims
    pilgrim_mine_ownership = None # Does pilgrim own a mine or is traversing back and forth -> 0 or 1
    mov_path_between_base_and_mine = [] # So we can go back and forth by reversing list
    mov_path_index = 0 # to keep track of movement in the above index
    pilgrim_in_danger = 0 # Boolean, true if it has seen enemy unit and no friendly combat units in vision

    # Castles
    castle_unit_build_log = [] # Maintain the ids of robots, pop and push every turn
    fuel_mine_locations_from_this_castle = [] # Compute once and store forever
    fuel_mine_occupancy_from_this_castle = [] # When you assign a unit to mine , make that element 1 else it is zero. TODO - Pilgrim retrun signal telling mine is occupied
    karb_mine_locations_from_this_castle = [] 
    karb_mine_occupancy_from_this_castle = []
    castle_health = None
    pilgrim_assign_to_mine = 0 # 0 for karbonite, 1 for fuel
    castle_under_attack = 0 # Boolean, if for 5 turn no more decrease in health, 
    castle_under_attack_turn = None # Change to turn number of attack

    # Church
    church_unit_build_log = [] # Maintains ids of nearby robots 
    home_castle_location = None # TODO - Given by pilgrim that built church

    # Combat Units
    is_targeting_robot_with_id = None # Remember robot to kill, after current turn
    has_enemy_target_dict = {} # Pop and 
    is_fleeing_to_home_base = 0 # Boolean, switch to one if routed
    has_unit_value = 1 # Decreases if less health or too much danger

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
        elif unit_type == constants.unit_crusader:
            return crusaders.crusader(self)
        elif unit_type == constants.unit_preacher:
            return preachers.preacher(self)
        elif unit_type == constants.unit_prophet:
            return prophets.prophet(self)
        elif unit_type == constants.unit_pilgrim:
            return pilgrims.pilgrim(self)

robot = MyRobot()

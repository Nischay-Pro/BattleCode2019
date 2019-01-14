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

def go_home(self):
    unit_map = self.getVisibleRobotMap()
    # unit_type  = SPECS['CASTLE']

def find_unit_type(self, map):
    None

# TODO - Add condition that team has fuel before making it move
# TODO - Before final turn, make sure that as much resources has been consumed
class MyRobot(BCAbstractRobot):

    step = -1

    def turn(self):
        self.step += 1
        unit_type = self.me['unit']
        
        # DEBUG
        # self.log("START TURN " + self.step)
        # self.log("Running pathfinding")

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

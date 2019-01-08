from battlecode import BCAbstractRobot, SPECS
import battlecode as bc
import random


__pragma__('iconv')
__pragma__('tconv')
#__pragma__('opov')

# don't try to use global variables!!

def crusaders_move(self):
    # self.log("Crusader health: " + str(self.me['health']))
    # The directions: North, NorthEast, East, SouthEast, South, SouthWest, West, NorthWest
    choices = [(0,-1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    choice = random.choice(choices)
    # self.log('TRYING TO MOVE IN DIRECTION ' + str(choice))
    return choice

class MyRobot(BCAbstractRobot):

    step = -1

    def turn(self):
        self.step += 1

        unit_castle = SPECS['CASTLE']
        unit_church = SPECS['CHURCH']
        unit_crusader = SPECS['CRUSADER']
        unit_pilgrim = SPECS['PILGRIM']
        unit_preacher = SPECS['PREACHER']
        unit_priest = SPECS['PRIEST']
        unit_prophet = SPECS['PROPHET']

        # self.log("START TURN " + self.step)
        
        
        if self.me['unit'] == unit_crusader:
            return self.move(crusaders_move(self))

        elif self.me['unit'] == unit_castle:
            if self.step < 10:
                # self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
                return self.build_unit(unit_crusader, 1, 1)

            else:
                None
                # self.log("Castle health: " + self.me['health'])

robot = MyRobot()



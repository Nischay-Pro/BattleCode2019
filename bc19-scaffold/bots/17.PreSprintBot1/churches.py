import utility
import constants
import production_module

# Add code for locked castles

def church(robot):
    if robot.step < 2:
        # self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
        return production_module.default_production_order(robot, constants.unit_prophet)
    # elif robot.step > 500 and robot.karbonite > 100 and robot.fuel > 200:
    #     return castle_build(robot, SPECS['PILGRIM'])
    else:
        None
        # self.log("Castle health: " + self.me['health'])
import utility
import constants
import production_module

# Add code for locked castles

def church(robot):
    if robot.step < 4 and robot.fuel >= 50 and robot.karbonite >=40:
        # self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
        return production_module.default_production_order(robot)
    elif robot.step > 300 and robot.karbonite > 100 and robot.fuel > 200:
        return robot.castle_build(robot, constants.unit_prophet)
    else:
        None
        # self.log("Castle health: " + self.me['health'])

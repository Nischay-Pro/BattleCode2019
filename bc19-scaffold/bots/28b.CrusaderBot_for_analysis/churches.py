import check
import churches_utility
import communications
import constants
import production_module
import utility

# Add code for locked castles

def church(robot):
    if robot.step == 0:
        churches_utility.recieve_initial_signal(robot)
    if robot.step < 4 and robot.fuel >= 50 and robot.karbonite >=40:
        robot.signal(1, 2)
        # self.log("Building a crusader at " + str(self.me['x']+1) + ", " + str(self.me['y']+1))
        return production_module.default_production_order(robot)
    elif robot.step > 250 and robot.karbonite > 100 and robot.fuel > 200:
        robot.signal(1, 2)
        return churches_utility.church_build(robot, constants.unit_crusader)
    else:
        None
        # self.log("Castle health: " + self.me['health'])

import constants

def move_check(robot, dx, dy, flag):
    distance = dx**2 + dy**2
    if robot.me.unit == constants.unit_pilgrim:
        if distance <= constants.pilgrim_speed:
            if robot.fuel >= constants.pilgrim_move_fuel_cost * distance:
                return robot.move(dx, dy)
        else:
            robot.log("Move check failed " +  str(flag))
            return None
    if robot.me.unit == constants.unit_prophet:
        if distance <= constants.prophet_speed:
            if robot.fuel >= constants.prophet_move_fuel_cost * distance:
                return robot.move(dx, dy)
        else:
            robot.log("Move check failed " +  str(flag))
            return None
    if robot.me.unit == constants.unit_crusader:
        if distance <= constants.crusader_speed:
            if robot.fuel >= constants.prophet_move_fuel_cost * distance:
                return robot.move(dx, dy)
        else:
            robot.log("Move check failed " +  str(flag))
            return None
    if robot.me.unit == constants.unit_preacher:
        if distance <= constants.prophet_speed:
            if robot.fuel >= constants.preacher_move_fuel_cost * distance:
                return robot.move(dx, dy)
        else:
            robot.log("Move check failed " +  str(flag))
            return None

def mine_check(robot, flag):
    if robot.me.unit == constants.unit_pilgrim:
        if robot.fuel >= 1:
            return robot.mine()
    else:
        robot.log("Mine check failed " + str(flag))
        return None

def attack_check(robot, dx, dy, flag):
    distance = dx**2 + dy**2
    if robot.me.unit == constants.unit_prophet:
        if distance <= constants.prophet_max_attack_range and distance >= constants.prophet_min_attack_range:
            if robot.fuel >= distance * constants.prophet_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None
    if robot.me.unit == constants.unit_preacher:
        if distance <= constants.preacher_max_attack_range and distance >= constants.preacher_min_attack_range:
            if robot.fuel >= distance * constants.preacher_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None
    if robot.me.unit == constants.unit_crusader:
        if distance <= constants.crusader_max_attack_range and distance >= constants.crusader_min_attack_range:
            if robot.fuel >= distance * constants.crusader_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None

def give(robot, dx, dy, karbonite, fuel, flag):
    None

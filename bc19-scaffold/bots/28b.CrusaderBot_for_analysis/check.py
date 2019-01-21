import constants

def move_check(robot, dx, dy, flag):
    distance = dx**2 + dy**2
    robot.position_at_end_of_turn = (robot.me.x, robot.me.y)
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
            # robot.log(constants.crusader_speed)
            # robot.log(str(dx, dy))
            # robot.log("Move check failed " +  str(flag))
            return None
    if robot.me.unit == constants.unit_preacher:
        if distance <= constants.prophet_speed:
            if robot.fuel >= constants.preacher_move_fuel_cost * distance:
                return robot.move(dx, dy)
        else:
            robot.log("Move check failed " +  str(flag))
            return None

def mine_check(robot, flag):
    robot.position_at_end_of_turn = (robot.me.x, robot.me.y)
    if robot.me.unit == constants.unit_pilgrim:
        if robot.fuel >= 1:
            return robot.mine()
    else:
        robot.log("Mine check failed " + str(flag))
        return None

def attack_check(robot, dx, dy, flag):
    distance = dx**2 + dy**2
    robot.position_at_end_of_turn = (robot.me.x, robot.me.y)
    if robot.me.unit == constants.unit_prophet:
        if distance <= constants.prophet_max_attack_range and distance >= constants.prophet_min_attack_range:
            if robot.fuel >= constants.prophet_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None
    if robot.me.unit == constants.unit_preacher:
        if distance <= constants.preacher_max_attack_range and distance >= constants.preacher_min_attack_range:
            if robot.fuel >= constants.preacher_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None
    if robot.me.unit == constants.unit_crusader:
        if distance <= constants.crusader_max_attack_range and distance >= constants.crusader_min_attack_range:
            if robot.fuel >= constants.crusader_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None
    if robot.me.unit == constants.unit_castle:
        if distance <= constants.castle_max_attack_range and distance >= constants.castle_min_attack_range:
            if robot.fuel >= constants.castle_attack_fuel_cost:
                return robot.attack(dx, dy)
        else:
            robot.log("Attack check failed " + str(flag))
            return None

def build_check(robot, build_unit_type, dx, dy, flag):
    distance = dx**2 + dy**2
    current_fuel = robot.fuel
    current_karbonite = robot.karbonite
    robot.position_at_end_of_turn = (robot.me.x, robot.me.y)
    if distance <= 2:
        if build_unit_type == constants.unit_church and current_fuel >= constants.church_construction_fuel and current_karbonite >= constants.church_construction_karbonite:
            return robot.build_unit(build_unit_type, dx, dy)
        elif build_unit_type == constants.unit_pilgrim and current_fuel >= constants.pilgrim_construction_fuel and current_karbonite >= constants.pilgrim_construction_karbonite:
            return robot.build_unit(build_unit_type, dx, dy)
        elif build_unit_type == constants.unit_prophet and current_fuel >= constants.prophet_construction_fuel and current_karbonite >= constants.prophet_construction_karbonite:
            return robot.build_unit(build_unit_type, dx, dy)
        elif build_unit_type == constants.unit_preacher and current_fuel >= constants.preacher_construction_fuel and current_karbonite >= constants.preacher_construction_karbonite:
            return robot.build_unit(build_unit_type, dx, dy)
        elif build_unit_type == constants.unit_crusader and current_fuel >= constants.crusader_construction_fuel and current_karbonite >= constants.crusader_construction_karbonite:
            return robot.build_unit(build_unit_type, dx, dy)
        else:
            dfuel = 0
            dkarb = 0
            if build_unit_type == constants.unit_church:
                dfuel = constants.church_construction_fuel - current_fuel
                dkarb = constants.church_construction_karbonite - current_karbonite
            elif build_unit_type == constants.unit_pilgrim:
                dfuel = constants.pilgrim_construction_fuel - current_fuel
                dkarb = constants.pilgrim_construction_karbonite - current_karbonite
            elif build_unit_type == constants.unit_prophet:
                dfuel = constants.prophet_construction_fuel - current_fuel
                dkarb = constants.prophet_construction_karbonite - current_karbonite
            elif build_unit_type == constants.unit_preacher:
                dfuel = constants.preacher_construction_fuel - current_fuel
                dkarb = constants.preacher_construction_karbonite - current_karbonite
            elif build_unit_type == constants.unit_crusader:
                dfuel = constants.crusader_construction_fuel - current_fuel
                dkarb = constants.crusader_construction_karbonite - current_karbonite
            dfuel = 0 if dfuel < 0 else dfuel
            dkarb = 0 if dkarb < 0 else dkarb
            robot.log("Not enough fuel or karbonite to build unit " + str(flag) + ". Deficit of " + str(dfuel) + " fuel and " + str(dkarb) + " karbonite.")
            return None
    else:
        robot.log("Build check failed " + str(flag))
        return None

def give_check(robot, dx, dy, karbonite, fuel, flag):
    robot.position_at_end_of_turn = (robot.me.x, robot.me.y)
    None

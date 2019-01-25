import vision

''' Special Cases

            Description                             Assignment Index

    If no fuel and no karbonite                            1
    If no fuel but karbonite                               2
    If fuel but no karbonite                               3
    If map is super narrow (Only 1 tile movable)           4                #TODO Add this feature

'''

def is_this_a_special_map(robot):
    ## Check for No Fuel No Karbonite
    karbs = vision.all_karbonite(robot)
    fuels = vision.all_fuel(robot)
    if karbs == 0 and fuels == 0:
        robot.special_case = 1
    elif karbs > 0 and fuels == 0:
        robot.special_case = 2
    elif karbs == 0 and fuels > 0:
        robot.special_case = 3
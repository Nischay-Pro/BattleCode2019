
''' Signal Protocol

Reserved Signals

    0 -
    1 - Built by this unit (Church and Castle Identification Signal)        (Castles, Churches)
    2 -
    3 -
    4 -
    5 -
    6 - Castle instructing all units to build Crusaders                     (Castles)
    7 - Castle instructing all units to build Prophets                      (Castles)
    8 - Castle instructing all units to build Preachers                     (Castles)
    9 - Castle instructing all units to build Piligrims                     (Castles)
    10 - Update ratio Crusader : Prophet make it 2 : 1                      (Castles)
    11 - Update ratio Crusader : Prophet make it 1 : 2                      (Castles)

    65533 - Crusader Core Ready                                             (Crusader)
    65534 - Failed to allocate mine                                         (Castles)


Reserved Castle Talk

    0 - Castle Identification Signal                                        (Castle)
    1 - Church Identification Signal                                        (Church)
    2 - Piligrim Identification Signal                                      (Piligrim)
    3 - Crusader Identification Signal                                      (Crusader)
    4 - Prophet Identification Signal                                       (Prophet)
    5 - Preacher Identification Signal                                      (Preacher)

    64 - 127 - Reserved for positions                                      (All Units)


'''


def get_initial_castle_position(robot):
    visible = robot.get_visible_robots()
    if visible == None:
        # That's weird
        return None
    for r in visible:
        if r['signal'] == -1 and r['team'] == robot.me['team'] and r['id'] != robot.me['id']:
            castle_talk_value = r['castle_talk']
            if castle_talk_value >= 64:
                castle_index = r['id']
                if robot.other_castle_index_1 == r['id']:
                    robot.other_castle_1_co_ordinates.append(castle_talk_value - 64)
                elif robot.other_castle_index_2 == r['id']:
                    robot.other_castle_2_co_ordinates.append(castle_talk_value - 64)
                elif robot.other_castle_index_1 == 0:
                    robot.other_castle_index_1 = castle_index
                    robot.other_castle_1_co_ordinates.append(castle_talk_value - 64)
                    robot.number_castles += 1
                elif robot.other_castle_index_2 == 0:
                    robot.other_castle_index_2 = castle_index
                    robot.other_castle_2_co_ordinates.append(castle_talk_value - 64)
                    robot.number_castles += 1
                else:
                    # Huh 4 castles in a map
                    robot.log("Weird Shit 4 castles?")

def broadcast_castle_position(robot):
    if robot.step == 1:
        robot.castle_talk(robot.me['x'] + 64)
    elif robot.step == 2:
        robot.castle_talk(robot.me['y'] + 64)

# Potential TODO
# CHARGE COMMAND
# ATTACK LOCATION AROUND COORDINATE
# GARRISON (USING LATTICE) AND GUARD
# SCOUT
# RETREAT

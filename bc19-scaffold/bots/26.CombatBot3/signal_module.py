

def getInitialCastlePosition(robot):
    visible = robot.get_visible_robots()
    if visible == None:
        # That's weird
        return None
    for r in visible:
        if r['signal'] == -1 and r['team'] == robot.me['team'] and r['id'] != robot.me['id']:
            castle_talk_value = r['castle_talk']
            if castle_talk_value > 64:
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

def broadcastCastlePosition(robot):
    if robot.step == 1:
        robot.castle_talk(robot.me['x'] + 64)
    elif robot.step == 2:
        robot.castle_talk(robot.me['y'] + 64)

        
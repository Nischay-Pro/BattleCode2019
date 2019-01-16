import utility
import pilgrims_utility
import constants
import movement

def pilgrim(robot):

    # TODO - Fix random difficult to find timeout errors happening for some pilgrims in large maps (-s 56)
    # TODO - Add scout bots, who scout if no mine to mine
    # communications.self_communicate_loop(robot)
    # robot.log("Pilgrims current move destination is " + robot.current_move_destination)
    carry_karb = robot.me.karbonite
    carry_fuel = robot.me.fuel

    # The pilgrim is on a mine and wants to deposit resources
    if carry_fuel > 80 or carry_karb > 18:
        # robot.log("Nearing capacity")
        return pilgrim_full(robot)

    # The pilgrim checks if it has a mine on it's current position
    pilgrim_is_mining = pilgrim_mine(robot)
    if pilgrim_is_mining !=0:
        return pilgrim_is_mining

    # Receive signal from castle on which mine to go to
    if robot.step == 0:
        pilgrims_utility.receive_initial_siganl(robot)

    if utility.fuel_less_check(robot):
        return None

    # TODO - Add code to make pilgrim move to church or castle rather just building a new church
    # Move Section
    pilgrim_is_moving = pilgrim_move(robot)
    if pilgrim_is_moving !=0:
        return pilgrim_is_moving

def pilgrim_move(robot):
    # Emergency case, allows pilgrims to mine
    if robot.fuel <= 2:
        return 0
    pos_x = robot.me.x
    pos_y = robot.me.y

    passable_map, occupied_map, karb_map, fuel_map = utility.get_all_maps(robot)
    random_directions = utility.random_cells_around()
    # May change for impossible resources

    pilgrims_utility.did_pilgrim_burn_out(robot)

    # Capture and start mining any resource if more than 50 turns since creation and no mine
    # TODO - Improve this code snippet to mine, if in visible region and empty
    if robot.me.turn > constants.pilgrim_will_scavenge_closeby_mines_after_turns and robot.me.turn < constants.pilgrim_will_scavenge_closeby_mines_before_turns:
        for direction in random_directions:
            if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and utility.is_cell_resourceful(karb_map, fuel_map, pos_x + direction[1],  pos_y + direction[0]):
                return robot.move(direction[1], direction[0])

    # TODO - Make into scout if too old, which will scout enemy bases
    # If the mine is already occupied
    pilgrims_utility.is_pilgrim_scavenging(robot)

    # Just move
    if robot.step < robot.pilgrim_mine_age_limt:
        move_command = movement.move_to_destination(robot)
        if move_command != None:
            return move_command

    # Random Movement when not enough time
    for direction in random_directions:
        if (not utility.is_cell_occupied(occupied_map, pos_x + direction[1],  pos_y + direction[0])) and passable_map[pos_y + direction[0]][pos_x + direction[1]] == 1:
            robot.has_made_random_movement = 1
            return robot.move(direction[1], direction[0])

    return 0

def pilgrim_mine(robot):
    pos_x = robot.me.x
    pos_y = robot.me.y

    karb_map = robot.get_karbonite_map()
    fuel_map = robot.get_fuel_map()

    if utility.is_cell_resourceful(karb_map, fuel_map, pos_x, pos_y):
        robot.signal(0, 0)
        return robot.mine()
    else:
        return 0

def pilgrim_full(robot):
    # If we have adjacent castle/church or haven't reached the convoy age end
    pilgrim_give_or_convoy = pilgrims_utility.give_or_mine(robot)
    if pilgrim_give_or_convoy != 0:
        return pilgrim_give_or_convoy
        
    # FIXME - Make churches not be built if castle/other church is in reasonable travel range
    if robot.karbonite > 50 and robot.fuel > 200:
        return pilgrims_utility.make_church(robot)

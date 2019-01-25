import vision
import check
import combat_utility
import constants
import pathfinding
import mapping

def preacher(robot):
        if robot.step == 0:
                robot.current_move_destination = mapping.find_symmetrical_point(robot, robot.me.x, robot.me.y)

        distances, enemies = vision.sort_visible_enemies_by_distance(robot)
        l = len(enemies)
        if l > 0:
                for i in range(l):
                        robot.log(distances[i])
                        robot.log(enemies[i])
                        if combat_utility.is_attackable_enemy_unit(robot, enemies[i], distances[i]) == 1:
                                return check.attack_check(robot, enemies[i].x - robot.me.x, enemies[i].y - robot.me.y, 500)

        destination = robot.current_move_destination
        move_dir = pathfinding.bug_walk_toward(robot, destination)
        return check.move_check(robot, move_dir[0], move_dir[1], 123)

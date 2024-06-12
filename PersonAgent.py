import numpy as np
import random

from Coordinate import Coordinate
from Settings import *
from State import State, LiftState, PersonType
import Utils

class Target:
    queue_grid = [
        "..xx..xx..",
        "...x...x..",
        "...x...x..",
        "xxxxxxxxxx",
        "...x...x..",
        "...x...x..",
        "..xx..xx.."
    ]
    @staticmethod
    def StairsUpQueue(floor):
        return [np.array([Coordinate.StairsUp(floor).x - 3, Coordinate.StairsUp(floor).y2])]
    @staticmethod
    def StairsDownQueue(floor):
        return [np.array([Coordinate.StairsDown(floor).x - 3, Coordinate.StairsDown(floor).y2])]
    @staticmethod
    def StairsUpRoute(floor):
        return [
            np.array([Coordinate.StairsUp(floor).x - 2, Coordinate.StairsUp(floor).y2]),
            np.array([Coordinate.StairsBetween(floor).x, Coordinate.StairsUp(floor).y2]),
            np.array([Coordinate.StairsBetween(floor).x, Coordinate.StairsDown(floor+1).y]),
            np.array([Coordinate.StairsDown(floor+1).x - 2, Coordinate.StairsDown(floor+1).y])
        ]
    @staticmethod
    def StairsDownRoute(floor):
        return [
            np.array([Coordinate.StairsDown(floor).x - 1, Coordinate.StairsDown(floor).y2]),
            np.array([Coordinate.StairsBetween(floor-1).x + 1, Coordinate.StairsDown(floor).y2]),
            np.array([Coordinate.StairsBetween(floor-1).x + 1, Coordinate.StairsUp(floor-1).y]),
            np.array([Coordinate.StairsUp(floor-1).x - 1, Coordinate.StairsUp(floor-1).y])
        ]
    @staticmethod
    def LiftQueue(floor, lifts, grid, gridLiftQueue):
        possible_queues = []
        for y in range(hall_height):
            for x in range(lift_hall_width):
                queue_pos = np.array([Coordinate.LiftHall(floor).x + x, Coordinate.LiftHall(floor).y + y])
                if not grid[Utils.key(queue_pos)] and Target.queue_grid[y][x] == "." and not gridLiftQueue.get(Utils.key(queue_pos), 0):
                    # if y == 0 and gridLiftQueue.get(Utils.key([queue_pos[0], queue_pos[1] + 1]), 0): continue
                    # if y == 1 and Target.queue_grid[y-1][x] == "." and not gridLiftQueue.get(Utils.key([queue_pos[0], queue_pos[1] - 1]), 0): continue
                    # if y == hall_height-1 and gridLiftQueue.get(Utils.key([queue_pos[0], queue_pos[1] - 1]), 0): continue
                    # if y == hall_height-2 and Target.queue_grid[y+1][x] == "." and not gridLiftQueue.get(Utils.key([queue_pos[0], queue_pos[1] + 1]), 0): continue
                    possible_queues.append(queue_pos)
        # Heuristic
        def f(queue):
            res = []
            for lift in range(lift_count):
                lift_door = Coordinate.LiftDoorOutsideInt(floor, lift)
                dist_pos = min(
                    Utils.norm(np.array([lift_door.x, lift_door.y]) - queue),
                    Utils.norm(np.array([lift_door.x+1, lift_door.y]) - queue)
                )
                dist_floor = abs(lifts[lift].floor - floor) + (0 if lifts[lift].floor == floor else floor_count if (lifts[lift].floor < floor) != lifts[lift].direction_up else 0)
                res.append((dist_pos + dist_floor, queue))
            return res
        if not possible_queues:
            return []
        dist_queues = sorted([dist_queue for queue in possible_queues for dist_queue in f(queue)], key=lambda x: x[0])
        best_dist = min(queue[0] for queue in dist_queues)
        best_queues = [queue for queue in dist_queues if queue[0] == best_dist]
        chosen_queue = random.choice(best_queues)
        gridLiftQueue[Utils.key(chosen_queue[1])] = 1
        return [
            np.array([Coordinate.LiftHall(floor).x2 + 1, Coordinate.LiftHall(floor).y + (hall_height-1)//2]),
            np.array([chosen_queue[1][0], Coordinate.LiftHall(floor).y + (hall_height-1)//2]),
            chosen_queue[1]
        ]
    @staticmethod
    def LiftQueueMove(pos, floor, target_lift, gridLiftQueue):
        coordinate = Coordinate.LiftHall(floor)
        relative_pos = np.array([coordinate.x, coordinate.y])
        door_pos = Target.LiftDoor(floor, target_lift)[0]
        possible_moves = []
        for move in Utils.adj(pos, True):
            condition_closer = Utils.norm(door_pos - move) < Utils.norm(door_pos - pos)
            condition_allowed = Utils.inside(move - relative_pos, [0, lift_hall_width-1], [0, hall_height-1]) and Target.queue_grid[move[1] - relative_pos[1]][move[0] - relative_pos[0]] != 'x'
            condition_empty = not gridLiftQueue.get(Utils.key(move), 0)
            condition_not_blocking = not gridLiftQueue.get(Utils.key(move + np.array([-1, 0] if move[1] - relative_pos[1] == 1 else [1, 0])), 0) if move[1] - relative_pos[1] == 1 or move[1] - relative_pos[1] == hall_height - 2 else True
            if condition_closer and condition_allowed and condition_empty and condition_not_blocking:
                possible_moves.append(move)
        if possible_moves:
            chosen_move = random.choice(possible_moves)
            return [chosen_move]
        return []
    @staticmethod
    def LiftExitRoute(pos, floor):
        return [
            np.array([pos[0], Coordinate.LiftHall(floor).y + hall_height//2]),
            np.array([Coordinate.LiftHall(floor).x2 + 1, Coordinate.LiftHall(floor).y + hall_height//2])
        ]
    @staticmethod
    def LiftDoor(floor, lift):
        coordinate = Coordinate.LiftDoorOutsideInt(floor, lift)
        return [np.array([coordinate.x, coordinate.y])]

class PersonAgent:
    def __init__(self, start_time, pos, current_floor, target_floor, target_floor_pos, person_type):
        self.start_time = start_time
        self.pos = pos
        self.grid_pos = pos
        self.current_floor = current_floor
        self.target_floor = target_floor
        self.target_floor_pos = target_floor_pos
        self.speed = 0.5
        
        self.finish_time = None
        self.target_pos = []
        self.state = State.start
        self.target_lift = None

        self.person_type = person_type

        # To debug stuck
        # self.stuck = 0
    
    def step(self, time, grid, lifts, gridLiftQueue, pressedLiftButton):
        if self.finish_time: return

        if self.person_type == PersonType.returning and self.pos[1] <= Coordinate.FirstFloorHall().y2 - first_floor_hall_height/2:
            self.finish_time = time
            return

        # Set target
        if not self.target_pos:
            if self.current_floor == self.target_floor:
                if Utils.equal_pos(self.pos, self.target_floor_pos):
                    self.finish_time = time
                    return
                else: self.target_pos = [self.target_floor_pos]
            elif self.state == State.start:
                self.state = State.lift_queue
                self.target_pos = Target.LiftQueue(self.current_floor, lifts, grid, gridLiftQueue)
                if self.target_pos:
                    best_lift = min((Utils.norm(self.target_pos[-1] - Target.LiftDoor(self.current_floor, i)[0]), i) for i in range(lift_count))
                    self.target_lift = best_lift[1]
                else:
                    self.state = State.stairs_queue
                    self.target_pos = Target.StairsUpQueue(self.current_floor) if self.target_floor > self.current_floor else Target.StairsDownQueue(self.current_floor)
            elif self.state == State.lift_queue:
                target_lift = lifts[self.target_lift]
                pressedLiftButton[self.current_floor][self.target_lift][1 if self.target_floor > self.current_floor else 0] = True
                # Problem: kalau yang di belakang antrian masuk mau masuk duluan
                door_coordinate = Coordinate.LiftDoorOutsideInt(self.current_floor, self.target_lift)
                door_pos = np.array([door_coordinate.x, door_coordinate.y])
                up = (door_pos[1] == Coordinate.LiftHall(self.current_floor).y2)
                condition_nearest_to_door = np.any([Utils.equal_pos(self.grid_pos, door_pos + np.array(pos)) for pos in [[-1, 0], [2, 0], [0, -1 if up else 1]]])
                condition_lift_open = target_lift.floor == self.current_floor and target_lift.state == LiftState.open
                condition_lift_not_full = target_lift.person_count < lift_max_person
                condition_lift_no_leaving = not np.any([person and person.state == State.lift_inside_leaving for person in target_lift.grid.values()])
                condition_lift_direction = enter_lift_wrong_direction or (self.target_floor > self.current_floor) == target_lift.direction_up
                if condition_nearest_to_door and condition_lift_open and condition_lift_not_full and condition_lift_no_leaving and condition_lift_direction:
                    target_lift.person_count += 1
                    self.state = State.lift_entering
                    self.target_pos = Target.LiftDoor(self.current_floor, self.target_lift)
                    gridLiftQueue[Utils.key(self.grid_pos)] = 0
                else:
                    queue_move = Target.LiftQueueMove(self.grid_pos, self.current_floor, self.target_lift, gridLiftQueue)
                    if queue_move:
                        self.target_pos.append(queue_move[0])
                        gridLiftQueue[Utils.key(queue_move[0])] = 1
                        gridLiftQueue[Utils.key(self.grid_pos)] = 0
            elif self.state == State.lift_entering:
                if not lifts[self.target_lift].grid[Utils.key([0, 1])]:
                    self.state = State.lift_inside_entering
                    grid[Utils.key(self.pos)] = None
                    self.pos = Coordinate.LiftGrid(self.target_lift, lifts[self.target_lift].y, 0, 1)
                    self.grid_pos = np.array([0, 1])
                    lifts[self.target_lift].grid[Utils.key([0, 1])] = self
                    lifts[self.target_lift].last_time = max(lifts[self.target_lift].last_time, time)
            elif self.state == State.stairs_queue:
                if self.target_floor > self.current_floor:
                    self.state = State.stairs_up
                    self.target_pos = Target.StairsUpRoute(self.current_floor)
                    self.current_floor += 1
                else:
                    if not grid[Utils.key([self.grid_pos[0]+2, self.grid_pos[1]+1])] and not grid[Utils.key([self.grid_pos[0]+1, self.grid_pos[1]-1])]:
                        self.state = State.stairs_down
                        self.target_pos = Target.StairsDownRoute(self.current_floor)
                        self.current_floor -= 1
            elif self.state == State.stairs_up:
                self.target_pos = Target.StairsUpRoute(self.current_floor)
                self.current_floor += 1
            elif self.state == State.stairs_down:
                self.target_pos = Target.StairsDownRoute(self.current_floor)
                self.current_floor -= 1

        # Move to target
        disable_collision = [State.lift_queue]
        if self.target_pos:
            if self.state in disable_collision:
                grid[Utils.key(self.grid_pos)] = None
                grid[Utils.key(self.target_pos[0])] = self
                self.pos = Utils.move(self.pos, self.target_pos[0], self.speed)
                if Utils.equal_pos(self.pos, self.target_pos[0]):
                    self.grid_pos = self.target_pos[0]
                    self.target_pos = self.target_pos[1:]
            else:
                if Utils.equal_pos(self.pos, self.grid_pos):
                    grid[Utils.key(self.grid_pos)] = None
                    possible_moves = [move for move in Utils.adj(self.grid_pos, True) if not grid.get(Utils.key(move), 1)]
                    dist_moves = sorted([(Utils.norm(self.target_pos[0] - move), move) for move in possible_moves], key=lambda x: x[0])
                    best_dist = min(move[0] for move in dist_moves)
                    best_moves = [move[1] for move in dist_moves if move[0] == best_dist]
                    self.grid_pos = random.choice(best_moves)
                    # To debug stuck
                    # if Utils.equal_pos(self.grid_pos, self.pos):
                    #     self.stuck += 1
                    # else:
                    #     self.stuck = 0
                    # if self.stuck > 20:
                    #     print(self.pos, self.target_pos[0], dist_moves)
                    #     print([(move, grid.get(Utils.key(move), 1)) for move in moves])
                    grid[Utils.key(self.grid_pos)] = self
                self.pos = Utils.move(self.pos, self.grid_pos, self.speed)
                if Utils.equal_pos(self.pos, self.target_pos[0]):
                    self.target_pos = self.target_pos[1:]
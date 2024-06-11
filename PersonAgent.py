import numpy as np
import random

from Coordinate import Coordinate
from Settings import *
from State import State, LiftState
import Utils

class Target:
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
        queue_grid = [
            "..xx..xx..",
            "...x...x..",
            "xxxxxxxxxx",
            "xxxxxxxxxx",
            "...x...x..",
            "..xx..xx.."
        ]
        possible_queues = []
        for y in range(hall_height):
            for x in range(lift_hall_width):
                queue_pos = np.array([Coordinate.LiftHall(floor).x + x, Coordinate.LiftHall(floor).y + y])
                if not grid[Utils.key(queue_pos)] and queue_grid[y][x] == "." and not gridLiftQueue.get(Utils.key(queue_pos), 0):
                    if y == 0 and gridLiftQueue.get(Utils.key([queue_pos[0], queue_pos[1] + 1]), 0): continue
                    if y == hall_height-1 and gridLiftQueue.get(Utils.key([queue_pos[0], queue_pos[1] - 1]), 0): continue
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
                res.append((dist_pos + dist_floor, queue, lift))
            return res
        if not possible_queues:
            return [], None
        dist_queues = sorted([dist_queue for queue in possible_queues for dist_queue in f(queue)], key=lambda x: x[0])
        best_dist = min(queue[0] for queue in dist_queues)
        best_queues = [queue for queue in dist_queues if queue[0] == best_dist]
        chosen_queue = random.choice(best_queues)
        gridLiftQueue[Utils.key(chosen_queue[1])] = 1
        return [
            np.array([Coordinate.LiftHall(floor).x2 + 1, Coordinate.LiftHall(floor).y + 2]),
            np.array([chosen_queue[1][0], Coordinate.LiftHall(floor).y + 2]),
            chosen_queue[1]
        ], chosen_queue[2]
    @staticmethod
    def LiftExitRoute(pos, floor):
        return [
            np.array([pos[0], Coordinate.LiftHall(floor).y + 3]),
            np.array([Coordinate.LiftHall(floor).x2 + 1, Coordinate.LiftHall(floor).y + 3])
        ]
    @staticmethod
    def LiftDoor(floor, lift):
        coordinate = Coordinate.LiftDoorOutsideInt(floor, lift)
        return [np.array([coordinate.x, coordinate.y])]

class PersonAgent:
    def __init__(self, start_time, pos, current_floor, target_floor, target_floor_pos):
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

        # To debug stuck
        # self.stuck = 0
    
    def step(self, time, grid, lifts, gridLiftQueue, pressedLiftButton):
        if self.finish_time: return

        # Set target
        if not self.target_pos:
            if self.current_floor == self.target_floor:
                if Utils.equal_pos(self.pos, self.target_floor_pos):
                    self.finish_time = time
                    return
                else: self.target_pos = [self.target_floor_pos]
            elif self.state == State.start:
                self.state = State.lift_queue
                self.target_pos, self.target_lift = Target.LiftQueue(self.current_floor, lifts, grid, gridLiftQueue)
                if not self.target_pos:
                    self.state = State.stairs_queue
                    self.target_pos = Target.StairsUpQueue(self.current_floor) if self.target_floor > self.current_floor else Target.StairsDownQueue(self.current_floor)
            elif self.state == State.lift_queue:
                target_lift = lifts[self.target_lift]
                pressedLiftButton[self.current_floor][self.target_lift][self.target_floor > self.current_floor] = True
                if target_lift.floor == self.current_floor and target_lift.state == LiftState.open and target_lift.person_count < lift_max_person and not np.any([person and person.state == State.lift_inside_leaving for person in target_lift.grid.values()]):
                    target_lift.person_count += 1
                    self.state = State.lift_entering
                    self.target_pos = Target.LiftDoor(self.current_floor, self.target_lift)
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
        if self.target_pos:
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
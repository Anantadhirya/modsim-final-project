import numpy as np
import random

from Coordinate import Coordinate
from Settings import *
from State import State
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
            "...x...x..",
            "..xx..xx.."
        ]
        possible_queues = []
        for y in range(hall_height):
            for x in range(lift_hall_width):
                queue_pos = np.array([Coordinate.LiftHall(floor).x + x, Coordinate.LiftHall(floor).y + y])
                if not grid.get(Utils.key(queue_pos), 1) and queue_grid[y][x] == "." and not gridLiftQueue.get(Utils.key(queue_pos), 0):
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
                dist_floor = abs(lifts[lift].floor - floor)
                res.append(dist_pos + dist_floor)
            return min(res)
        if not possible_queues:
            return []
        dist_queues = sorted([(f(queue), queue) for queue in possible_queues], key=lambda x: x[0])
        best_dist = min(queue[0] for queue in dist_queues)
        best_queues = [queue[1] for queue in dist_queues if queue[0] == best_dist]
        chosen_queue = random.choice(best_queues)
        gridLiftQueue[Utils.key(chosen_queue)] = 1
        return [
            np.array([Coordinate.LiftHall(floor).x2 + 1, Coordinate.LiftHall(floor).y + 2]),
            np.array([chosen_queue[0], Coordinate.LiftHall(floor).y + 2]),
            chosen_queue
        ]

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

        # To debug stuck
        # self.stuck = 0
    
    def step(self, time, grid, lifts, gridLiftQueue):
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
                self.target_pos = Target.LiftQueue(self.current_floor, lifts, grid, gridLiftQueue)
                if not self.target_pos:
                    self.state = State.stairs_queue
                    self.target_pos = Target.StairsUpQueue(self.current_floor) if self.target_floor > self.current_floor else Target.StairsDownQueue(self.current_floor)
            elif self.state == State.stairs_queue:
                if self.target_floor > self.current_floor:
                    self.state = State.stairs_up
                    self.target_pos = Target.StairsUpRoute(self.current_floor)
                    self.current_floor += 1
                else:
                    if not grid.get(Utils.key([self.grid_pos[0]+2, self.grid_pos[1]+1]), 1) and not grid.get(Utils.key([self.grid_pos[0]+1, self.grid_pos[1]-1]), 1):
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
                grid[Utils.key(self.grid_pos)] = 0
                moves = [self.pos + np.array(d) for d in [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]]
                possible_moves = [move for move in moves if not grid.get(Utils.key(move), 1)]
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
                grid[Utils.key(self.grid_pos)] = 1
            self.pos = Utils.move(self.pos, self.grid_pos, self.speed)
            if Utils.equal_pos(self.pos, self.target_pos[0]):
                self.target_pos = self.target_pos[1:]
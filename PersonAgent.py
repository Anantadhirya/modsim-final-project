import numpy as np
import random

from Coordinate import Coordinate
from Settings import *
from State import State, forbidden_grid
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
    
    def step(self, time, grid):
        if self.finish_time: return

        # Set target
        if not self.target_pos:
            if self.current_floor == self.target_floor:
                if Utils.equal_pos(self.pos, self.target_floor_pos):
                    self.finish_time = time
                    return
                else: self.target_pos = [self.target_floor_pos]
            elif self.state == State.start:
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
                possible_moves = [move for move in moves if not grid.get(Utils.key(move), 1) and not forbidden_grid.get(self.state, {}).get(Utils.key(move), 0)]
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
                #     print([(move, not grid.get(Utils.key(move), 1), not forbidden_grid.get(self.state, {}).get(Utils.key(move), 0)) for move in moves])
                grid[Utils.key(self.grid_pos)] = 1
            self.pos = Utils.move(self.pos, self.grid_pos, self.speed)
            if Utils.equal_pos(self.pos, self.target_pos[0]):
                self.target_pos = self.target_pos[1:]
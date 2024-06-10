import numpy as np
import random

from Coordinate import Coordinate
from Settings import *
import Utils

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
    
    def step(self, time):
        if self.finish_time: return
        if not self.target_pos:
            if self.target_floor > self.current_floor:
                self.target_pos = [
                    np.array([Coordinate.StairsUp(self.current_floor).x - 2, Coordinate.StairsUp(self.current_floor).y2]),
                    np.array([Coordinate.StairsBetween(self.current_floor).x, Coordinate.StairsUp(self.current_floor).y2]),
                    np.array([Coordinate.StairsBetween(self.current_floor).x, Coordinate.StairsDown(self.current_floor+1).y]),
                    np.array([Coordinate.StairsDown(self.current_floor+1).x - 2, Coordinate.StairsDown(self.current_floor+1).y])
                ]
                self.current_floor += 1
            elif self.target_floor < self.current_floor:
                self.target_pos = [
                    np.array([Coordinate.StairsDown(self.current_floor).x - 1, Coordinate.StairsDown(self.current_floor).y2]),
                    np.array([Coordinate.StairsBetween(self.current_floor-1).x + 1, Coordinate.StairsDown(self.current_floor).y2]),
                    np.array([Coordinate.StairsBetween(self.current_floor-1).x + 1, Coordinate.StairsUp(self.current_floor-1).y]),
                    np.array([Coordinate.StairsUp(self.current_floor-1).x - 1, Coordinate.StairsUp(self.current_floor-1).y])
                ]
                self.current_floor -= 1
            else:
                if Utils.equal_pos(self.pos, self.target_floor_pos):
                    self.finish_time = time
                    return
                else: self.target_pos = [self.target_floor_pos]
        if Utils.equal_pos(self.pos, self.grid_pos):
            possible_moves = [self.pos + np.array(d) for d in [[1, 0], [-1, 0], [0, 1], [0, -1]]]
            dist_moves = sorted([(Utils.norm(self.target_pos[0] - move), move) for move in possible_moves if Coordinate.inside_building(move)], key=lambda x: x[0])
            best_dist = min(move[0] for move in dist_moves)
            best_moves = [move[1] for move in dist_moves if move[0] == best_dist]
            self.grid_pos = random.choice(best_moves)
        self.pos = Utils.move(self.pos, self.grid_pos, self.speed)
        if Utils.equal_pos(self.pos, self.target_pos[0]):
            self.target_pos = self.target_pos[1:]
import numpy as np

from Coordinate import Coordinate
from Settings import *
import Utils

class PersonAgent:
    def __init__(self, start_time, pos, current_floor, target_floor, target_floor_pos):
        self.start_time = start_time
        self.pos = pos
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
                    np.array([Coordinate.StairsUp(self.current_floor).x - person_size, Coordinate.StairsUp(self.current_floor).y2 - person_size]),
                    np.array([Coordinate.StairsBetween(self.current_floor).x + person_size, Coordinate.StairsUp(self.current_floor).y2 - person_size]),
                    np.array([Coordinate.StairsBetween(self.current_floor).x + person_size, Coordinate.StairsDown(self.current_floor+1).y + person_size]),
                    np.array([Coordinate.StairsDown(self.current_floor+1).x - 3*person_size, Coordinate.StairsDown(self.current_floor+1).y + person_size])
                ]
                self.current_floor += 1
            elif self.target_floor < self.current_floor:
                self.target_pos = [
                    np.array([Coordinate.StairsDown(self.current_floor).x - person_size, Coordinate.StairsDown(self.current_floor).y2 - person_size]),
                    np.array([Coordinate.StairsBetween(self.current_floor-1).x + 3*person_size, Coordinate.StairsDown(self.current_floor).y2 - person_size]),
                    np.array([Coordinate.StairsBetween(self.current_floor-1).x + 3*person_size, Coordinate.StairsUp(self.current_floor-1).y + person_size]),
                    np.array([Coordinate.StairsUp(self.current_floor-1).x - person_size, Coordinate.StairsUp(self.current_floor-1).y + person_size])
                ]
                self.current_floor -= 1
            else:
                if Utils.equal_pos(self.pos, self.target_floor_pos):
                    self.finish_time = time
                    return
                else: self.target_pos = [self.target_floor_pos]
        self.pos = Utils.move(self.pos, self.target_pos[0], self.speed)
        if Utils.equal_pos(self.pos, self.target_pos[0]): self.target_pos = self.target_pos[1:]
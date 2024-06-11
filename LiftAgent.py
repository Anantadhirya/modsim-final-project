from State import LiftState
from Coordinate import Coordinate
import Utils

import numpy as np
import random

class LiftAgent:
    priority = [
        "1012",
        "2123",
        "3234",
        "4345"
    ]
    def __init__(self, lift_number):
        self.lift_number = lift_number
        self.y = 0
        self.floor = 0
        self.state = LiftState.open
        self.person_count = 0
        self.grid = {Utils.key([i, j]): None for i in range(4) for j in range(4)}
    
    def step(self):
        if self.grid[Utils.key([0, 1])]:
            possible_move_tos = [np.array([i, j]) for i in range(4) for j in range(4) if not self.grid[Utils.key([i, j])]]
            random.shuffle(possible_move_tos)
            possible_move_tos.sort(key=lambda pos: self.priority[pos[0]][pos[1]], reverse=True)
            for move_to in possible_move_tos:
                move_froms = [move_to + np.array(d) for d in [[1, 0], [-1, 0], [0, 1], [0, -1]]]
                possible_froms = [move_from for move_from in move_froms if self.grid.get(Utils.key(move_from), None) and self.priority[move_from[0]][move_from[1]] < self.priority[move_to[0]][move_to[1]]]
                if possible_froms:
                    chosen_from = random.choice(possible_froms)
                    self.grid[Utils.key(chosen_from)].grid_pos = move_to
                    self.grid[Utils.key(move_to)] = self.grid[Utils.key(chosen_from)]
                    self.grid[Utils.key(chosen_from)] = None
        for person in self.grid.values():
            if not person: continue
            actual_pos = Coordinate.LiftGrid(self.lift_number, self.y, person.grid_pos[0], person.grid_pos[1])
            if not Utils.equal_pos(person.pos, actual_pos):
                person.pos = Utils.move(person.pos, actual_pos, person.speed)
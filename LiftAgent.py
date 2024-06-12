from State import State, LiftState
from Coordinate import Coordinate
import Utils
from Settings import *
from PersonAgent import Target

import numpy as np
import random

class LiftAgent:
    priority = [
        "2105",
        "3234",
        "4345",
        "5456"
    ]
    def __init__(self, time, lift_number):
        self.lift_number = lift_number
        self.y = 0
        self.floor = 0
        self.state = LiftState.open
        self.direction_up = 1
        self.last_time = time
        self.person_count = 0
        self.grid = {Utils.key([i, j]): None for i in range(4) for j in range(4)}
        self.target = np.array([False for _ in range(floor_count)])
        self.speed = 0.5
    
    def actual_pos(self, grid_pos):
        return Coordinate.LiftGrid(self.lift_number, self.y, grid_pos[0], grid_pos[1])
    
    def correct_pos(self, pos):
        person = self.grid[Utils.key(pos)]
        return Utils.equal_pos(person.pos, self.actual_pos(person.grid_pos))
    
    def step(self, time, pressedLiftButton, grid):
        if self.state == LiftState.open:
            if pressedLiftButton[self.floor][self.lift_number][self.direction_up] and self.person_count < lift_max_person:
                pressedLiftButton[self.floor][self.lift_number][self.direction_up] = False
                self.last_time = time
            for person in self.grid.values():
                if person and person.target_floor != self.floor:
                    self.target[person.target_floor] = True
            for floor in range(floor_count):
                if floor != self.floor and np.any(pressedLiftButton[floor][self.lift_number]):
                    self.target[floor] = True
            self.target[self.floor] = False
            if self.person_count == 0 and not np.any(self.target):
                if self.floor != 0:
                    self.target[0] = True
                    self.state = LiftState.closing
                    self.last_time = time
            elif (time - self.last_time) > lift_stay_open_duration and np.any(self.target) and not np.any([person and person.target_floor == self.floor for person in self.grid.values()]):
                self.state = LiftState.closing
                self.last_time = time
        elif self.state == LiftState.closing:
            if (time - self.last_time) > lift_door_transition_duration:
                self.state = LiftState.closed
            elif pressedLiftButton[self.floor][self.lift_number][self.direction_up] and self.person_count < lift_max_person:
                pressedLiftButton[self.floor][self.lift_number][self.direction_up] = False
                self.state = LiftState.opening
                self.last_time = time - (lift_door_transition_duration - (time - self.last_time))
        elif self.state == LiftState.opening:
            if (time - self.last_time) > lift_door_transition_duration:
                self.state = LiftState.open
                self.last_time = time
        elif self.state == LiftState.closed:
            if self.direction_up and not np.any([self.target[floor] for floor in range(self.floor+1, floor_count)]):
                self.direction_up = 0
            elif not self.direction_up and not np.any([self.target[floor] for floor in range(0, self.floor)]):
                self.direction_up = 1
            if (pressedLiftButton[self.floor][self.lift_number][self.direction_up] and self.person_count < lift_max_person) or np.any([person and person.target_floor == self.floor for person in self.grid.values()]) or self.target[self.floor]:
                pressedLiftButton[self.floor][self.lift_number][self.direction_up] = False
                self.state = LiftState.opening
                self.last_time = time
            else:
                self.state = LiftState.moving
                self.floor += 1 if self.direction_up else -1
        elif self.state == LiftState.moving:
            if self.y == Coordinate.LiftHall(self.floor).y:
                self.state = LiftState.closed
                for person in self.grid.values():
                    if person and person.target_floor == self.floor:
                        person.state = State.lift_inside_leaving
            else:
                target_y = Coordinate.LiftHall(self.floor).y
                self.y = target_y if abs(target_y - self.y) < self.speed * time_step else self.y + self.speed * time_step * (1 if target_y > self.y else -1)
                for person in self.grid.values():
                    if not person: continue
                    person.pos = Coordinate.LiftGrid(self.lift_number, self.y, person.grid_pos[0], person.grid_pos[1])

        # Lift entrance
        if np.any([self.grid[Utils.key(pos)] and self.grid[Utils.key(pos)].state == State.lift_inside_entering for pos in [[0, 1], [0, 2]]]):
            possible_move_tos = [np.array([i, j]) for i in range(4) for j in range(4) if not self.grid[Utils.key([i, j])]]
            random.shuffle(possible_move_tos)
            possible_move_tos.sort(key=lambda pos: self.priority[pos[0]][pos[1]], reverse=True)
            for move_to in possible_move_tos:
                possible_froms = [move_from for move_from in Utils.adj(move_to) if self.grid.get(Utils.key(move_from), None) and self.priority[move_from[0]][move_from[1]] < self.priority[move_to[0]][move_to[1]] and self.correct_pos(move_from) and self.grid[Utils.key(move_from)].state == State.lift_inside_entering]
                if possible_froms:
                    chosen_from = random.choice(possible_froms)
                    self.grid[Utils.key(chosen_from)].grid_pos = move_to
                    self.grid[Utils.key(move_to)], self.grid[Utils.key(chosen_from)] = self.grid[Utils.key(chosen_from)], self.grid[Utils.key(move_to)]
        
        # Lift exit
        if self.state == LiftState.open:
            for person in self.grid.values():
                if not person or person.state != State.lift_inside_leaving or not Utils.equal_pos(person.pos, self.actual_pos(person.grid_pos)): continue
                possible_move = [move for move in Utils.adj(person.grid_pos) if Utils.inside(move, [0, 3], [0, 3]) and self.priority[move[0]][move[1]] < self.priority[person.grid_pos[0]][person.grid_pos[1]]]
                empty_move = [move for move in possible_move if self.grid[Utils.key(move)] == None]
                swappable_move = [move for move in possible_move if self.grid[Utils.key(move)] and self.grid[Utils.key(move)].state != State.lift_inside_leaving]
                if empty_move:
                    chosen_move = random.choice(empty_move)
                    self.grid[Utils.key(chosen_move)], self.grid[Utils.key(person.grid_pos)] = self.grid[Utils.key(person.grid_pos)], self.grid[Utils.key(chosen_move)]
                    self.grid[Utils.key(chosen_move)].grid_pos = chosen_move
                elif swappable_move:
                    chosen_move = random.choice(swappable_move)
                    other_person = self.grid[Utils.key(chosen_move)]
                    other_person.grid_pos, person.grid_pos = person.grid_pos, other_person.grid_pos
                    self.grid[Utils.key(other_person.grid_pos)], self.grid[Utils.key(person.grid_pos)] = self.grid[Utils.key(person.grid_pos)], self.grid[Utils.key(other_person.grid_pos)]
            person = self.grid[Utils.key([0, 2])]
            coordinate = Coordinate.LiftDoorOutsideInt(self.floor, self.lift_number)
            door_pos = np.array([coordinate.x2, coordinate.y])
            if person and person.state == State.lift_inside_leaving and not grid[Utils.key(door_pos)]:
                person.pos = person.grid_pos = door_pos
                person.state = State.lift_leaving
                person.target_pos = Target.LiftExitRoute(person.grid_pos, self.floor)
                person.current_floor = self.floor
                self.person_count -= 1
                self.last_time = time
                grid[Utils.key(person.grid_pos)] = person
                self.grid[Utils.key([0, 2])] = None

        
        # Lift automatic grid movement
        for person in self.grid.values():
            if not person: continue
            actual_pos = self.actual_pos(person.grid_pos)
            if not Utils.equal_pos(person.pos, actual_pos):
                person.pos = Utils.move(person.pos, actual_pos, person.speed)
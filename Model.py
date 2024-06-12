from PersonAgent import PersonAgent
from LiftAgent import LiftAgent
from ModelDisplay import ModelDisplay
from Coordinate import Coordinate
from Settings import *
from State import PersonType
from Insight import Insight

import Utils
import random
import numpy as np
import time

class Model:
    def __init__(self, person_arriving, arrive_params, classes_finished, classes_person_params, classes_finish_params, classes_empty_params, display = False, verbose = False):
        # Initialize Persons
        self.arrivingPersons = []
        self.persons = []
        self.arrivedPersons = []
        self.arrivingQueue = []
        self.grid = {}
        self.gridLiftQueue = {}
        self.pressedLiftButton = [[np.array([False, False]) for _ in range(lift_count)] for _ in range(floor_count)]
        self.model_finish = None
        self.insight = Insight()
        self.display = None
        self.verbose = verbose
        self.last_nodisplay_print_time = None
        self.total_person = 0

        for _ in range(person_arriving):
            arrive_time = Utils.normal(arrive_params) * 60
            pos = Utils.random_pos(Coordinate.Hall(0), (0, 2, 0, 0), "u")
            target_floor = random.randint(1, floor_count-1)
            target_pos = Utils.random_pos(Coordinate.Hall(target_floor), (0, 3, 0, 1), "u")
            self.arrivingPersons.append(PersonAgent(arrive_time, pos, 0, target_floor, target_pos, PersonType.arriving))
        
        random.shuffle(classes_position)
        for i in range(classes_finished):
            class_floor, class_room = classes_position[i]
            class_person_count = Utils.normal(classes_person_params)
            class_finish_time = Utils.normal(classes_finish_params) * 60
            for _ in range(round(class_person_count)):
                person_time = class_finish_time + Utils.normal(classes_empty_params) * 60
                person_pos = Utils.random_pos(Coordinate.Hall(class_floor), (0, 2, 0, 0), class_room)
                target_pos = Utils.random_pos(Coordinate.FirstFloorHall(), (0, 2, 0, 2), side="d")
                self.arrivingPersons.append(PersonAgent(person_time, person_pos, class_floor, 0, target_pos, PersonType.returning))

        self.startTime = min([person.start_time for person in self.arrivingPersons])
        self.arrivingPersons.sort(key=lambda person: person.start_time, reverse=True)

        self.total_person = len(self.arrivingPersons)

        # Initialize Lifts
        self.lifts = [LiftAgent(self.startTime, i) for i in range(lift_count)]

        self.init_building_grid()

        if display:
            self.display = ModelDisplay()
    
    def init_room_grid(self, room):
        for x in range(room.x, room.x + room.w):
            for y in range(room.y, room.y + room.h):
                self.grid[Utils.key([x, y])] = None

    def init_building_grid(self):
        self.init_room_grid(Coordinate.FirstFloorHall())
        for floor in range(floor_count):
            self.init_room_grid(Coordinate.LiftHall(floor))
            self.init_room_grid(Coordinate.Hall(floor))
            self.init_room_grid(Coordinate.StairsUp(floor))
            self.init_room_grid(Coordinate.StairsDown(floor))
        for floor in range(floor_count - 1):
            self.init_room_grid(Coordinate.StairsBetween(floor))

    def step(self):
        self.time += time_step
        # print(f"Time: {(self.time/60):.2f} menit")
        while self.arrivingPersons and self.arrivingPersons[-1].start_time <= self.time:
            self.arrivingQueue.append(self.arrivingPersons[-1])
            self.arrivingPersons.pop()
        
        tmp = []
        for person in self.arrivingQueue:
            if self.grid[Utils.key(person.pos)]:
                tmp.append(person)
            else:
                self.grid[Utils.key(person.pos)] = person
                self.persons.append(person)
        self.arrivingQueue = tmp
        
        for person in self.persons:
            person.step(self.time, self.grid, self.lifts, self.gridLiftQueue, self.pressedLiftButton)
            if person.finish_time:
                self.arrivedPersons.append(person)
                self.grid[Utils.key(person.grid_pos)] = None
        
        for lift in self.lifts:
            lift.step(self.time, self.pressedLiftButton, self.grid)

        self.persons = [person for person in self.persons if not person.finish_time]

    def run_simulation(self):
        self.time = self.startTime
        while True:
            self.step()

            if not self.model_finish and not self.arrivingPersons and not self.persons:
                self.model_finish = self.time
            if self.model_finish and (self.time - self.model_finish) > time_before_display_close:
                break

            if self.display:
                self.display.redraw(self.persons, self.lifts, self.time, self.gridLiftQueue)
            if self.verbose:
                current_time = time.time()
                if not self.last_nodisplay_print_time or (current_time - self.last_nodisplay_print_time) > time_verbose_print:
                    self.last_nodisplay_print_time = current_time
                    print(f"Progress: {len(self.arrivedPersons)}/{self.total_person} ({(len(self.arrivedPersons)/self.total_person*100):.2f}%)")

        # After simulation finish
        for person in self.arrivedPersons:
            self.insight.person_total_time[person.use_lift][person.start_floor] += (person.finish_time - person.start_time)
            self.insight.person_count[person.use_lift][person.start_floor] += 1
            if person.use_lift:
                self.insight.list_lift_wait_time.append(person.lift_wait_finish_time - person.lift_wait_start_time)
        self.insight.display()
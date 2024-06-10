from PersonAgent import PersonAgent
from LiftAgent import LiftAgent
from ModelDisplay import ModelDisplay
from Coordinate import Coordinate
from Settings import *
import Utils
import random

class Model:
    def __init__(self, person_arriving, early_params, classes_finished, classes_person_params, classes_finish_params, classes_empty_params, display = False):
        # Initialize Persons
        self.arrivingPersons = []
        self.persons = []

        for _ in range(person_arriving):
            arrive_time = Utils.normal(early_params) * 60
            pos = Utils.random_pos(Coordinate.Hall(0), person_size)
            target_floor = random.randint(1, floor_count-1)
            target_pos = Utils.random_pos(Coordinate.Hall(target_floor), person_size, "y")
            self.arrivingPersons.append(PersonAgent(arrive_time, pos, 0, target_floor, target_pos))
        
        random.shuffle(classes_position)
        for i in range(classes_finished):
            class_floor, class_room = classes_position[i]
            class_person_count = Utils.normal(classes_person_params)
            class_finish_time = Utils.normal(classes_finish_params) * 60
            for _ in range(round(class_person_count)):
                person_time = class_finish_time + Utils.uniform(classes_empty_params) * 60
                print(class_finish_time, person_time)
                person_pos = Utils.random_pos(Coordinate.Hall(class_floor), person_size, class_room)
                target_pos = Utils.random_pos(Coordinate.Hall(0), person_size)
                self.arrivingPersons.append(PersonAgent(person_time, person_pos, class_floor, 0, target_pos))

        self.startTime = min([person.arrive_time for person in self.arrivingPersons])
        self.arrivingPersons.sort(key=lambda person: person.arrive_time, reverse=True)

        self.lifts = [LiftAgent() for _ in range(lift_count)]
        if display:
            self.display = ModelDisplay()

    def step(self):
        self.time += time_step
        print(f"Time: {(self.time/60):.2f} menit")

        while self.arrivingPersons and self.arrivingPersons[-1].arrive_time <= self.time:
            self.persons.append(self.arrivingPersons[-1])
            self.arrivingPersons.pop()
        pass

    def run_simulation(self):
        self.time = self.startTime
        while True:
            self.step()
            if self.display:
                self.display.redraw(self.persons)
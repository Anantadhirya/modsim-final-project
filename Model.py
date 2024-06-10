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
            arrive_time = Utils.normal(early_params)
            pos = Utils.random_pos(Coordinate.Hall(0), person_size)
            target_floor = random.randint(1, floor_count-1)
            target_pos = Utils.random_pos(Coordinate.Hall(target_floor), person_size)
            self.arrivingPersons.append(PersonAgent(arrive_time, pos, 0, target_floor, target_pos))

        self.lifts = [LiftAgent() for _ in range(lift_count)]
        if display:
            self.display = ModelDisplay()

    def step(self):
        pass

    def run_simulation(self):
        while True:
            self.step()
            if self.display:
                self.display.redraw(self.persons)
from PersonAgent import PersonAgent
from LiftAgent import LiftAgent
from ModelDisplay import ModelDisplay
from Coordinate import Coordinate
from Settings import *
import Utils

class Model:
    def __init__(self, N, display = False):
        self.persons = [PersonAgent(Utils.randomPos(Coordinate.Hall(0), person_size)) for _ in range(N)]
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
from PersonAgent import PersonAgent
from LiftAgent import LiftAgent
from Settings import *

class Model:
    def __init__(self, N):
        self.listPerson = [PersonAgent() for _ in range(N)]
        self.listLift = [LiftAgent() for _ in range(lift_count)]
        print("Model initialized")

    def step(self):
        pass
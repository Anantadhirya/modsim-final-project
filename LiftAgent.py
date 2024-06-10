class State:
    open = 0
    up = 1
    down = 2

class LiftAgent:
    def __init__(self):
        self.y = 0
        self.floor = 0
        self.state = State.open
    
    def step(self):
        pass
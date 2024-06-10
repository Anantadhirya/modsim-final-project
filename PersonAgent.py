class PersonAgent:
    def __init__(self, arrive_time, pos, current_floor, target_floor, target_floor_pos):
        self.arrive_time = arrive_time
        self.pos = pos
        self.current_floor = current_floor
        self.target_floor = target_floor
        self.target_floor_pos = target_floor_pos
    
    def step(self):
        pass
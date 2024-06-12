from Settings import *

class Insight:
    def __init__(self):
        # 1 = lift
        self.person_total_time = [[0 for _ in range(floor_count)] for _ in range(2)]
        self.person_count = [[0 for _ in range(floor_count)] for _ in range(2)]
        self.list_lift_wait_time = []
    def person_time_average(self, lift = 0):
        total = 0
        cnt = 0
        for floor in range(floor_count):
            total += self.person_total_time[1 if lift else 0][floor]
            cnt += self.person_count[1 if lift else 0][floor]
        return total / cnt
    def percentage_choice(self, lift = 0):
        cnt_stairs = sum(self.person_count[0])
        cnt_lift = sum(self.person_count[1])
        cnt = cnt_stairs + cnt_lift
        return cnt_lift / cnt if lift else cnt_stairs / cnt
    def display(self):
        print(f"Average time (stairs) = {self.person_time_average(0)}")
        print(f"Average time (lift) = {self.person_time_average(1)}")
        print(f"Percentage (stairs : lift) = {self.percentage_choice(0)} : {self.percentage_choice(1)}")
        print(f"Average lift wait time: {sum(self.list_lift_wait_time) / len(self.list_lift_wait_time)}")

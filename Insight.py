from Settings import *
import Utils

import pandas as pd

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
        print(f"Average time (stairs) = {Utils.time_string(self.person_time_average(0))}")
        print(f"Average time (lift) = {Utils.time_string(self.person_time_average(1))}")
        print(f"Average lift wait time: {Utils.time_string(sum(self.list_lift_wait_time) / len(self.list_lift_wait_time))}")
        print(f"Percentage (stairs : lift) = {self.percentage_choice(0):.2f} : {self.percentage_choice(1):.2f}")
        print(f"Average time by floor (stairs) =", [Utils.time_string(self.person_total_time[0][floor] / self.person_count[0][floor]) if self.person_count[0][floor] else "-" for floor in range(floor_count)])
        print(f"Average time by floor (lift) =", [Utils.time_string(self.person_total_time[1][floor] / self.person_count[1][floor]) if self.person_count[1][floor] else "-" for floor in range(floor_count)])
    @staticmethod
    def insights_to_csv(insights):
        result1_df = pd.DataFrame([{"avg_stairs": insight.person_time_average(0), "avg_lift": insight.person_time_average(1)} for insight in insights])
        result1_df.to_csv('insights1.csv', index=False)

        result_total = [[0 for _ in range(floor_count)] for _ in range(2)]
        result_count = [[0 for _ in range(floor_count)] for _ in range(2)]
        for insight in insights:
            for i in range(2):
                for floor in range(floor_count):
                    result_total[i][floor] += insight.person_total_time[i][floor]
                    result_count[i][floor] += insight.person_count[i][floor]
        result_avg = [[result_total[i][floor] / result_count[i][floor] if result_count[i][floor] else None for floor in range(floor_count)] for i in range(2)]
        result2_df = pd.DataFrame([{"avg_stairs": result_avg[0][floor], "avg_lift": result_avg[1][floor]} for floor in range(floor_count)])
        result2_df.to_csv('insights2.csv', index=False)

        result_wait_time = []
        for insight in insights:
            for wait_time in insight.list_lift_wait_time:
                result_wait_time.append(wait_time)
        result3_df = pd.DataFrame([{"wait_time": wait_time} for wait_time in result_wait_time])
        result3_df.to_csv('insights3.csv', index=False)
        

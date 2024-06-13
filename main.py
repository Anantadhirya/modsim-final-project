from Model import Model
from Insight import Insight

# To run multiple simulations
# simulation_count = 20
# insights = []
# for i in range(simulation_count):
#     print(f"Running simulation {i}")
#     model = Model(600, [-0.097, 14.029], 8, [83.70, 23.89], [-17.083, 7.683], [5, 2], False, True)
#     model.run_simulation()
#     insights.append(model.insight)
# Insight.insights_to_csv(insights)

# To run a single simulation with display
model = Model(600, [-0.097, 14.029], 8, [83.70, 23.89], [-17.083, 7.683], [5, 2], True)
model.run_simulation()
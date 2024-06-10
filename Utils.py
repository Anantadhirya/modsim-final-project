import random
import numpy as np
import math

def random_between(l, r):
    return random.random() * (r-l) + l

def random_pos(room, margin = 0):
    return np.array([random_between(room.x + margin, room.x2 - margin), random_between(room.y + margin, room.y2 - margin)])

def normal(normal_params):
    mu = normal_params[0]
    sigma = normal_params[1]

    # Box-Muller-Gauss Method
    a = 2*math.pi*random.random()
    b = sigma*math.sqrt(-2*math.log(random.random()))
    return b * math.sin(a) + mu
import random
import numpy as np
import math

def random_between(l, r):
    return random.random() * (r-l) + l

def random_pos(room, margin = 0, side = ""):
    x, x2, y, y2 = room.x + margin, room.x2 - margin, room.y + margin, room.y2 - margin
    if side == "y":
        y = y2 = random.choice([y, y2])
    elif side == "x":
        x = x2 = random.choice([x, x2])
    elif side == "l":
        x2 = x
    elif side == "r":
        x = x2
    elif side == "u":
        y = y2
    elif side == "d":
        y2 = y
    return np.array([random_between(x, x2), random_between(y, y2)])

def normal(normal_params):
    mu = normal_params[0]
    sigma = normal_params[1]

    # Box-Muller-Gauss Method
    a = 2*math.pi*random.random()
    b = sigma*math.sqrt(-2*math.log(random.random()))
    return b * math.sin(a) + mu
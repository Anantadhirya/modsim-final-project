import random
import numpy as np
import math

from Settings import *

# Random Utils
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
    return np.array([random.randint(x, x2), random.randint(y, y2)])

def normal(normal_params):
    mu = normal_params[0]
    sigma = normal_params[1]

    # Box-Muller-Gauss Method
    a = 2*math.pi*random.random()
    b = sigma*math.sqrt(-2*math.log(random.random()))
    return b * math.sin(a) + mu

def uniform(uniform_params):
    return random_between(uniform_params[0], uniform_params[1])

# Vector Utils
def norm(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def normalize(v):
    return v / norm(v)

def move(pos, target, speed):
    direction = normalize(target - pos)
    return target if norm(target - pos) < speed * time_step else pos + direction * speed * time_step

def equal_pos(a, b):
    return norm(a-b) < 0.001
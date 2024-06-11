import random
import numpy as np
import math

from Settings import *

# Random Utils
def random_between(l, r):
    return random.random() * (r-l) + l

def random_pos(room, margin = (0, 0, 0, 0), side = ""):
    x, x2, y, y2 = room.x + margin[3], room.x2 - margin[1], room.y + margin[2], room.y2 - margin[0]
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

def equal_pos(a, b, tolerance = 0.001):
    return norm(a-b) < tolerance + 0.001

def key(pos):
    return (pos[0], pos[1])

def adj(pos, includeCenter = False):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    if includeCenter: directions.append([0, 0])
    return [pos + np.array(direction) for direction in directions]

def inside(pos, x_range, y_range):
    """Note: inclusive inside (x_range[0] <= pos[0] and pos[0] <= x_range[1] and y_range[0] <= pos[1] and pos[1] <= y_range[1])"""
    return x_range[0] <= pos[0] and pos[0] <= x_range[1] and y_range[0] <= pos[1] and pos[1] <= y_range[1]
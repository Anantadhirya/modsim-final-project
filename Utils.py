import random
import numpy as np

def random_between(l, r):
    return random.random() * (r-l) + l

def randomPos(room, margin = 0):
    return np.array([random_between(room.x + margin, room.x2 - margin), random_between(room.y + margin, room.y2 - margin)])
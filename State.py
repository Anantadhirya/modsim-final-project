class State:
    start = 0
    stairs_queue = 1
    stairs_up = 2
    stairs_down = 3

import Utils
from Settings import *
from Coordinate import Coordinate

forbidden_grid = {}
def set_room_grid(state, room):
    if state not in forbidden_grid:
        forbidden_grid[state] = {}
    for x in range(room.x, room.x + room.w):
        for y in range(room.y, room.y + room.h):
            forbidden_grid[Utils.key([x, y])] = 1
for floor in range(floor_count):
    forbidden_grid[State.stairs_queue] = {}
    set_room_grid(State.stairs_queue, Coordinate(Coordinate.Hall(floor).x2 - 2, Coordinate.Hall(floor).y, 2, Coordinate.Hall(floor).h))
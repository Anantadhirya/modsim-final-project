class State:
    start = 0
    lift_queue = 1
    lift_inside = 2
    stairs_queue = 3
    stairs_up = 4
    stairs_down = 5

import Utils
from Settings import *
from Coordinate import Coordinate

forbidden_grid = {}
def set_room_grid(state, room):
    if state not in forbidden_grid:
        forbidden_grid[state] = {}
    for x in range(room.x, room.x + room.w):
        for y in range(room.y, room.y + room.h):
            forbidden_grid[state][Utils.key([x, y])] = 1
            
for floor in range(floor_count):
    # Lift queue
    forbidden_grid[State.lift_queue] = {}
    grid = [
        "..xx..xx..",
        "..........",
        "...xxxxxxx",
        "..........",
        "..xx..xx.."
    ]
    for x in range(lift_hall_width):
        for y in range(hall_height):
            if grid[hall_height-1-y][x]:
                pos = Coordinate.LiftHall(floor)
                forbidden_grid[State.lift_queue][Utils.key([pos.x, pos.y])] = 1
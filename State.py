class State:
    start = 0
    lift_queue = 1
    lift_entering = 2
    lift_inside = 3
    stairs_queue = 4
    stairs_up = 5
    stairs_down = 6

class LiftState:
    open = 0
    up = 1
    down = 2
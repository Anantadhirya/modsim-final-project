class State:
    start = 0
    lift_queue = 1
    lift_entering = 2
    lift_inside_entering = 3
    lift_inside_leaving = 4
    lift_leaving = 5
    stairs_queue = 6
    stairs_up = 7
    stairs_down = 8

class LiftState:
    open = 0
    opening = 1
    closed = 2
    closing = 3
    moving = 4
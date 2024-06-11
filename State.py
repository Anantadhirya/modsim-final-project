class State:
    start = 0
    lift_press_button = 1
    lift_queue = 2
    lift_entering = 3
    lift_inside = 4
    stairs_queue = 5
    stairs_up = 6
    stairs_down = 7

class LiftState:
    open = 0
    opening = 1
    closed = 2
    closing = 3
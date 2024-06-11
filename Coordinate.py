from Settings import *
from State import LiftState
import numpy as np

# Catatan: Semua koordinat dihitung dari kiri bawah
class Coordinate:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x + w - 1
        self.y2 = y + h - 1
    @staticmethod
    def LiftHall(floor):
        return Coordinate(x=0, y=floor * (hall_height + gap), w=lift_hall_width, h=hall_height)
    @staticmethod
    def Hall(floor):
        return Coordinate(x=lift_hall_width, y=floor * (hall_height + gap), w=hall_width, h=hall_height)
    @staticmethod
    def StairsUp(floor):
        return Coordinate(x=floor_width, y=Coordinate.Hall(floor).y2 - stairs_width + 1, w=stairs_length, h=stairs_width)
    @staticmethod
    def StairsDown(floor):
        return Coordinate(x=floor_width, y=Coordinate.Hall(floor).y, w=stairs_length, h=stairs_width)
    @staticmethod
    def StairsBetween(floor):
        return Coordinate(x=Coordinate.StairsUp(floor).x2 + 1, y=Coordinate.StairsUp(floor).y, w=stairs_width, h=2*stairs_width+gap)
    @staticmethod
    def LiftTrack(lift):
        return Coordinate(x=-(lift + 1) * (lift_size + gap + 2*lift_gap_x), y=0.0, w=lift_size+2*lift_gap_x, h=Coordinate.Hall(floor_count-1).y2 + 1)
    @staticmethod
    def Lift(lift, y):
        lift = 3 - lift
        return Coordinate(x=-(lift + 1) * (lift_size + gap + 2*lift_gap_x) + lift_gap_x, y=y, w=lift_size, h=lift_size)
    @staticmethod
    def LiftDoorInside(lift, y):
        up = ~lift&1
        return Coordinate(x=Coordinate.Lift(lift, y).x + lift_door_inside_gap, y=Coordinate.Lift(lift, y).y2 - lift_door_height + 1 if up else Coordinate.Lift(lift, y).y, w=lift_door_width, h=lift_door_height)
    @staticmethod
    def LiftDoorOutside(floor, lift):
        up = lift&1
        lift //= 2
        return Coordinate(x=lift * (lift_door_gap + lift_door_width) + lift_door_gap, y=Coordinate.LiftHall(floor).y2 - lift_door_height + 1 if up else Coordinate.LiftHall(floor).y, w=lift_door_width, h=lift_door_height)
    @staticmethod
    def LiftDoorOutsideInt(floor, lift):
        up = lift&1
        return Coordinate(Coordinate.LiftDoorOutside(floor, lift).x, Coordinate.LiftHall(floor).y2 if up else Coordinate.LiftHall(floor).y, lift_door_width, 1)
    @staticmethod
    def LiftGrid(lift, y, row, col):
        up = ~lift&1
        row = row if not up else 3 - row
        coordinate = Coordinate.Lift(lift, y)
        return np.array([coordinate.x + col, coordinate.y + row])
    @staticmethod
    def LiftDoorInsideAnimated(lift, time, side):
        close_percentage = 1 if lift.state == LiftState.closed else 0 if lift.state == LiftState.open else (time - lift.door_time) / lift_door_transition_duration if lift.state == LiftState.closing else 1 - (time - lift.door_time) / lift_door_transition_duration
        l, r = 0.2, 0.55
        close_percentage = (r-l) * close_percentage + l
        coordinate = Coordinate.LiftDoorInside(lift.lift_number, lift.y)
        width = coordinate.w * close_percentage
        return Coordinate(coordinate.x if side == "l" else coordinate.x2 + 1 - width, coordinate.y, width, coordinate.h)
    @staticmethod
    def LiftDoorOutsideAnimated(floor, lift, time, side):
        close_percentage = 1 if floor != lift.floor else 1 if lift.state == LiftState.closed else 0 if lift.state == LiftState.open else (time - lift.door_time) / lift_door_transition_duration if lift.state == LiftState.closing else 1 - (time - lift.door_time) / lift_door_transition_duration
        l, r = 0.2, 0.55
        close_percentage = (r-l) * close_percentage + l
        coordinate = Coordinate.LiftDoorOutside(floor, lift.lift_number)
        width = coordinate.w * close_percentage
        return Coordinate(coordinate.x if side == "l" else coordinate.x2 + 1 - width, coordinate.y, width, coordinate.h)
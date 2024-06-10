from Settings import *

# Catatan: Semua koordinat dihitung dari kiri bawah
class Coordinate:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x + w - 1
        self.y2 = y + h - 1
    def inside(self, pos):
        x, y = pos[0], pos[1]
        return self.x <= x and x <= self.x2 and self.y <= y and y <= self.y2
    @staticmethod
    def inside_building(pos):
        for floor in range(floor_count):
            if Coordinate.LiftHall(floor).inside(pos): return True
            if Coordinate.Hall(floor).inside(pos): return True
            if Coordinate.StairsUp(floor).inside(pos): return True
            if Coordinate.StairsDown(floor).inside(pos): return True
        for floor in range(floor_count - 1):
            if Coordinate.StairsBetween(floor).inside(pos): return True
        return False
    @staticmethod
    def LiftHall(floor):
        return Coordinate(x=0.0, y=floor * (hall_height + gap), w=lift_hall_width, h=hall_height)
    @staticmethod
    def Hall(floor):
        return Coordinate(x=lift_hall_width, y=floor * (hall_height + gap), w=hall_width, h=hall_height)
    @staticmethod
    def LiftDoorUp(floor, lift):
        return Coordinate(x=lift * (lift_door_gap + lift_door_width) + lift_door_gap, y=Coordinate.LiftHall(floor).y2 - lift_door_height + 1, w=lift_door_width, h=lift_door_height)
    @staticmethod
    def LiftDoorDown(floor, lift):
        return Coordinate(x=lift * (lift_door_gap + lift_door_width) + lift_door_gap, y=Coordinate.LiftHall(floor).y, w=lift_door_width, h=lift_door_height)
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
        return Coordinate(x=-(lift + 1) * (lift_size + gap), y=0.0, w=lift_size, h=Coordinate.Hall(floor_count-1).y2 + 1)
from Settings import *
from Coordinate import Coordinate

import pygame
import numpy as np
import math

class Color:
    white = (255, 255, 255)
    wood = (205, 133, 63)
    gray = (128, 128, 128)
    light_gray = (211, 211, 211)

class ModelDisplay:
    def __init__(self):
        pygame.init()
        width, height = 800, 600
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("SGLC Stairs Model")
        self.initDisplay()
    
    def initDisplay(self):
        self.initRectangles()
        self.initBounds()
        self.rectangles = [(self.mapRectangle(rectangle[0]), rectangle[1]) for rectangle in self.rectangles]
    
    def addRectangle(self, pos: Coordinate, color):
        self.rectangles.append(((pos.x, pos.y, pos.w, pos.h), color))

    def initRectangles(self):
        self.rectangles = []
        for floor in range(floor_count):
            self.addRectangle(Coordinate.LiftHall(floor), Color.wood)
            self.addRectangle(Coordinate.Hall(floor), Color.wood)

            for lift in range(lift_count // 2):
                self.addRectangle(Coordinate.LiftDoorUp(floor, lift), Color.gray)
                self.addRectangle(Coordinate.LiftDoorDown(floor, lift), Color.gray)

            # class_hall_bottom = patches.Rectangle((lift_hall_width + (hall_width - class_hall_height) / 2, floor * (hall_height + gap) - class_hall_height), class_hall_width, class_hall_height, linewidth=2, edgecolor='black', facecolor='none')
            # self.ax.add_patch(class_hall_bottom)
    
            self.addRectangle(Coordinate.StairsUp(floor), Color.wood)
            self.addRectangle(Coordinate.StairsDown(floor), Color.wood)
        
        for floor in range(floor_count - 1):
            self.addRectangle(Coordinate.StairsBetween(floor), Color.wood)
        
        for lift in range(lift_count):
            self.addRectangle(Coordinate.LiftTrack(lift), Color.light_gray)
            
    def initBounds(self):
        self.bounds = [math.inf, math.inf, 0, 0]
        for rectangle, _ in self.rectangles:
            self.bounds[0] = min(self.bounds[0], rectangle[0])
            self.bounds[1] = min(self.bounds[1], rectangle[1])
            self.bounds[2] = max(self.bounds[2], rectangle[0] + rectangle[2])
            self.bounds[3] = max(self.bounds[3], rectangle[1] + rectangle[3])
        self.bounds += np.array([-margin, -margin, margin, margin])
        self.scale = min(self.screen.get_width() / (self.bounds[2] - self.bounds[0]), self.screen.get_height() / (self.bounds[3] - self.bounds[1]))
        self.offset = np.array([self.screen.get_width() / 2 - self.scale * (self.bounds[0] + self.bounds[2]) / 2, self.screen.get_height() / 2 - self.scale * (self.bounds[1] + self.bounds[3]) / 2])
    
    def mapRectangle(self, rectangle):
        return np.array([rectangle[0] * self.scale + self.offset[0], self.screen.get_height() - ((rectangle[1] + rectangle[3]) * self.scale + self.offset[1]), rectangle[2] * self.scale, rectangle[3] * self.scale])
    def mapCoordinatePoint(self, pos):
        return np.array([pos[0] * self.scale + self.offset[0], self.screen.get_height() - (pos[1] * self.scale + self.offset[1])])

    def redraw(self, persons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.initDisplay()
        self.screen.fill(Color.white)
        for rectangle, color in self.rectangles:
            pygame.draw.rect(self.screen, color, rectangle)
        
        for person in persons:
            pygame.draw.circle(self.screen, (0, 0, 255), self.mapCoordinatePoint(person.pos), person_size*self.scale)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
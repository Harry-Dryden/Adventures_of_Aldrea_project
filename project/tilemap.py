from turtle import Screen
import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        if target.x > 1056 and target.y > 32 and target.x < 1985 and target.y < 705: # if the special room is entered
            x = min(-1024, x)
            y = min(0, y)
            x = max(-(1024), x)
            y = max(-(768 - HEIGHT), y)
            self.camera = pg.Rect(x, y, self.width, self.height)
        elif target.y < (768 + (HEIGHT/2)):
            x = min(0, x)
            y = min(0, y)
            x = max(-(0), x)
            y = max(-(self.height - HEIGHT), y)
            self.camera = pg.Rect(x, y, self.width, self.height)
        elif target.y > (768 + (HEIGHT/2)):
            x = min(0, x)
            y = min(0, y)
            x = max(-(self.width - WIDTH), x)
            y = max(-(self.height - HEIGHT), y)
            self.camera = pg.Rect(x, y, self.width, self.height)

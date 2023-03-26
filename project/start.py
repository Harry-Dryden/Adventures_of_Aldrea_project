import pygame as pg
from settings import *

class Start(pg.sprite.Sprite):
    def __init__(self, game, x, y,):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.image = pg.image.load("starticon.png")
        self.imageVal = 1

    def controls(self):
        if self.imageVal == 1:
            self.image = pg.image.load("controlicon.png")
            self.imageVal = 2

    def startScre(self):
        if self.imageVal == 2:
            self.image = pg.image.load("starticon.png")
            self.imageVal = 1

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL]:
            self.controls()
        if keys[pg.K_s]:
            self.startScre()

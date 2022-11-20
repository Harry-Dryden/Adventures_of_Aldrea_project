from sys import _xoptions
import pygame as pg
from settings import *
from tilemap import *
from os import path
import random

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("playerR.png")
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.direction = "UP"
        self.attacking = False
        self.dodging = False
        self.permdodge = 1500
        self.dodgecounter = 0

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7
            self.vy *= 0.7
        if keys[pg.K_LSHIFT]:
            self.dodge()
        if keys[pg.K_SPACE]:
            self.attack()
            self.attacking = True

    def collideWithWalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def dodge(self): #working 'dodge' function
        quickdodge = self.permdodge #sets the local variable
        if self.vx == 0 and self.vy == 0 and self.dodging == True: #if you were dodging but stopped moving
            self.permdodge = 1500 #resets dodge speed
            self.dodging = False #stops dodging
            self.dodgecounter = 0
        if quickdodge == 0: #if the dodge has ended
            self.permdodge = 1500 #does the same as above
            self.dodging = False
            self.dodgecounter = 0
            print("succesful dodge")
        if self.dodging == True or self.dodgecounter >= 200: #if you are dodging or if the counter is right
            if self.dodging == False: 
                self.dodging = True #if you werent dodging you now are
            keys = pg.key.get_pressed() #moving faster at dodge speed
            if keys[pg.K_a]:
                self.vx = -PLAYER_SPEED - quickdodge
            if keys[pg.K_d]:
                self.vx = PLAYER_SPEED + quickdodge
            if keys[pg.K_w]:
                self.vy = -PLAYER_SPEED - quickdodge
            if keys[pg.K_s]:
                self.vy = PLAYER_SPEED + quickdodge
            if self.vx != 0 and self.vy != 0:
                self.vx *= 0.7
                self.vy *= 0.7
            self.permdodge -= 100 #lowers dodge speed

    def getDirection(self):
        if self.vx < 0 and self.vy == 0:
            self.direction = "LEFT"
            self.image = pg.image.load("playerL.png")
        if self.vx > 0 and self.vy == 0:
            self.direction = "RIGHT"
            self.image = pg.image.load("playerR.png")
        if self.vx == 0 and self.vy < 0:
            self.direction = "UP"
            self.image = pg.image.load("playerU.png")
        if self.vx == 0 and self.vy > 0:
            self.direction = "DOWN"
            self.image = pg.image.load("playerD.png")
        if self.vx > 0 and self.vy > 0:
            self.direction = "DOWNRIGHT"
            self.image = pg.image.load("playerD.png")
        if self.vx > 0 and self.vy < 0:
            self.direction = "UPRIGHT"
            self.image = pg.image.load("playerU.png")
        if self.vx < 0 and self.vy > 0:
            self.direction = "DOWNLEFT"
            self.image = pg.image.load("playerD.png")
        if self.vx < 0 and self.vy < 0:
            self.direction = "UPLEFT"
            self.image = pg.image.load("playerU.png")
        
    def attack(self):
        print("Attacking")
        self.attacking = False

    def update(self):
        keys = pg.key.get_pressed()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collideWithWalls('x')
        self.rect.y = self.y
        self.collideWithWalls('y')
        xPos = int(self.x)
        yPos = int(self.y)
        if keys[pg.K_t]:
            print('y:')
            print(yPos)
            print('x:')
            print(xPos)
        if xPos >= 192 and xPos < 260 and yPos >= 224 and yPos <= 240:
            self.x = 1504
            self.y = 672
        if xPos >= 1504 and xPos < 1568 and yPos <= 704 and yPos >=690:
            self.x = 192
            self.y = 256
        self.dodgecounter += 1
        if self.dodging == True: #if you're dodging
            self.dodge()
        self.getDirection()
        if self.attacking == True:
            self.attack()
        print(self.direction)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("enemy1.png")
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.enemyRandom = random.randint(1,8)
        self.enemyDifficulty = 2
        self.enemyCounter = 0

    def move(self):
        self.vx = 0
        self.vy = 0
        if self.enemyRandom == 1:
            self.vx = -ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 2:
            self.vx = -ENEMY_SPEED * self.enemyDifficulty
            self.vy = +ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 3:
            self.vy = +ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 4:
            self.vx = +ENEMY_SPEED * self.enemyDifficulty
            self.vy = +ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 5:
            self.vx = +ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 6:
            self.vx = +ENEMY_SPEED * self.enemyDifficulty
            self.vy = -ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 7:
            self.vy = -ENEMY_SPEED * self.enemyDifficulty
        if self.enemyRandom == 8:
            self.vx = -ENEMY_SPEED * self.enemyDifficulty
            self.vy = -ENEMY_SPEED * self.enemyDifficulty
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7
            self.vy *= 0.7

        """
        if Player.x > self.x:
            self.vx = -ENEMY_SPEED
        if Player.x < self.x:
            self.vx = +ENEMY_SPEED
        if Player.y > self.y:
            self.vy = -ENEMY_SPEED
        if Player.y > self.y:
            self.vy = +ENEMY_SPEED """

    def collideWithWalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.enemyRandom = random.randint(1,8)
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.enemyRandom = random.randint(1,8)
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.enemyCounter += 1
        print(self.enemyCounter)
        if self.enemyCounter >= 200:
            self.enemyRandom = random.randint(1,8)
            self.enemyCounter = 0
            print(self.enemyRandom)
        self.move()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collideWithWalls('x')
        self.rect.y = self.y
        self.collideWithWalls('y')

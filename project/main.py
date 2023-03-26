import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from start import *

class Game:
    # initialising the game
    def __init__(self):
        pg.init()
        #setting up the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        game_folder = path.dirname(__file__)
        self.startmap = Map(path.join(game_folder, 'startmap.txt'))
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.mapNum = 1
#        self.playerDirection = "UP"
        
    def newOut(self, outside):
        # initialize all variables and do all the setup for a new game
        #loading up the map file
        #creating the map
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, outside)
                if tile == '2':
                    Door(self, col, row, outside)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    Enemy(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def startScreen(self):
        for row, tiles in enumerate(self.startmap.data):
            for col, tile in enumerate(tiles):
                if tile == 'S':
                    Start(self,col,row)
        self.camera = Camera(self.map.width, self.map.height)
                    

    def runFirst(self, time):
        #setting self.playing to false will end the game loop, which runs in this while loop
        self.playing = True
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        if time == 1:
            self.startScreen()
        if time == 2:
            self.newOut(False)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events(time)
            self.update(time)
            self.draw(time)

    def quit(self):
        #necessary quit function to close the game cleanly
        pg.quit()
        sys.exit()

    def update(self, time):
        if time == 1:
            self.all_sprites.update()
        else:
            # updates its portion of the game loop
            self.all_sprites.update()
            self.camera.update(self.player)
            Door.enterDoor(self, self.player, self.mapNum)
            if Door.enterDoor(self, self.player, self.mapNum) == True:
                self.newMap()
            game_folder = path.dirname(__file__)
#        Player.getDirection = self.playerDirection
#        print(self.playerDirection)
#        Player.isAttacking(self)
#        if Player.isAttacking(self) == True:
#            Sword(self, self.player.x, self.player.y, self.playerDirection)
            if self.map == Map(path.join(game_folder, 'map.txt')):
                self.mapNum = 1
            if self.map == Map(path.join(game_folder, 'map2.txt')):
                self.mapNum = 2
#        print(self.player.x)
#        print(self.player.y)

#    def draw_grid(self):
#        for x in range(0, WIDTH, TILESIZE):
#            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
#        for y in range(0, HEIGHT, TILESIZE):
#            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self, time):
        if time == 1:
            self.screen.fill(STARTCOLOUR)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image,self.camera.apply(sprite))
            pg.display.flip()
        else:
            self.screen.fill(BACKGROUNDCOLOUR)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image,self.camera.apply(sprite))
#           self.draw_grid()
            pg.display.flip()

    def events(self,time):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_0:
                    self.newMap()
                if time == 1:
                    if event.key == pg.K_SPACE:
                        self.runFirst(2)

    def newMap(self):
        if self.mapNum == 1:
            game_folder = path.dirname(__file__)
            self.map = Map(path.join(game_folder, 'map2.txt'))
            self.newOut(True)
            self.mapNum = 2
        elif self.mapNum == 2:
            game_folder = path.dirname(__file__)
            self.map = Map(path.join(game_folder, 'map.txt'))
            self.newOut(False)
            self.mapNum = 1

# create the game object
g = Game()
while True:
    g.runFirst(1)
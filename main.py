# This file was created by: Ethan Chan

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
import random
from settings import *
from sprites import *

# created a game class to instantiate later
# it will have all the necessary parts to run the game
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Ethan's Game")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 50, 50)
        self.mob = Mob(self, 100, 100)
        self.wall = Wall(self, 200, 200)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.mob)
        self.all_sprites.add(self.wall)
        for i in range(6):
            print(i*TILESIZE)
            Wall(self, i*TILESIZE, i*TILESIZE)
        for i in range(6):
            Mob(self, i*random.randint(0, WIDTH), i*random.randint(0, HEIGHT))
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

        # input
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
        # pg.quit()
        # process
    def update(self):
        self.all_sprites.update()
        # output
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
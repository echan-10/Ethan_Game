# This file was created by: Ethan Chan

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
import random
from settings import *
from sprites import *

# created a game class to instantiate later
# it will have all the necessary parts to run the game
# the game class is created to organize the elements needed to create a game
class Game:

    # the game __init__ method intializes all the necessary components for the game, including video and sound
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # this sets the length and width of the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # this is the name of the pygame window
        pg.display.set_caption("Ethan's Game")
        # game clock which allows us to set the framerate
        self.clock = pg.time.Clock()
        self.running = True

    # this defines a new game instance of itself everytime it runs
    def new(self):
        # adds all sprites or characters into a group, which helps instantiate, update, and render all characters at once, rather than individually
        self.all_sprites = pg.sprite.Group()
        # creates a new player instance sprite at 50, 50 
        self.player = Player(self, 1, 1)
        # creates a new mob instance sprite at 100, 100
        self.mob = Mob(self, 100, 100)
        # creates a new wall instance sprite at 200, 200
        self.wall = Wall(self, 200, 200)
        # ading all sprites into a group
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.mob)
        self.all_sprites.add(self.wall)
        # for loop runs 6 times, creating 6 walls
        for i in range(6):
            Wall(self, i*TILESIZE, i*TILESIZE)
        # for loop runs 6 times, creating 6 mobs and random coordinates
        for i in range(6):
            Mob(self, i*random.randint(0, WIDTH), i*random.randint(0, HEIGHT))
            
    # while self.running keeps checking to see if the game is still running
    # if self.running is True, it will run events(), update(), and draw()
    # if self.running is False, it will not run these events and close the game under the events() function
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        # constantly listens for an event, such as keystrokes
        for event in pg.event.get():
                # closes game if there are no more events
                if event.type == pg.QUIT:
                    self.running = False

    # updates the sprites on the screen, so that the sprites will move when its x or y coordinate changes
    def update(self):
        self.all_sprites.update()

    # draws the background sprites on the screen
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # checks file name and runs the game loop by running the new() and run() methods
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
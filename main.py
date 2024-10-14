# This file was created by: Ethan Chan

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
import random
from settings import *
from tilemap import *
from os import path
from sprites import *

'''
Elevator Pitch: I want to create a game where a character must complete three levels to reach the top of the castle and defeat a final boss. There will be obstacles, disappearing walls that are randomly generated, enemies, and teleportation portals at the end of each level that will take to the player to the next level.

GOALS: Complete all three levels
RULES: Cannot move through walls, can only kill enemies when a specific powerup is collected, go through portals to go to next level.
FEEDBACK: If you collide with an enemy before eating a powerup, you will die. Collect all coins for the portal to appear in the level.
FREEDOM: Move around inside the game space, collect coins

'''
# created a game class to instantiate later
# it will have all the necessary parts to run the game
# the game class is created to organize the elements needed to create a game
class Game:

    # the game __init__ method intializes all the necessary components for the game, including video and sound
    def __init__(self):
        self.game = Game
        pg.init()
        pg.mixer.init()
        # this sets the length and width of the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # this is the name of the pygame window
        pg.display.set_caption("Ethan's Game")
        # game clock which allows us to set the framerate
        self.clock = pg.time.Clock()
        self.running = True

    def load_data(self, level):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, level))
        print("it worked")
    # this defines a new game instance of itself everytime it runs
    def new(self):
        self.load_data("level1.txt")
        # adds all sprites or characters into a group, which helps instantiate, update, and render all characters at once, rather than individually
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_portals = pg.sprite.Group()
        # creates a new player instance sprite at 50, 50 
        # self.player = Player(self, 1, 1)
        # creates a new mob instance sprite at 100, 100
        # self.mob = Mob(self, 100, 100)
        # # creates a new wall instance sprite at 200, 200
        # self.wall = Wall(self, 200, 200)
        # ading all sprites into a group
        # self.all_sprites.add(self.player)
        # self.all_sprites.add(self.mob)
        # self.all_sprites.add(self.wall)
        # for loop runs 6 times, creating 6 walls
        # for i in range(6):
        #     Wall(self, i*TILESIZE, i*TILESIZE)
        # # for loop runs 6 times, creating 6 mobs and random coordinates
        # for i in range(6):
        #     Mob(self, i*random.randint(0, WIDTH), i*random.randint(0, HEIGHT))
        
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
                if tile == "U":
                    Powerup(self, col, row)
                if tile == "C":
                    Coin(self, col, row)
                if tile == "O":
                    Portal(self, col, row)
            
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

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
    # draws the background sprites on the screen
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt*1000) + "FPS", 24, WHITE, WIDTH / 24, HEIGHT / 100)
        self.draw_text(self.screen, "Level 1", 24, WHITE, WIDTH / 2, HEIGHT / 100)
        self.draw_text(self.screen, "Coins Collected: " + str(self.player.coins) , 24, WHITE, WIDTH / 12, HEIGHT / 30)
        pg.display.flip()

    # checks file name and runs the game loop by running the new() and run() methods
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
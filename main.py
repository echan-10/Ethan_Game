# This file was created by: Ethan Chan

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
import random
from settings import *
from tilemap import *
from os import path
from sprites import *
# from sprites_sidescroller import Player as SideScrollerPlayer  # Import sidescroller player
# from sprites_sidescroller import Projectile

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
        # define variables that are not supposed to be reset every level here
        # self.highscore = 0
        self.level = 1 # CHANGE THIS LATER
        self.lives = 15
        self.score = 0
        self.boss_lives = 2
        self.speed_multiplier = 1
        self.projectileSpeed = 1
        self.special_ammo = 0
        self.collected = True
        self.running = True
        self.top_down = True
        pg.init()
        pg.mixer.init()
        # this sets the length and width of the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # this is the name of the pygame window
        pg.display.set_caption("Ethan's Game")
        # game clock which allows us to set the framerate
        self.clock = pg.time.Clock()
        self.load_data("level1.txt") # CHANGE THIS LATER
        pg.mixer.Sound.play(self.music)

    def load_data(self, level):
        self.game_folder = path.dirname(__file__)
        # LOAD HIGH SCORE FILE

        # with open(path.join(self.game_folder, HS_FILE), 'w') as file:
        #     file.write("High Score File")
        
        # print("File created")

        try:
            with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                f.write(str(self.highscore))
                
        self.img_folder = path.join(self.game_folder, 'images')
        self.snd_folder = path.join(self.game_folder, 'sounds')

        # load sounds
        self.coin_snd = pg.mixer.Sound(path.join(self.snd_folder, 'coin_sound.wav'))
        self.gainhp_snd = pg.mixer.Sound(path.join(self.snd_folder, 'gainhp_sound.wav'))
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'jump_sound.wav'))
        self.portal_snd = pg.mixer.Sound(path.join(self.snd_folder, 'portal_sound.wav'))
        self.portal_snd.set_volume(0.3)
        self.music = pg.mixer.Sound(path.join(self.snd_folder, 'background_music.mp3'))
        self.music.set_volume(0.5)


        self.map = Map(path.join(self.game_folder, level))
        # self.player_img = pg.image.load(path.join(self.img_folder, "bell.png"))
        print("Opened new level")
    # this defines a new game instance of itself everytime it runs
    def new(self):
        # self.load_data("level1.txt")
        # adds all sprites or characters into a group, which helps instantiate, update, and render all characters at once, rather than individually
        # define variables here if you want it to reset after every level
        self.spawnPortal = False
        self.coins = 0
        self.ammo = 5
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_portals = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_playerprojectiles = pg.sprite.Group()
        self.all_bossprojectiles = pg.sprite.Group()
        self.all_mobprojectiles = pg.sprite.Group()
        self.all_bosses = pg.sprite.Group()
        self.all_invisiblewalls = pg.sprite.Group()
        self.all_specialprojectiles = pg.sprite.Group()
        self.all_shootspecialprojectiles = pg.sprite.Group()

        print(self.level)
        if self.level == 1:
            self.top_down = True
        elif self.level == 2:
            self.top_down = False
        elif self.level == 3:
            self.top_down = True
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
                    self.player = Player(self, col, row)  # Default top-down movement
                    
                    # self.player = Player(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
                if tile == "U":
                    Powerup(self, col, row)
                if tile == "C":
                    Coin(self, col, row)
                if tile == "O":
                    Portal(self, col, row)
                if tile == "B":
                    Boss(self, col, row)
                if tile == "I":
                    InvisibleWall(self, col, row)
        if self.level == 3:
                    SpecialProjectile(self)
                    print("i have a special projectile")
            
    # while self.running keeps checking to see if the game is still running
    # if self.running is True, it will run events(), update(), and draw()
    # if self.running is False, it will not run these events and close the game under the events() function
    
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            if self.lives <= 0:
                # checks number of lives and sees if you have any more lives
                self.highscoreCheck()
                self.running = False

    def events(self):
        # constantly listens for an event, such as keystrokes
        for event in pg.event.get():
            # closes game if there are no more events
            if event.type == pg.QUIT:
                self.highscoreCheck()
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
        if hasattr(self, 'player'):
            self.all_sprites.draw(self.screen)
            # might want to use if hasattr function to make sure all sprites are there
            self.draw_text(self.screen, str(self.dt*1000) + "FPS", 24, WHITE, WIDTH - 980, HEIGHT - 770)
            self.draw_text(self.screen, "Level " + str(self.level), 24, WHITE, WIDTH / 2, HEIGHT / 100)
            self.draw_text(self.screen, "Coins Collected: " + str(self.coins) , 24, WHITE, WIDTH - 940, HEIGHT - 750)
            self.draw_text(self.screen, "Lives: " + str(self.lives) , 24, WHITE, WIDTH - 985, HEIGHT - 730)
            self.draw_text(self.screen, "Ammo: " + str(self.ammo) , 24, WHITE, WIDTH - 980, HEIGHT - 710)
            self.draw_text(self.screen, "Special Ammo: " + str(self.special_ammo) , 24, WHITE, WIDTH - 945, HEIGHT - 690)
            self.draw_text(self.screen, "High Score: " + str(self.highscore), 24, WHITE, WIDTH - 80, HEIGHT - 770)
            self.draw_text(self.screen, "Current Score: " + str(self.score), 24, WHITE, WIDTH - 80, HEIGHT - 750)
            if self.level == 3:
                self.draw_text(self.screen, "Boss Lives: " + str(self.boss_lives) , 24, WHITE, WIDTH - 945, HEIGHT - 670)
            pg.display.flip()
        else:
            print("YIKES")
            self.running = False
            # can use this code to give end screen if player dies

    def highscoreCheck(self):
        if self.score > self.highscore:
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                f.write(str(self.score))

    # checks file name and runs the game loop by running the new() and run() methods
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
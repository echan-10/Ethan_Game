# This file was created by Ethan Chan

import pygame as pg
import random
from pygame.sprite import Sprite
from settings import *
from utils import *
# from threading import Timer

class Player(Sprite):
    def __init__(self, game, x, y, col=None, row=None):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        # self.rect.x = x
        # self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.max_speed = 400
        self.speed = 10
        self.vx, self.vy = 0, 0
        self.speed_multiplier = 1
        self.cd = Cooldown()

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed * self.speed_multiplier
        if keys[pg.K_a]:
            self.vx -= self.speed * self.speed_multiplier   
            print(self.vx)  
        if keys[pg.K_s]:
            self.vy += self.speed * self.speed_multiplier
        if keys[pg.K_d]:
            self.vx += self.speed * self.speed_multiplier
        
        if abs(self.vx) > self.max_speed:
            if self.vx > 0:
                self.vx = self.max_speed
            elif self.vx < 0:
                self.vx = -self.max_speed
        if abs(self.vy) > self.max_speed:
            if self.vy > 0:
                self.vy = self.max_speed
            elif self.vy < 0:
                self.vy = -self.max_speed
        if pg.mouse.get_pressed()[0]:
            print(pg.mouse.get_pos())
            self.shoot()

    def shoot(self):
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
        if self.cd.delta > 0.01:
            p = Projectile(self.game, self.rect.x, self.rect.y)
        else:
            print("Weapon on cooldown")



    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:
                    self.y= hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                powerupChoice = random.randint(0, 100)
                if powerupChoice > 30:
                    print("extra speed!")
                    self.speed_multiplier += 0.5
                else:
                    print("extra life!")
                    self.game.lives += 1
            if str(hits[0].__class__.__name__) == "Coin":
                self.game.coins += 1
            if str(hits[0].__class__.__name__) == "Portal":
                # self.game.new()
                print(self.game.level)
                self.game.level += 1
                textLevel = "level" + str(self.game.level) + ".txt"
                self.game.load_data(textLevel)
                self.game.new()
                print(textLevel)
            if str(hits[0].__class__.__name__) == "Mob":
                self.game.lives -= 1

                # replace the print function to call a method that will load next level
            


    def update(self):
        self.cd.ticking()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_portals, True)
        self.collide_with_stuff(self.game.all_mobs, True)
        # self.collide_with_stuff(self.game.all_projectiles, True)

        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
        self.category = random.choice([0, 1])

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed *= -1
            self.rect.y += 32
        # elif self.rect.colliderect(self.game.player):
        #     self.speed *= -1
        # moving towards the side of the screen
        # when it hits the side of the screen, it will move down
        # then it will towards the other side of the screen
        # if it gets to the bottom, then teleport to the top of the screen

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
        pass


class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PINK)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Portal(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_portals
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PURPLE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_projectiles
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PINK)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
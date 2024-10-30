# This file was created by Ethan Chan

import pygame as pg
import random
from pygame.sprite import Sprite
from settings import *
# from threading import Timer
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        # self.rect.x = x
        # self.rect.y = y
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.pos = vec(x * TILESIZE, y * TILESIZE)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.speed = 1.5
        self.jumping = False
        self.jump_power = 13
        self.max_speed = 8
        # self.vx, self.vy = 0, 0
        # self.coins = 0


        # self.level = 1
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.vy -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed  
            print(self.vel.x)  
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()

        if abs(self.vel.x) > self.max_speed:
            if self.vel.x > 0:
                self.vel.x = self.max_speed
            elif self.vel.x < 0:
                self.vel.x = -self.max_speed


    def jump(self):
        print("I'm trying to jump")
        print(self.vel.y)
        self.rect.y += 2
        # adjusts the y value to be 2 pixels lower to detect collision with platform to jump
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y= hits[0].rect.top - self.rect.height
                    self.jumping = False
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed += 2
            if str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
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
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt

        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_portals, True)
        self.collide_with_stuff(self.game.all_mobs, True)

        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')





class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
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
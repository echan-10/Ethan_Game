# This file was created by Ethan Chan

import pygame as pg
from pygame.sprite import Sprite
from settings import *

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed      
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_d]:
            self.rect.x += self.speed
    def update(self):
        self.get_keys()

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left <0:
            self.speed *= -1
            self.rect.y += 32
        elif self.rect.colliderect(self.game.player):
            self.speed *= -1
        # moving towards the side of the screen
        # when it hits the side of the screen, it will move down
        # then it will towards the other side of the screen
        # if it gets to the bottom, then teleport to the top of the screen

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.x = x
        self.rect.y = y
    def update(self):
        pass
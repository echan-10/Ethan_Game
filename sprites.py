# This file was created by Ethan Chan

import pygame as pg
import random
from pygame.sprite import Sprite
from settings import *
from utils import *
import math
# from threading import Timer
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y, col=None, row=None):
        self.game = game
        self.groups = game.all_sprites
        print(self.game.top_down)
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        # self.rect.x = x
        # self.rect.y = y
        if self.game.top_down == True:
            print("top down")
            self.x = x * TILESIZE
            self.y = y * TILESIZE
            self.max_speed = 400
            self.speed = 10
            self.vx, self.vy = 0, 0
            print(self.x, self.y)
            self.cd = Cooldown()
        if self.game.top_down == False:
            print("sidescroller")

            self.pos = vec(x * TILESIZE, y * TILESIZE)
            print(self.pos)
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.speed = 2
            self.jumping = False
            self.jump_power = 15
            self.max_speed = 10
            self.cd = Cooldown()

    def top_down_get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed * self.game.speed_multiplier
        if keys[pg.K_a]:
            self.vx -= self.speed * self.game.speed_multiplier   
        if keys[pg.K_s]:
            self.vy += self.speed * self.game.speed_multiplier
        if keys[pg.K_d]:
            self.vx += self.speed * self.game.speed_multiplier
        
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
            self.shoot()
    
    def sidescroller_get_keys(self):
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
            print(self.vel.x)
        if keys[pg.K_SPACE]:
            self.jump()

        if abs(self.vel.x) > self.max_speed:
            if self.vel.x > 0:
                self.vel.x = self.max_speed
            elif self.vel.x < 0:
                self.vel.x = -self.max_speed
        if pg.mouse.get_pressed()[0]:
            print(pg.mouse.get_pos())
            self.shoot()

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
            pg.mixer.Sound.play(self.game.jump_snd)

    def shoot(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.game.top_down == True:
            dx = mouse_x - self.x
            dy = mouse_y - self.y
        elif self.game.top_down == False:
            dx = mouse_x - self.pos.x
            dy = mouse_y - self.pos.y
        angle = math.atan2(dy, dx)

        self.cd.event_time = floor(pg.time.get_ticks()/1000)
        if self.cd.delta > 0.001:
            if self.game.special_ammo > 0:
                p = ShootSpecialProjectile(self.game, self.rect.centerx, self.rect.centery, angle)
                self.game.special_ammo -= 1
            elif self.game.ammo > 0:
                p = PlayerProjectile(self.game, self.rect.centerx, self.rect.centery, angle)
                self.game.ammo -= 1
            else:
                print("NO AMMO")
        else:
            print("Weapon on cooldown")


    def top_down_collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            hits2 = pg.sprite.spritecollide(self, self.game.all_invisiblewalls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if hits2:
                if self.vx > 0:
                    self.x = hits2[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits2[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            hits2 = pg.sprite.spritecollide(self, self.game.all_invisiblewalls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
            if hits2:
                if self.vy > 0:
                    self.y = hits2[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits2[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    def sidescroller_collide_with_walls(self, dir):
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


    def top_down_collide_with_invisiblewalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_invisiblewalls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_invisiblewalls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
        
    def sidescroller_collide_with_invisible_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_invisiblewalls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_invisiblewalls, False)
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
                pg.mixer.Sound.play(self.game.gainhp_snd)
                powerupChoice = random.randint(0, 100)
                if powerupChoice <= 30:
                    self.game.speed_multiplier += 0.5
                elif powerupChoice > 30 and powerupChoice <= 60:
                    self.game.ammo += 5
                elif powerupChoice > 60 and powerupChoice <= 90:
                    self.game.projectileSpeed += 0.5
                else:
                    self.game.lives += 1
            if str(hits[0].__class__.__name__) == "Coin":
                pg.mixer.Sound.play(self.game.coin_snd)
                self.game.coins += 1
                self.game.score += 1000
            if str(hits[0].__class__.__name__) == "Portal":
                pg.mixer.Sound.stop(self.game.portal_snd)
                # self.game.new()
                self.game.level += 1
                textLevel = "level" + str(self.game.level) + ".txt"
                self.game.load_data(textLevel)
                self.game.new()
            if str(hits[0].__class__.__name__) == "Mob":
                self.game.lives -= 1
                self.game.score += 500
            if str(hits[0].__class__.__name__) == "BossProjectile":
                self.game.lives -= 1
            if str(hits[0].__class__.__name__) == "MobProjectile":
                self.game.lives -= 1
            # if str(hits[0].__class__.__name__) == "SpecialProjectile":
            #     self.game.special_ammo += 1
            #     SpecialProjectile(self.game)

                # replace the print function to call a method that will load next level
            


    def update(self):
        self.cd.ticking()
        if self.game.top_down == True:
            self.top_down_get_keys()
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt

            self.rect.x = self.x
            self.top_down_collide_with_walls('x')
            self.top_down_collide_with_invisiblewalls('x')
            self.rect.y = self.y
            self.top_down_collide_with_walls('y')
            self.top_down_collide_with_invisiblewalls('y')
        elif self.game.top_down == False:
            self.acc = vec(0, GRAVITY)
            self.sidescroller_get_keys()
            self.acc.x += self.vel.x * FRICTION
            self.vel += self.acc

            if abs(self.vel.x) < 0.1:
                self.vel.x = 0

            self.pos += self.vel + 0.5 * self.acc

            self.rect.x = self.pos.x
            self.sidescroller_collide_with_walls('x')
            self.sidescroller_collide_with_invisible_walls('x')
            self.rect.y = self.pos.y
            self.sidescroller_collide_with_walls('y')
            self.sidescroller_collide_with_invisible_walls('y')
            if self.pos.y > HEIGHT:
                self.pos.x, self.pos.y = 96, 704
                print("You fell off the map!")

        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_portals, True)
        self.collide_with_stuff(self.game.all_mobs, True)
        self.collide_with_stuff(self.game.all_bossprojectiles, True)
        self.collide_with_stuff(self.game.all_mobprojectiles, True)
        self.collide_with_stuff(self.game.all_specialprojectiles, True)



            

        # self.rect.x = self.x
        # self.collide_with_invisiblewalls('x')
        # self.rect.y = self.y
        # self.collide_with_invisiblewalls('y')



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
        self.shootTimer = 0
        self.moveTimer = 0
        self.shootCountdown = random.randint(1000, 2000)
        self.moveCountdown = random.randint(1000, 3000)
        self.move()
    def shoot(self):
        self.mob_x, self.mob_y = self.rect.centerx, self.rect.centery

        # self.game.player.x is for top down movement
        # self.game.player.pos.x is for sidescroller movement
        if self.game.top_down:
            player_x, player_y = self.game.player.x, self.game.player.y
        else:
            player_x, player_y = self.game.player.pos.x, self.game.player.pos.y
        # player_x, player_y = self.game.player.x, self.game.player.y
        dx = player_x - self.mob_x
        dy = player_y - self.mob_y
        angle = math.atan2(dy, dx)
        p = MobProjectile(self.game, self.rect.centerx, self.rect.centery, angle)

    def move(self):
        # self.mob_x, self.mob_y = self.rect.centerx, self.rect.centery
        global random_pos_x
        global random_pos_y
        random_pos_x = random.randint(0, (WIDTH // TILESIZE) - 1) * TILESIZE
        random_pos_y = random.randint(0, (HEIGHT // TILESIZE) - 1) * TILESIZE
        print("x:", random_pos_x)
        print("y:", random_pos_y)
        dx = random_pos_x - self.rect.x
        dy = random_pos_y - self.rect.y
        angle = math.atan2(dy, dx)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)


    def update(self):
        # gets current time
        # if self.rect.x <= 0:
        #     self.rect.x = 0
        # if self.rect.x >= WIDTH - TILESIZE:
        #     self.rect.x >= WIDTH - TILESIZE
        # if self.rect.y <= 0:
        #     self.rect.y = 0
        # if self.rect.y >= HEIGHT - TILESIZE:
        #     self.rect.y = HEIGHT - TILESIZE

        self.rect.x += self.vx
        self.rect.y += self.vy

        current_move_time = pg.time.get_ticks()
        if current_move_time - self.moveTimer >= self.moveCountdown:
            self.move()
            self.moveTimer = current_move_time

        
        current_shoot_time = pg.time.get_ticks()
        # finds time difference between every shot and checks to see if 2 seconds have passed
        if current_shoot_time - self.shootTimer >= self.shootCountdown:
            self.shoot()
            # reset the timer to the current time (or 2 seconds), so the mob doesn't rapid fire within the 2 seconds
            self.shootTimer = current_shoot_time
        

        # if self.rect.right > WIDTH or self.rect.left < 0:
        #     self.speed *= -1
        #     self.rect.y += 32
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

class InvisibleWall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_invisiblewalls
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(TRANSPARENT)
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

        self.x_original = x * TILESIZE
        self.y_original = y * TILESIZE

        self.image.fill(PURPLE)
        self.rect.x = self.x_original + (100 * TILESIZE)
        self.rect.y = self.y_original
    def update(self):
        if self.game.coins >= 3:
            self.rect.x = self.x_original
            self.rect.y = self.y_original
            pg.mixer.Sound.play(self.game.portal_snd)
        else:
            self.rect.x = self.x_original + (100 * TILESIZE)

class PlayerProjectile(Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.all_sprites, game.all_playerprojectiles
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(ORANGE)
        self.rect.center = (x, y)
        self.speed = 10
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "BossProjectile":
                self.kill()
            if str(hits[0].__class__.__name__) == "Mob":
                self.kill()
                self.game.score += 500
            if str(hits[0].__class__.__name__) == "MobProjectile":
                self.kill()
            # Add more to this later for special bullets
    def update(self):
        self.rect.x += self.vx * self.game.projectileSpeed
        self.rect.y += self.vy * self.game.projectileSpeed
        if (self.rect.x < 0 or self.rect.x > WIDTH or
            self.rect.y < 0 or self.rect.y > HEIGHT):
            self.kill() 
        # Collision:
        self.collide_with_stuff(self.game.all_mobs, True)
        self.collide_with_stuff(self.game.all_mobprojectiles, True)
        self.collide_with_stuff(self.game.all_bossprojectiles, True)

class Boss(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_bosses
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PINK)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.shootTimer = 0
        self.shootCountdown = 5000
    def shoot(self):
        # gets all the angles in pi radians for every 15 degrees (15 * 24 iterations = 360 degrees)
        angles = [i * math.pi / 12 for i in range(24)]
        for angle in angles:
            # creates 24 projectile sprites all offset by 15 degrees
            p = BossProjectile(self.game, self.rect.centerx, self.rect.centery, angle)
        # spawns mob at a random location
        mob_x = random.randint(1, 31)
        mob_y = random.randint(1, 24)
        mob = Mob(self.game, mob_x, mob_y)
        print("mob spawned")
        print(self.game.all_mobs)
        print(mob_x, mob_y)
            # self.game.all_projectiles.add(p)
    def update(self):
        # gets current time
        current_time = pg.time.get_ticks()
        # finds time difference between every shot and checks to see if 5 seconds have passed
        if current_time - self.shootTimer >= self.shootCountdown:
            self.shoot()
            
            # reset the timer to the current time (or 5 seconds), so the boss doesn't rapid fire within the 5 seconds
            self.shootTimer = current_time
        if self.game.boss_lives == 0:
            self.kill()
            self.game.highscoreCheck()
            self.game.running = False
            print("YOU WIN!!!!!!!")
class BossProjectile(Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.all_sprites, game.all_bossprojectiles
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.rect.center = (x, y)
        self.speed = 10
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Wall":
                self.kill()
            if str(hits[0].__class__.__name__) == "ShootSpecialProjectile":
                self.kill()
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.collide_with_stuff(self.game.all_walls, True)
class MobProjectile(Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.all_sprites, game.all_mobprojectiles
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.rect.center = (x, y)
        self.speed = 10
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Player":
                self.game.lives -= 1
                self.kill()
            if str(hits[0].__class__.__name__) == "PlayerProjectile":
                self.kill()
            if str(hits[0].__class__.__name__) == "ShootSpecialProjectile":
                self.kill()
            # if str(hits[0].__class__.__name__) == "Wall":
            #     self.kill()
            
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.collide_with_stuff(self.game.all_shootspecialprojectiles, True)
        self.collide_with_stuff(self.game.all_playerprojectiles, True)
        # self.collide_with_stuff(self.game.all_walls, False)

class SpecialProjectile(Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.all_specialprojectiles
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(SKYBLUE)
        self.position = random.choice([(5, 5), (10, 10), (15, 15), (20, 20)])
        print("you instantiated specialprojectile")
        if self.game.collected == True:
            print("it wokred")
            self.rect.x = self.position[0] * TILESIZE
            self.rect.y = self.position[1] * TILESIZE
            self.game.collected = False

    def update(self):
        if pg.sprite.collide_rect(self, self.game.player):
            self.game.special_ammo += 1
            self.game.collected = True
            self.kill()
            SpecialProjectile(self.game)


class ShootSpecialProjectile(Sprite):
    def __init__(self, game, x, y, angle):
        self.groups = game.all_sprites, game.all_shootspecialprojectiles
        self.game = game
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(SKYBLUE)
        self.rect.center = (x, y)
        self.speed = 10
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Boss":
                self.game.boss_lives -= 1
                self.kill()
                self.game.score += 2000
            if str(hits[0].__class__.__name__) == "BossProjectile":
                print("I hit a boss projectile")
            if str(hits[0].__class__.__name__) == "Mob":
                print("I hit a mob")
            if str(hits[0].__class__.__name__) == "MobProjectile":
                print("I hit a mob projectile")
            if str(hits[0].__class__.__name__) == "Wall":
                print("I hit a wall")
    def update(self):
        self.rect.x += self.vx * (self.game.projectileSpeed + 3)
        self.rect.y += self.vy * (self.game.projectileSpeed + 3)
        if (self.rect.x < 0 or self.rect.x > WIDTH or
            self.rect.y < 0 or self.rect.y > HEIGHT):
            self.kill() 
        # Collision:
        self.collide_with_stuff(self.game.all_bosses, False)
        self.collide_with_stuff(self.game.all_bossprojectiles, True)
        self.collide_with_stuff(self.game.all_mobs, True)
        self.collide_with_stuff(self.game.all_mobprojectiles, True)
        self.collide_with_stuff(self.game.all_walls, True)

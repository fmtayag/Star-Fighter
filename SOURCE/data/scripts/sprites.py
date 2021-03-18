import pygame
import pygame.math as pygmath
import math
from data.scripts.settings import *

# Player =====================================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill("RED")
        self.rect = self.image.get_rect()
        self.position = pygmath.Vector2(WIN_RES["w"]/2,WIN_RES["h"]*0.9)
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y
        self.velocity = pygmath.Vector2(0,0)
        self.speed = 225
        self.gun_level = 3
        
        # Managers
        self.attack_manager = PlayerAttackManager(self)

    def update(self, dt, sprites):
        self.velocity *= 0

        keyspressed = pygame.key.get_pressed()
        self.move(keyspressed)
        self.attack_manager.update(sprites, keyspressed)
        self.check_bounds()

        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

    def move(self, keyspressed):
        if keyspressed[pygame.K_UP]:
            self.velocity.y = -self.speed
        if keyspressed[pygame.K_DOWN]:
            self.velocity.y = self.speed 
        if keyspressed[pygame.K_LEFT]:
            self.velocity.x = -self.speed 
        if keyspressed[pygame.K_RIGHT]:
            self.velocity.x = self.speed

    def check_bounds(self):
        if self.rect.right > WIN_RES["w"]:
            self.rect.right = WIN_RES["w"]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > WIN_RES["h"]:
            self.rect.bottom = WIN_RES["h"]
        if self.rect.top < 0:
            self.rect.top = 0

class PlayerAttackManager:
    def __init__(self, player):
        self.player = player
        self.shoot_delay = 125
        self.shoot_timer = pygame.time.get_ticks()
        self.bullet_increase_delay = 50
        self.bullet_increase_timer = 0
        self.bullet_increase_tick = 25
        self.weak_bullet_delay = 250
        self.weak_bullet_timer = pygame.time.get_ticks()
        self.weak_bullet_tick = 10

    def update(self, sprites, keyspressed):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            if keyspressed[pygame.K_z]:
                if self.bullet_increase_timer >= self.bullet_increase_delay * 2 and self.player.gun_level == 3:
                    self.attack3(sprites)
                elif self.bullet_increase_timer >= self.bullet_increase_delay and self.player.gun_level >= 2:
                    self.attack2(sprites)
                else:
                    self.attack1(sprites)
                self.bullet_increase_timer += self.bullet_increase_tick
            else:
                self.bullet_increase_timer = 0

    def attack1(self, sprites):
        sprites.add(PlayerStrongBullet(pygmath.Vector2(self.player.rect.centerx, self.player.rect.top), pygmath.Vector2(0, self.player.speed)))

    def attack2(self, sprites):
        sprites.add(PlayerStrongBullet(pygmath.Vector2(self.player.rect.centerx-8, self.player.rect.top), pygmath.Vector2(0, self.player.speed)))
        sprites.add(PlayerStrongBullet(pygmath.Vector2(self.player.rect.centerx+8, self.player.rect.top), pygmath.Vector2(0, self.player.speed)))

    def attack3(self, sprites):
        sprites.add(PlayerStrongBullet(pygmath.Vector2(self.player.rect.centerx-8, self.player.rect.top), pygmath.Vector2(0, self.player.speed)))
        sprites.add(PlayerStrongBullet(pygmath.Vector2(self.player.rect.centerx+8, self.player.rect.top), pygmath.Vector2(0, self.player.speed)))

        # Spawn weak bullets
        now = pygame.time.get_ticks()
        if now - self.weak_bullet_timer > self.weak_bullet_delay:
            self.weak_bullet_timer = now
            sprites.add(PlayerWeakBullet(pygmath.Vector2(self.player.rect.centerx-16, self.player.rect.top-8), pygmath.Vector2(-16, self.player.speed)))
            sprites.add(PlayerWeakBullet(pygmath.Vector2(self.player.rect.centerx-16, self.player.rect.top), pygmath.Vector2(-16, self.player.speed)))
            sprites.add(PlayerWeakBullet(pygmath.Vector2(self.player.rect.centerx+16, self.player.rect.top), pygmath.Vector2(32, self.player.speed)))
            sprites.add(PlayerWeakBullet(pygmath.Vector2(self.player.rect.centerx+16, self.player.rect.top-8), pygmath.Vector2(32, self.player.speed)))
        
class PlayerStrongBullet(pygame.sprite.Sprite):
    def __init__(self, position, pspeed):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill("GREEN")
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.bottom = position.y
        self.velocity = pygmath.Vector2(0,0)
        self.speed = pspeed*2.5
        self.damage = 1

    def update(self, dt, sprites):
        self.velocity.x = self.speed.x
        self.velocity.y = -self.speed.y
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        if self.rect.bottom < 0:
            self.kill()

class PlayerWeakBullet(pygame.sprite.Sprite):
    def __init__(self, position, pspeed):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill("ORANGE")
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.bottom = position.y
        self.velocity = pygmath.Vector2(0,0)
        self.speed = pspeed*2.5
        self.damage = 0.5

    def update(self, dt, sprites):
        self.velocity.x = self.speed.x
        self.velocity.y = -self.speed.y
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        if self.rect.bottom < 0:
            self.kill()

# Fighter ====================================

class EnemyFighter(pygame.sprite.Sprite):
    def __init__(self, position, dest, speed):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill("RED")
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.dest = dest
        self.velocity = pygmath.Vector2(0,0)
        self.speed = speed
        self.pos = position

        self.dist = 0
        self.dx = 0
        self.dy = 0
        self.travelling = False

    def update(self, dt, sprites):
        self.travel(dt)

    def travel(self, dt):
        if not self.travelling:
            pos_x = self.rect.x
            pos_y = self.rect.y 
            dest_x = self.dest.x
            dest_y = self.dest.y
            radians = math.atan2(dest_y-pos_y, dest_x-pos_x)
            self.dist = math.hypot(dest_x-pos_x, dest_y-pos_y) / (self.speed/100)
            self.dist = int(self.dist)
            self.dx = math.cos(radians) * (self.speed/100)
            self.dy = math.sin(radians) * (self.speed/100)
            self.travelling = True

        if self.dist:
            self.dist -= 1
            self.pos.x += self.dx
            self.pos.y += self.dy
            print(self.dx)

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
import pygame
import pygame.math
Vec2 = pygame.math.Vector2
import math
from data.scripts.settings import *

# Player =====================================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill("RED")
        self.rect = self.image.get_rect()
        self.rect.x = WIN_RES["w"]*0.3
        self.rect.y = WIN_RES["h"]*0.9
        self.position = Vec2(self.rect.x,self.rect.y)
        self.velocity = Vec2(0,0)
        self.speed = 225
        self.gun_level = 3
        
        # Managers
        self.attack_manager = PlayerAttackManager(self)

    def update(self, dt, sprites):
        self.velocity *= 0

        keyspressed = pygame.key.get_pressed()
        self.move(keyspressed)
        self.attack_manager.update(sprites, keyspressed)

        self.position += self.velocity * dt 
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.check_bounds()

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
            self.position.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0 
            self.position.x = self.rect.x
        if self.rect.bottom > WIN_RES["h"]:
            self.rect.bottom = WIN_RES["h"]
            self.position.y = self.rect.y 
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.y

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
        sprites.add(PlayerStrongBullet(Vec2(self.player.rect.centerx, self.player.rect.top), Vec2(0, -self.player.speed)))

    def attack2(self, sprites):
        sprites.add(PlayerStrongBullet(Vec2(self.player.rect.centerx-8, self.player.rect.top), Vec2(0, -self.player.speed)))
        sprites.add(PlayerStrongBullet(Vec2(self.player.rect.centerx+8, self.player.rect.top), Vec2(0, -self.player.speed)))

    def attack3(self, sprites):
        sprites.add(PlayerStrongBullet(Vec2(self.player.rect.centerx-8, self.player.rect.top), Vec2(0, -self.player.speed)))
        sprites.add(PlayerStrongBullet(Vec2(self.player.rect.centerx+8, self.player.rect.top), Vec2(0, -self.player.speed)))

        # Spawn weak bullets
        now = pygame.time.get_ticks()
        if now - self.weak_bullet_timer > self.weak_bullet_delay:
            self.weak_bullet_timer = now
            sprites.add(PlayerWeakBullet(Vec2(self.player.rect.centerx-16, self.player.rect.top-16), Vec2(-32, self.player.speed)))
            sprites.add(PlayerWeakBullet(Vec2(self.player.rect.centerx+16, self.player.rect.top-16), Vec2(32, self.player.speed)))
        
class PlayerStrongBullet(pygame.sprite.Sprite):
    def __init__(self, position, velocity):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill("GREEN")
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.bottom = position.y
        self.position = Vec2(self.rect.centerx, self.rect.bottom)
        self.velocity = Vec2(velocity.x, velocity.y*2.5)
        self.damage = 1

    def update(self, dt, sprites):
        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

        if self.rect.bottom < 0:
            self.kill()

class PlayerWeakBullet(pygame.sprite.Sprite):
    def __init__(self, position, velocity):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill("CYAN")
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.bottom = position.y
        self.position = Vec2(self.rect.centerx, self.rect.bottom)
        self.velocity = Vec2(velocity.x, -velocity.y*3)
        self.damage = 0.5

    def update(self, dt, sprites):
        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

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
        self.velocity = Vec2(0,0)
        self.speed = speed
        self.position = position

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
            self.dist = math.hypot(dest_x-pos_x, dest_y-pos_y)
            self.dist = int(self.dist)
            self.dx = math.cos(radians)
            self.dy = math.sin(radians)
            self.travelling = True

        if self.dist >= 0:
            # TODO - this kinda works, i guess??
            self.dist -= 1
            self.position.x += self.dx
            self.position.y += self.dy

        self.rect.x = self.position.x
        self.rect.y = self.position.y
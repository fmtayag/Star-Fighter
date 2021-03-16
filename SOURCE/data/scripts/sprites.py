import pygame
import pygame.math as pygmath
from data.scripts.settings import *

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
        self.speed = 200

        # Shooting
        self.shoot_delay = 50
        self.shoot_timer = pygame.time.get_ticks()

    def update(self, dt, sprites):
        self.velocity *= 0

        keyspressed = pygame.key.get_pressed()
        self.move(keyspressed)
        self.shoot(keyspressed, sprites)
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

    def shoot(self, keyspressed, sprites):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            if keyspressed[pygame.K_z]:
                sprites.add(PlayerBullet(pygmath.Vector2(self.rect.centerx-16, self.rect.top-16), self.speed))
                sprites.add(PlayerBullet(pygmath.Vector2(self.rect.centerx, self.rect.top-32), self.speed))
                sprites.add(PlayerBullet(pygmath.Vector2(self.rect.centerx+16, self.rect.top-16), self.speed))

    def check_bounds(self):
        if self.rect.right > WIN_RES["w"]:
            self.rect.right = WIN_RES["w"]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > WIN_RES["h"]:
            self.rect.bottom = WIN_RES["h"]
        if self.rect.top < 0:
            self.rect.top = 0
        
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, position, pspeed):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill("GREEN")
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.top = position.y
        self.velocity = pygmath.Vector2(0,0)
        self.speed = pspeed*2.5

    def update(self, dt, sprites):
        self.velocity.y = -self.speed
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

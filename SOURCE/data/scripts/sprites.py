import pygame
import pygame.math as pygmath
from data.scripts.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32,32))
        self.image.fill("RED")
        self.rect = self.image.get_rect()
        self.position = pygmath.Vector2(WIN_RES["w"]/2-self.image.get_width()/2,WIN_RES["h"]*0.8)
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y
        self.velocity = pygmath.Vector2(0,0)
        self.speed = 250

    def update(self, dt):
        self.velocity *= 0

        self.move()
        self.check_bounds()

        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

    def move(self):
        keyspressed = pygame.key.get_pressed()
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
        
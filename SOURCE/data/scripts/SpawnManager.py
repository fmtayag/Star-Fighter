import pygame
import pygame.math as pygmath
Vec2 = pygame.math.Vector2
import random as rand
from data.scripts.settings import *
from data.scripts.sprites import *

class SpawnManager:
    def __init__(self, enemies_sg):
        self.enemies_sg = enemies_sg
        self.spawn_delay = 1000
        self.spawn_timer = pygame.time.get_ticks()

    def update(self, sprites):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = now
            pass

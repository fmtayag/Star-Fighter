import pygame
import pygame.math as pygmath
Vec2 = pygame.math.Vector2
import random as rand
from data.scripts.settings import *
from data.scripts.sprites import *

class SpawnManager:
    def __init__(self):
        self.spawn_delay = 1000
        self.spawn_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = now
            h = Hellfighter(
                Vec2(100,100),
                Vec2(100,0)
            )
            hostiles_g.add(h)
            all_sprites_g.add(h)

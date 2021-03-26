import pygame
import pygame.math as pygmath
Vec2 = pygame.math.Vector2
import random
from data.scripts.settings import *
from data.scripts.sprites import *

class SpawnManager:
    def __init__(self, player):
        self.spawn_delay = 1000
        self.spawn_timer = pygame.time.get_ticks()
        self.player = player
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.spawn_hellfighter()
                elif event.key == pygame.K_2:
                    self.spawn_netherdrone()
                elif event.key == pygame.K_3:
                    self.spawn_solturret()

    def update(self):
        pass

    def spawn_netherdrone(self):
        e = Netherdrone(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
            Vec2(0,0),
            self.player
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)
            
    def spawn_hellfighter(self):
        e = Helleye(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
            Vec2(0,0),
            self.player
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_solturret(self):
        e = Solturret(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
            Vec2(0,0),
            self.player
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)


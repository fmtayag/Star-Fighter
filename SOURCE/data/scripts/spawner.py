import pygame
import pygame.math
import random
from data.scripts.settings import *
from data.scripts.sprites import *

Vec2 = pygame.math.Vector2

class Spawner:
    def __init__(self, player, g_diff):
        self.spawn_delay = 1000
        self.spawn_timer = pygame.time.get_ticks()
        self.player = player
        self.g_diff = g_diff
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.spawn_helleye()
                elif event.key == pygame.K_2:
                    self.spawn_hellfighter()
                elif event.key == pygame.K_3:
                    self.spawn_solturret()
                elif event.key == pygame.K_4:
                    self.spawn_fatty()
                elif event.key == pygame.K_5:
                    self.spawn_raider()

    def update(self):
        pass

    def spawn_hellfighter(self):
        e = Hellfighter(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)
            
    def spawn_helleye(self):
        e = Helleye(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_solturret(self):
        e = Solturret(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_fatty(self):
        e = Fatty(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/4)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_raider(self):
        e = Raider(
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/4)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)
 


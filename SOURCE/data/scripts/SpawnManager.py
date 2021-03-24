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

    def update(self):
        pass
            
    def spawn_hellfighter(self):
        tries = 0
        while True:
            h = Helleye(
                Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/2)),
                Vec2(0,0),
                self.player
            )
            has_overlap = pygame.sprite.spritecollide(h, hostiles_g, False, collided=pygame.sprite.collide_rect_ratio(4))
            if not has_overlap:
                hostiles_g.add(h)
                all_sprites_g.add(h)
                break
            else:
                if tries < 10:
                    tries += 1
                    continue
                else:
                    break


import pygame
import pygame.math as pygmath
import random as rand
from data.scripts.settings import *
from data.scripts.sprites import EnemyFighter

class SpawnManager:
    def __init__(self):
        pass

    def update(self, sprites):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_q]:
            sprites.add(
                EnemyFighter(
                    pygmath.Vector2(32,WIN_RES["h"]/2),
                    pygmath.Vector2(WIN_RES["w"]/2,WIN_RES["h"]*0.3),
                    200
                )
            )
            sprites.add(
                EnemyFighter(
                    pygmath.Vector2(32,WIN_RES["h"]/2),
                    pygmath.Vector2(WIN_RES["w"]/4,WIN_RES["h"]*0.5),
                    310
                )
            )
            sprites.add(
                EnemyFighter(
                    pygmath.Vector2(32,WIN_RES["h"]/2),
                    pygmath.Vector2(WIN_RES["w"]/3,WIN_RES["h"]*0.7),
                    350
                )
            )
            sprites.add(
                EnemyFighter(
                    pygmath.Vector2(32,WIN_RES["h"]/2),
                    pygmath.Vector2(WIN_RES["w"]/6,WIN_RES["h"]*0.35),
                    100
                )
            )
            sprites.add(
                EnemyFighter(
                    pygmath.Vector2(32,WIN_RES["h"]/2),
                    pygmath.Vector2(WIN_RES["w"]/4.5,WIN_RES["h"]*0.54),
                    125
                )
            )

import pygame, random
import pygame.math
from data.scripts.settings import *
from data.scripts.sprites import *
from data.scripts.muda import load_img

Vec2 = pygame.math.Vector2

class Spawner:
    def __init__(self, player, g_diff):
        self.spawn_delay = 1000
        self.spawn_timer = pygame.time.get_ticks()
        self.player = player
        self.g_diff = g_diff

        # ENEMY IMAGES
        self.HELLFIGHTER_IMAGES = [
            load_img("hellfighter1.png", IMG_DIR, SCALE),
            load_img("hellfighter2.png", IMG_DIR, SCALE)
        ]
        self.FATTY_IMAGES = [
            load_img("fatty1.png", IMG_DIR, SCALE),
            load_img("fatty2.png", IMG_DIR, SCALE)
        ]
        self.RAIDER_IMAGES = [
            load_img("raider1.png", IMG_DIR, SCALE),
            load_img("raider2.png", IMG_DIR, SCALE)
        ]
        self.HELLEYE_IMAGES = [
            load_img("helleye1.png", IMG_DIR, SCALE),
            load_img("helleye2.png", IMG_DIR, SCALE)
        ]
        self.SOLTURRET_IMAGES = [
            load_img("solturret1.png", IMG_DIR, SCALE),
            load_img("solturret2.png", IMG_DIR, SCALE)
        ]

        # BULLET IMAGES
        self.SMALL_BULLET_IMAGE = load_img("bullet_enemy.png", IMG_DIR, SCALE)
        self.FATTY_BULLET_IMAGE = load_img("bullet_fatty.png", IMG_DIR, SCALE)
        self.FATTY_BULLETS_IMAGES = {"LARGE": self.FATTY_BULLET_IMAGE, "SMALL": self.SMALL_BULLET_IMAGE}

        # POWERUP IMAGES
        self.POWERUP_IMAGES = {
            "GUN": [load_img("powerup_gun.png", IMG_DIR, SCALE)],
            "HEALTH": [load_img("powerup_health.png", IMG_DIR, SCALE)],
            "SCORE": [load_img("powerup_score.png", IMG_DIR, SCALE)],
            "SENTRY": [load_img("powerup_sentry.png", IMG_DIR, SCALE)]
        }

        # SENTRY IMAGES 
        self.SENTRY_IMAGES = {
            "BASE": load_img("sentry_base.png", IMG_DIR, SCALE),
            "GUN": load_img("sentry_gun.png", IMG_DIR, SCALE)
        }
        self.SENTRY_BULLET_IMAGE = load_img("bullet_sentry.png", IMG_DIR, SCALE)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.spawn_hellfighter()
                elif event.key == pygame.K_2:
                    self.spawn_fatty()
                elif event.key == pygame.K_3:
                    self.spawn_raider()
                elif event.key == pygame.K_4:
                    self.spawn_solturret()
                elif event.key == pygame.K_5:
                    self.spawn_helleye()
                elif event.key == pygame.K_6:
                    self.spawn_sentry()

    def update(self):
        pass

    def spawn_hellfighter(self):
        e = Hellfighter(
            self.HELLFIGHTER_IMAGES,
            self.SMALL_BULLET_IMAGE,
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/3)),
            self.player,
            self.g_diff
        ),
        hostiles_g.add(e)
        all_sprites_g.add(e)
    
    def spawn_fatty(self):
        e = Fatty(
            self.FATTY_IMAGES,
            self.FATTY_BULLETS_IMAGES,
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/4)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_raider(self):
        e = Raider(
            self.RAIDER_IMAGES,
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/4)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_helleye(self):
        e = Helleye(
            self.HELLEYE_IMAGES,
            self.SMALL_BULLET_IMAGE,
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/3)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_solturret(self):
        e = Solturret(
            self.SOLTURRET_IMAGES,
            self.SMALL_BULLET_IMAGE,
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/3)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        all_sprites_g.add(e)

    def spawn_powerup(self, position):
        pow_type = self.roll_powerup()
        pow_image = self.POWERUP_IMAGES[pow_type]
        p = Powerup(pow_image, position, pow_type, self.g_diff)
        powerups_g.add(p)
        all_sprites_g.add(p)

    def roll_powerup(self):
        type_choices = POWERUP_TYPES
        weights = POWERUP_TYPES_WEIGHTS
        pow_choices = random.choices(type_choices, weights)
        pow_type = pow_choices[0]

        return pow_type

    def spawn_sentry(self):
        s = Sentry(
            self.SENTRY_IMAGES, 
            self.SENTRY_BULLET_IMAGE, 
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(WIN_RES["h"]/2, WIN_RES["h"]-64))
        )
        sentries_g.add(s)
        all_sprites_g.add(s)


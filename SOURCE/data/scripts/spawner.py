import pygame, random
import pygame.math
from data.scripts.sprites import *
from data.scripts.muda import load_img, image_at, scale_rect

Vec2 = pygame.math.Vector2

class Spawner:
    def __init__(self, player, g_diff):
        # Spawner defines 
        self.spawn_timer = pygame.time.get_ticks()
        self.player = player
        self.g_diff = g_diff
        self.current_stage = GAME_STAGES[0]
        
        # HELLFIGHTER IMAGES ==================
        HELLFIGHTER_SPRITESHEET = load_img("hellfighter_sheet.png", IMG_DIR, SCALE)
        self.HELLFIGHTER_IMAGES = {
            "NORMAL": [
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
            ],
            "SPAWNING": [
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(HELLFIGHTER_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ]
        }

        # RAIDER IMAGES =======================
        RAIDER_SPRITESHEET = load_img("raider_sheet.png", IMG_DIR, SCALE)
        self.RAIDER_IMAGES = {
            "NORMAL": [
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
            ],
            "SPAWNING": [
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(RAIDER_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ]
        }

        # FATTY IMAGES =======================-
        FATTY_SPRITESHEET = load_img("fatty_sheet.png", IMG_DIR, SCALE)
        self.FATTY_IMAGES = {
            "NORMAL": [
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
            ],
            "SPAWNING": [
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(FATTY_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ]
        }

        # HELLEYE IMAGES ======================
        HELLEYE_SPRITESHEET = load_img("helleye_sheet.png", IMG_DIR, SCALE)
        self.HELLEYE_IMAGES = {
            "NORMAL": [
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
            ],
            "SPAWNING": [
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(HELLEYE_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ]
        }

        # SOLTURRET IMAGES ====================
        SOLTURRET_SPRITESHEET = load_img("solturret_sheet.png", IMG_DIR, SCALE)
        SOLTURRET_NORMAL_IMAGES = {
            "GUN": [
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
            ],
            "BASE": [
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ]
        }
        self.SOLTURRET_IMAGES = {
            "NORMAL": SOLTURRET_NORMAL_IMAGES,
            "SPAWNING": [
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [0,32,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [16,32,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [32,32,16,16]), True),
                image_at(SOLTURRET_SPRITESHEET, scale_rect(SCALE, [48,32,16,16]), True)
            ]
        }

        # BULLET IMAGES =======================
        BULLET_SPRITESHEET = load_img("bullet_sheet.png", IMG_DIR, SCALE)
        self.LARGE_BULLET_IMAGE = image_at(BULLET_SPRITESHEET, scale_rect(SCALE, [0,0,10,10]), True)
        self.SMALL_BULLET_IMAGE = image_at(BULLET_SPRITESHEET, scale_rect(SCALE, [8,8,8,8]), True)
        self.FATTY_BULLETS_IMAGES = {
            "LARGE": self.LARGE_BULLET_IMAGE, 
            "SMALL": self.SMALL_BULLET_IMAGE
        }
        self.SENTRY_BULLET_IMAGE = image_at(BULLET_SPRITESHEET, scale_rect(SCALE, [24,0,8,8]), True)

        # POWERUP IMAGES ======================
        POWERUP_SPRITESHEET = load_img("powerup_sheet.png", IMG_DIR, SCALE)
        self.POWERUP_IMAGES = {
            "GUN": [
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
            ],
            "HEALTH": [
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [0,32,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [16,32,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [32,32,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [48,32,16,16]), True)
            ],
            "SCORE": [
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [0,48,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [16,48,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [32,48,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [48,48,16,16]), True)
            ],
            "SENTRY": [
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(POWERUP_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ]
        }

        # SENTRY IMAGES =======================
        SENTRY_SPRITESHEET = load_img("sentry_sheet.png", IMG_DIR, SCALE)
        self.SENTRY_IMAGES = {
            "SPAWNING": [
                image_at(SENTRY_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                image_at(SENTRY_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                image_at(SENTRY_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                image_at(SENTRY_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
            ],
            "BASE": image_at(SENTRY_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
            "GUN": image_at(SENTRY_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True)
        }

        # EXPLPOSION IMAGES ===================
        EXPLOSION_SPRITESHEET = load_img("explosion_sheet.png", IMG_DIR, SCALE)
        self.EXPLOSION_IMAGES = {
            "BIG": {
                "VAR1": [
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
                ],
                "VAR2": [
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
                ],
                "VAR3": [
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [0,32,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [16,32,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [32,32,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [48,32,16,16]), True)
                ]
            },
            "SMALL": {
                "VAR1": [
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [0,48,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [16,48,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [32,48,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [48,48,16,16]), True)
                ],
                "VAR2": [
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [0,64,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [16,64,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [32,64,16,16]), True),
                    image_at(EXPLOSION_SPRITESHEET, scale_rect(SCALE, [48,64,16,16]), True)
                ]
            }
        }
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if DEBUG_MODE:
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
                    elif event.key == pygame.K_7:
                        self.spawn_explosion()

    def update(self, score):
        # Update current game stage
        if score >= LATE_STAGE_SCORE_TRIGGER[self.g_diff]:
            self.current_stage = GAME_STAGES[2]
        elif score >= MID_STAGE_SCORE_TRIGGER[self.g_diff]:
            self.current_stage = GAME_STAGES[1]
        else:
            self.current_stage = GAME_STAGES[0]

        # Spawn enemies 
        if len(hostiles_g) < MAX_ENEMY_COUNT[self.current_stage]:
            now = pygame.time.get_ticks()
            if now - self.spawn_timer > SPAWN_DELAY[self.current_stage]:
                self.spawn_timer = now

                # Roll
                roll_list = SPAWN_ROLLS[self.current_stage]
                roll_weights = SPAWN_WEIGHTS[self.current_stage]
                roll_choice = random.choices(roll_list, roll_weights)[0]
                
                # Spawn the rolled enemy
                if roll_choice == "HELLFIGHTER":
                    self.spawn_hellfighter()
                elif roll_choice == "RAIDER":
                    self.spawn_raider()
                elif roll_choice == "FATTY":
                    self.spawn_fatty()
                elif roll_choice == "SOLTURRET":
                    # Count number of solturrets
                    count = 0
                    for sprite in hostiles_g:
                        if type(sprite) == Solturret:
                            count += 1

                    # Spawn
                    if count < MAX_SOLTURRET_COUNT:
                        self.spawn_solturret()
                    else:
                        self.spawn_hellfighter()

                elif roll_choice == "HELLEYE":
                    # Count number of helleye
                    count = 0
                    for sprite in hostiles_g:
                        if type(sprite) == Helleye:
                            count += 1

                    # Spawn
                    if count < MAX_HELLEYE_COUNT:
                        self.spawn_helleye()
                    else:
                        self.spawn_fatty()

    def spawn_hellfighter(self):
        e = Hellfighter(
            self.HELLFIGHTER_IMAGES,
            self.SMALL_BULLET_IMAGE,
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(32,WIN_RES["h"]/3)),
            self.player,
            self.g_diff
        )
        hostiles_g.add(e)
        hellfighters_g.add(e)
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
        weights = POWERUP_TYPES_WEIGHTS[self.current_stage]
        pow_choices = random.choices(type_choices, weights)
        pow_type = pow_choices[0]

        if pow_type == "SENTRY" and len(sentries_g) >= MAX_SENTRY_COUNT - 1:
            pow_type = SUBSTITUTE_POWERUP
        elif pow_type == "HEALTH" and self.player.health >= HEALTH_PICKUP_HP_THRESHOLD:
            pow_type = SUBSTITUTE_POWERUP
        elif pow_type == "GUN" and self.player.gun_level >= PLAYER_MAX_GUN_LEVEL:
            pow_type = SUBSTITUTE_POWERUP

        return pow_type

    def spawn_sentry(self):
        s = Sentry(
            self.SENTRY_IMAGES, 
            self.SENTRY_BULLET_IMAGE, 
            Vec2(random.randrange(0, WIN_RES["w"]-32), random.randrange(WIN_RES["h"]/2, WIN_RES["h"]-64))
        )
        sentries_g.add(s)
        all_sprites_g.add(s)

    def spawn_explosion(self, position=Vec2(32,32), size="SMALL"):
        # Pick explosion images
        img_list = self.EXPLOSION_IMAGES[size]
        variant = random.sample(img_list.keys(), k=1)[0]
        pick = self.EXPLOSION_IMAGES[size][variant]

        # Create explosion object
        exp = Explosion(pick, position)
        all_sprites_g.add(exp)
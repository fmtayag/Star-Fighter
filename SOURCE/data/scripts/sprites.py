import pygame
import math
import random
import pygame.math
from data.scripts.defines import *
from data.scripts.muda import (
    SpriteState,
    SpriteStateManager,
    load_sound
)

Vec2 = pygame.math.Vector2

# PLAYER =======================================================================

class Player(pygame.sprite.Sprite):
    def __init__(self, images, bullet_image, P_Prefs):
        # Sprite defines
        super().__init__()
        self.P_Prefs = P_Prefs
        self.images = images
        self.image = pygame.Surface((32,32))
        self.image.set_colorkey("BLACK")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_RES["w"]*0.5
        self.rect.centery = WIN_RES["h"]*0.75
        self.position = Vec2(self.rect.x,self.rect.y)
        self.velocity = Vec2(0,0)
        self.radius = PLAYER_RADIUS

        # Settings
        self.speed = PLAYER_SPEED
        self.gun_level = PLAYER_DEFAULT_GUN_LEVEL
        self.prev_gunlv = PLAYER_DEFAULT_GUN_LEVEL
        self.health = PLAYER_HEALTH
        
        # For shooting
        self.BULLET_SPEED = PLAYER_BULLET_SPEED
        self.bullet_image = bullet_image
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.shoot_timer = pygame.time.get_ticks()
        self.bullet_increase_delay = PLAYER_INCREASE_BULLET_DELAY
        self.bullet_increase_timer = 0
        self.bullet_increase_tick = PLAYER_INCREASE_BULLET_TICK
        self.weak_bullet_delay = PLAYER_WEAK_BULLET_DELAY
        self.weak_bullet_timer = pygame.time.get_ticks()
        self.weak_bullet_tick = PLAYER_WEAK_BULLET_TICK
        self.BULLET_DAMAGE = PLAYER_BULLET_DAMAGE

        # States
        self.states_ = ("SPAWNING", "NORMAL", "LEVELUP")
        self.state_ = self.states_[0]

        # For animation
        self.imgdict_key = "SPAWNING"
        self.lvto = str() # x LEVEL TO y
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = 4
        self.orientations_ = ("FORWARD", "LEFT", "RIGHT")
        self.orientation_ = self.orientations_[0]

        # For flashing effect
        self._flash_delay = 300
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

        # Sounds
        self.sfx_shoot = load_sound("sfx_shoot.wav", SFX_DIR, self.P_Prefs.sfx_vol)
    
    def update(self, dt):
        if self.state_ == "NORMAL":
            # Reset velocity and image
            self.velocity *= 0
            self.orientation_ = "FORWARD"
            if self.gun_level >= PLAYER_MAX_GUN_LEVEL:
                self.gun_level = PLAYER_MAX_GUN_LEVEL
            
            # Run methods
            keyspressed = pygame.key.get_pressed()
            self._move(keyspressed)
            self._shoot(keyspressed)
            self._animate()

            # Update image
            self.image = self.images[self.imgdict_key][f"LV{self.gun_level}"][self.orientation_][self.current_frame]
            self._flash()

            # Update position
            self.position += self.velocity * dt 
            self.rect.x = self.position.x
            self.rect.y = self.position.y
            self._check_bounds()

            # Go to LEVELUP state
            if self.prev_gunlv != self.gun_level:
                self.lvto = f"{self.prev_gunlv}-{self.gun_level}"
                self.prev_gunlv = self.gun_level 
                self.current_frame = 0
                self.imgdict_key = "LEVELUP"

                self.state_ = self.states_[2]
        
        elif self.state_ == "LEVELUP":
            # Run methods
            self._animate()

            # Run methods
            keyspressed = pygame.key.get_pressed()
            self._move(keyspressed)
            self._shoot(keyspressed)
            self._animate()

            # Update image
            self.image = self.images[self.imgdict_key][self.lvto][self.current_frame]

            # Update position
            self.position += self.velocity * dt 
            self.rect.x = self.position.x
            self.rect.y = self.position.y
            self._check_bounds()

            # Go back to NORMAL state
            if self.current_frame == self.MAX_FRAMES - 1:
                self.current_frame = 0
                self.imgdict_key = "NORMAL"

                self.state_ = self.states_[1]

        elif self.state_ == "SPAWNING":
            # Run methods
            self._animate()

            # Update image
            self.image = self.images[self.imgdict_key][self.current_frame]

            # Change state...
            if self.current_frame == self.MAX_FRAMES - 1:
                self.current_frame = 0
                self.imgdict_key = "NORMAL"

                self.state_ = self.states_[1]

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
            points = pygame.mask.from_surface(self.images[self.imgdict_key][f"LV{self.gun_level}"][self.orientation_][self.current_frame]).outline()
            pygame.draw.polygon(flash_image,"WHITE",points,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0

    def _move(self, keyspressed):
        if keyspressed[self.P_Prefs.key_up]:
            self.velocity.y = -self.speed
        if keyspressed[self.P_Prefs.key_down]:
            self.velocity.y = self.speed
        if keyspressed[self.P_Prefs.key_left]:
            self.orientation_ = self.orientations_[1]
            self.velocity.x = -self.speed
        if keyspressed[self.P_Prefs.key_right]:
            self.orientation_ = self.orientations_[2]
            self.velocity.x = self.speed

    def _check_bounds(self):
        if self.rect.right > WIN_RES["w"]:
            self.rect.right = WIN_RES["w"]
            self.position.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0 
            self.position.x = self.rect.x
        if self.rect.bottom > WIN_RES["h"]:
            self.rect.bottom = WIN_RES["h"]
            self.position.y = self.rect.y 
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.y
    
    def _play_shoot_sound(self):
        self.sfx_shoot.play(loops=1, fade_ms=100) # Play sound

    def _shoot(self,  keyspressed):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            if keyspressed[self.P_Prefs.key_fire]:

                self._play_shoot_sound()

                if self.bullet_increase_timer >= self.bullet_increase_delay * 2 and self.gun_level == 3:
                    self._attack3()
                elif self.bullet_increase_timer >= self.bullet_increase_delay and self.gun_level >= 2:
                    self._attack2()
                else:
                    self._attack1()
                self.bullet_increase_timer += self.bullet_increase_tick
            else:
                self.bullet_increase_timer = 0

    def _attack1(self):
        b = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx, self.rect.top), Vec2(0, -self.BULLET_SPEED))
        all_sprites_g.add(b)
        p_bullets_g.add(b)

    def _attack2(self):
        b1 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx-10, self.rect.top+12), Vec2(0, -self.BULLET_SPEED))
        b2 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx+10, self.rect.top+12), Vec2(0, -self.BULLET_SPEED))
        all_sprites_g.add(b1)
        all_sprites_g.add(b2)
        p_bullets_g.add(b1)
        p_bullets_g.add(b2)

    def _attack3(self):
        b1 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx-10, self.rect.top+12), Vec2(-50, -self.BULLET_SPEED))
        b2 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx, self.rect.top+12), Vec2(0, -self.BULLET_SPEED))
        b3 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx+10, self.rect.top+12), Vec2(50, -self.BULLET_SPEED))
        all_sprites_g.add(b1)
        all_sprites_g.add(b2)
        all_sprites_g.add(b3)
        p_bullets_g.add(b1)
        p_bullets_g.add(b2)
        p_bullets_g.add(b3)
    
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, image, position, velocity):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.bottom = position.y
        self.position = Vec2(self.rect.centerx, self.rect.bottom)
        self.velocity = Vec2(velocity.x, velocity.y)
        self.radius = PLAYER_BULLET_RADIUS

    def update(self, dt):
        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

        if self.rect.bottom < 0:
            self.kill()

# ENEMIES ======================================================================

# BULLETS =====================================

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, image, position, velocity, damage):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.centery = position.y
        self.position = Vec2(self.rect.centerx, self.rect.bottom)
        self.velocity = Vec2(velocity)
        self.DAMAGE = damage
        self.radius = SMALL_BULLET_RADIUS

    def update(self, dt):
        # Kill if it goes out of bounds
        if (self.rect.top > WIN_RES["h"] or 
            self.rect.bottom < 0 or
            self.rect.right < 0 or
            self.rect.left > WIN_RES["w"]):
            self.kill()

        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

class FattyBullet(pygame.sprite.Sprite):
    def __init__(self, image, small_bullet_img, position, velocity, damage, sb_speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.centery = position.y
        self.position = Vec2(self.rect.centerx, self.rect.bottom)
        self.velocity = Vec2(velocity)
        self.radius = FATTY_BULLET_RADIUS

        self.DAMAGE = damage
        self.DECELERATE_SPEED = random.randrange(6,8)
        self.SMALL_BULLET_SPEED = sb_speed
        self.SMALL_BULLET_IMAGE = small_bullet_img

    def update(self, dt):
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        # Decelerate
        if self.velocity.y > 0:
            self.velocity.y -= self.DECELERATE_SPEED
        else:
            self._explode()

        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

        if self.rect.top > WIN_RES["h"] or self.rect.bottom < 0:
            self.kill()

    def _explode(self):
        for i in range(len(FATTY_BULLET_DIRECTION)):
            b = EnemyBullet(
                self.SMALL_BULLET_IMAGE,
                Vec2(self.rect.center),
                Vec2(
                        FATTY_BULLET_DIRECTION[i].x * FATTY_BULLET_SPEED_X[i] * self.SMALL_BULLET_SPEED, 
                        FATTY_BULLET_DIRECTION[i].y * FATTY_BULLET_SPEED_Y[i] * self.SMALL_BULLET_SPEED
                    ),
                self.DAMAGE
            )
            e_bullets_g.add(b)
            all_sprites_g.add(b)
        
        self.kill()

# HELLFIGHTER ENEMY ===========================

class Hellfighter(pygame.sprite.Sprite):
    def __init__(self, images, bullet_img, position, player, g_diff):
        # Settings
        self.player = player
        self.health = HELLFIGHTER_HEALTH[g_diff]
        self.SPEED = HELLFIGHTER_SPEED[g_diff]
        self.WORTH = SCORE_WORTH["HELLFIGHTER"]
        self.SPEED_WAITING = self.SPEED * 0.65

        # Sprite defines
        super().__init__()
        self.images = images.copy()
        self.image = self.images["SPAWNING"][0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x 
        self.rect.y = position.y 
        self.position = position
        self.velocity = Vec2(random.choice([-self.SPEED_WAITING, self.SPEED_WAITING]),0)
        self.radius = ENEMY_RADIUS

        # State machine
        self.states_ = ("SPAWNING", "FIGHTING", "WAITING")
        self.state_ = self.states_[0]
        
        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images["SPAWNING"]) # could be a constant. maybe 4.

        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.SHOOT_DELAY = HELLFIGHTER_SHOOT_DELAY[g_diff]
        self.RANGE = HELLFIGHTER_RANGE[g_diff] 
        self.BULLET_SPEED = HELLFIGHTER_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = HELLFIGHTER_BULLET_DAMAGE[g_diff]
        self.BULLET_IMAGE = bullet_img
    
        # For flashing effect
        self._flash_delay = 50
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

        # For behavior changing. Note: one could make a good argument that I should merge this into the states. 10:20am
                                # - but i'm too lazy to do it. 10:21am
                                # - well actually i just implemented it. 10:28am
        # self.behaviors = ("WAITING", "FOLLOWING")
        # self.behavior = self.behaviors[0]
        self.ch_behavior_delay = 100
        self.ch_behavior_timer = pygame.time.get_ticks()

    def update(self, dt):
        if self.state_ == "FIGHTING":
            # Run methods
            self._animate()
            self._follow_player()
            self._shoot()
            self._flash()

            # Update position
            self.position += self.velocity * dt 
            self.rect.x = self.position.x
            self.rect.y = self.position.y

            # Change state...
            self.ch_behavior()

        elif self.state_ == "WAITING":
            # Run methods
            self._animate()
            self._move()
            self._shoot()
            self._flash()

            # Update position
            self.position += self.velocity * dt 
            self.rect.x = self.position.x
            self.rect.y = self.position.y

            # Change state...
            self.ch_behavior()

        elif self.state_ == "SPAWNING":
            # Run methods
            self._animate()

            # Change state...
            if self.current_frame == self.MAX_FRAMES - 1:
                # Change images dictionary key
                self.imgdict_key = "NORMAL"
                
                self.state_ = self.ch_state_behav()

    def ch_state_behav(self):
        hf_following_exists = False
        for hellfighter in hellfighters_g:
            # Check if same instance
            if hellfighter is self:
                continue 
            
            if hellfighter.state_ == "FIGHTING":
                hf_following_exists = True

        if hf_following_exists:
            return "WAITING"
        else:
            return "FIGHTING"

    def ch_behavior(self):
        now = pygame.time.get_ticks()
        if now - self.ch_behavior_timer > self.ch_behavior_delay:
            self.ch_behavior_timer = now
            hf_following_exists = False

            for hellfighter in hellfighters_g:
                # Check if same instance
                if hellfighter is self:
                    continue 
                
                if hellfighter.state_ == "FIGHTING":
                    hf_following_exists = True

            if hf_following_exists:
                self.state_ = "WAITING"
            else:
                self.state_ = "FIGHTING"

    def _move(self):
        if self.rect.left < 0:
            self.velocity.x = self.SPEED_WAITING
        elif self.rect.right > WIN_RES["w"]:
            self.velocity.x = -self.SPEED_WAITING

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.imgdict_key][self.current_frame]

    def _follow_player(self):
        # Calculate delta-x
        rel_y = self.rect.y - self.player.rect.y
        rel_x = self.rect.x - self.player.rect.x
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)

    def _shoot(self):
        # Calculate radians
        rel_y = self.rect.centery - self.player.rect.centery
        rel_x = self.rect.centerx - self.player.rect.centerx
        radians = math.atan2(rel_y, rel_x)

        # Calculate x-component
        x_com = math.cos(radians)

        # Only shoot if in range
        if x_com > -self.RANGE and x_com < self.RANGE:
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > self.SHOOT_DELAY:
                self.shoot_timer = now

                # Calculate vertical direction
                dir_y = -(math.copysign(1, math.sin(radians)))

                b = EnemyBullet(
                    self.BULLET_IMAGE,
                    Vec2(self.rect.center),
                    Vec2(-x_com * (self.BULLET_SPEED / 2), self.BULLET_SPEED * dir_y),
                    self.BULLET_DAMAGE
                )
                e_bullets_g.add(b)
                all_sprites_g.add(b)

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
            points = pygame.mask.from_surface(self.images[self.imgdict_key][self.current_frame]).outline()
            pygame.draw.polygon(flash_image,"WHITE",points,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

# FATTY ENEMY =================================

class Fatty(pygame.sprite.Sprite):
    def __init__(self, images, bullet_imgs, position, player, g_diff):
        # Settings
        self.player = player
        self.health = FATTY_HEALTH[g_diff]
        self.SPEED = FATTY_SPEED[g_diff]
        self.WORTH = SCORE_WORTH["FATTY"]

        # Sprite defines
        super().__init__()
        self.images = images
        self.image = self.images["SPAWNING"][0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.velocity = Vec2(random.choice([-self.SPEED, self.SPEED]),0)
        self.radius = ENEMY_RADIUS

        # States
        self.states_ = ("SPAWNING", "NORMAL")
        self.state_ = self.states_[0]

        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images[self.imgdict_key])
        self.bob_y = -2 # For bobbing effect

        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.SHOOT_DELAY = FATTY_SHOOT_DELAY[g_diff]
        self.BULLET_SPEED = FATTY_LARGE_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = FATTY_BULLET_DAMAGE[g_diff]
        self.SMALL_BULLET_SPEED = FATTY_SMALL_BULLET_SPEED[g_diff]
        self.BULLET_IMAGES = bullet_imgs
        self.LARGE_BULLET_IMAGE = self.BULLET_IMAGES["LARGE"]
        self.SMALL_BULLET_IMAGE = self.BULLET_IMAGES["SMALL"]

        # For flashing effect
        self._flash_delay = 50
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

    def update(self, dt):
        if self.state_ == "NORMAL":
            # Run methods
            self._animate()
            self._move()
            self.bob()
            self._shoot()
            self._flash() 

            # Update position
            self.position += self.velocity * dt 
            self.rect.x = self.position.x
            self.rect.y = self.position.y

        elif self.state_ == "SPAWNING":
            # Run methods
            self._animate()

            # Change state...
            if self.current_frame == self.MAX_FRAMES - 1:
                # Change images dictionary key
                self.imgdict_key = "NORMAL"

                self.state_ = self.states_[1]

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.imgdict_key][self.current_frame]

    def _move(self):
        if self.rect.left < 0:
            self.velocity.x = self.SPEED
        elif self.rect.right > WIN_RES["w"]:
            self.velocity.x = -self.SPEED

    def bob(self):
        self.velocity.y = math.sin(self.bob_y) * 50
        self.bob_y += 0.1
        
    def _shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.SHOOT_DELAY:
            self.shoot_timer = now

            b = FattyBullet(
                self.LARGE_BULLET_IMAGE,
                self.SMALL_BULLET_IMAGE,
                Vec2(self.rect.centerx, self.rect.bottom),
                Vec2(0,self.BULLET_SPEED),
                self.BULLET_DAMAGE,
                self.SMALL_BULLET_SPEED
            )
            e_bullets_g.add(b)
            all_sprites_g.add(b)

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
            points = pygame.mask.from_surface(self.images[self.imgdict_key][self.current_frame]).outline()
            pygame.draw.polygon(flash_image,"WHITE",points,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

# RAIDER ENEMY ================================

class Raider(pygame.sprite.Sprite):
    def __init__(self, images, position, player, g_diff):
        # Sprite defines
        super().__init__()
        self.images = images
        self.image = self.images["SPAWNING"][0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.velocity = Vec2(0,0)
        self.radius = ENEMY_RADIUS

        # Settings
        self.player = player
        self.health = RAIDER_HEALTH[g_diff]
        self.SPEED = RAIDER_SPEED[g_diff]
        self.DASH_RANGE = RAIDER_DASH_RANGE[g_diff]
        self.MAX_DASH_SPEED = RAIDER_MAX_SPEED[g_diff]
        self.WORTH = SCORE_WORTH["RAIDER"]

        # For dashing
        self.target_acquired = False
        self.dash_x = -2

        # States
        self.states_ = ("SPAWNING", "NORMAL", "DASHING")
        self.state_ = self.states_[0]

        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images[self.imgdict_key])

        # For flashing effect
        self._flash_delay = 100
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

    def update(self, dt):
        if self.state_ == "NORMAL":
            # Run methods
            self._animate()
            self._follow_player()
            self._flash()

            # Update position
            self.position += self.velocity * dt
            self.rect.x = self.position.x
            self.rect.y = self.position.y
        
            # Change state...
            if self.target_acquired:
                self.state_ = self.states_[2]

        elif self.state_ == "DASHING":
            # Run methods
            self._animate()
            self._dash()
            self._flash()
            if self.velocity.y >= 0:
                self._spawn_gas()
            
            # Kill if it goes out of bounds
            if self.rect.top > WIN_RES["h"]:
                self.kill()

            # Update position
            self.position += self.velocity * dt
            self.rect.x = self.position.x
            self.rect.y = self.position.y

        elif self.state_ == "SPAWNING":
            # Change image dictionary's key
            self.imgdict_key = "SPAWNING"

            # Run methods
            self._animate()

            # Change state....
            if self.current_frame == self.MAX_FRAMES - 1:
                # Change image dictionary's key
                self.imgdict_key = "NORMAL"

                self.state_ = self.states_[1]

    def _spawn_gas(self):
        # Spawn gas trail
        c_color = random.choice(EP_COLORS)
        ep = Particle(
            Vec2(
                self.position.x,
                self.position.y
            ),
            Vec2(
                random.randrange(-100,100), 
                -self.velocity.y / 2
            ),
            c_color
        )
        all_sprites_g.add(ep)

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.imgdict_key][self.current_frame]

    def _follow_player(self):
        # Calculate delta-x
        rel_x = self.rect.x - self.player.rect.x
        rel_y = self.rect.y - self.player.rect.y
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)
        if dx > -self.DASH_RANGE and dx < self.DASH_RANGE:
            self.target_acquired = True

    def _dash(self):
        if self.velocity.y < self.MAX_DASH_SPEED:
            self.velocity.y += math.pow(self.dash_x, 3)
            self.dash_x += 0.1

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((32,32))
            olist = pygame.mask.from_surface(self.images[self.imgdict_key][self.current_frame]).outline()
            pygame.draw.polygon(flash_image,"WHITE",olist,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

# HELLEYE ENEMY ===============================

class Helleye(pygame.sprite.Sprite):
    def __init__(self, images, bullet_img, position, player, g_diff):
        # Sprite defines
        super().__init__()
        self.images = images
        self.image = self.images["SPAWNING"][0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.velocity = Vec2(0,0)
        self.radius = ENEMY_RADIUS

        # Settings
        self.player = player
        self.health = HELLEYE_HEALTH[g_diff]
        self.SPEED = HELLEYE_SPEED[g_diff]
        self.WORTH = SCORE_WORTH["HELLEYE"]

        # State machine
        self.states_ = ("SPAWNING", "NORMAL")
        self.state_ = self.states_[0]

        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images[self.imgdict_key])
    
        # For shooting
        self.SHOOT_DELAY = HELLEYE_SHOOT_DELAY[g_diff]
        self.BULLET_SPEED = HELLEYE_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = HELLEYE_BULLET_DAMAGE[g_diff]
        self.shoot_timer = pygame.time.get_ticks()
        self.BULLET_IMAGE = bullet_img
    
        # For flashing effect
        self._flash_delay = 50
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

    def update(self, dt):
        if self.state_ == "NORMAL":
            # Run methods
            self._animate()
            self._follow_player()
            self._shoot()
            self._flash()

            # Update position
            self.position += self.velocity * dt 
            self.rect.x = self.position.x
            self.rect.y = self.position.y

        elif self.state_ == "SPAWNING":
            # Run methods
            self._animate()

            # Change state
            if self.current_frame >= self.MAX_FRAMES - 1:
                # Set image dictionary's key
                self.imgdict_key = "NORMAL"

                self.state_ = self.states_[1]

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.imgdict_key][self.current_frame]

    def _follow_player(self):
        # Calculate delta-x
        rel_y = self.rect.y - self.player.rect.y
        rel_x = self.rect.x - self.player.rect.x
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)

    def _shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.SHOOT_DELAY:
            self.shoot_timer = now

            for i in range(len(HELLEYE_BULLET_DIRECTION)):
                b = EnemyBullet(
                    self.BULLET_IMAGE,
                    Vec2(self.rect.center),
                    Vec2(HELLEYE_BULLET_DIRECTION[i] * self.BULLET_SPEED),
                    self.BULLET_DAMAGE
                )
                e_bullets_g.add(b)
                all_sprites_g.add(b)

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
            points = pygame.mask.from_surface(self.images[self.imgdict_key][self.current_frame]).outline()
            pygame.draw.polygon(flash_image,"WHITE",points,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

# SOLTURRET ENEMY =============================

class Solturret(pygame.sprite.Sprite): 
    def __init__(self, images, bullet_img, position, player, g_diff):
        # Sprite defines
        super().__init__()
        self.images = images
        self.image = pygame.Surface((32,32))
        self.image.set_colorkey("BLACK")
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.radius = ENEMY_RADIUS

        # Images
        self.base_image = self.images["NORMAL"]["BASE"][0]
        self.gun_image = self.images["NORMAL"]["GUN"][0]
        self.assembled_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.assembled_image.set_colorkey("BLACK")

        # Settings
        self.player = player
        self.health = SOLTURRET_HEALTH[g_diff]
        self.WORTH = SCORE_WORTH["SOLTURRET"]

        # States
        self.states_ = ("SPAWNING", "NORMAL")
        self.state_ = self.states_[0]

        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = 4

        # For shooting
        self.SHOOT_DELAY = SOLTURRET_SHOOT_DELAY[g_diff]
        self.BULLET_SPEED = SOLTURRET_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = SOLTURRET_BULLET_DAMAGE[g_diff]
        self.shoot_timer = pygame.time.get_ticks()
        self.BULLET_IMAGE = bullet_img

        # For flashing effect
        self._flash_delay = 100
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

    def update(self, dt):
        if self.state_ == "NORMAL":            
            # Run methods
            self.rotate_gun()
            self._shoot()
            self.update_image()
            self._flash()

        elif self.state_ == "SPAWNING":
            # Run methods
            self.spawn_animate()

            # Change state
            if self.current_frame >= self.MAX_FRAMES - 1:
                # Change image dictionary's key
                self.imgdict_key = "NORMAL"    

                self.state_ = self.states_[1]

    def spawn_animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.imgdict_key][self.current_frame]

    def _shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.SHOOT_DELAY:
            self.shoot_timer = now

            # Calculate delta x, and delta y
            rel_x = self.player.rect.x - self.rect.x
            rel_y = self.player.rect.y - self.rect.y
            radians = math.atan2(rel_y, rel_x)
            dx = (math.cos(radians) * self.BULLET_SPEED)
            dy = (math.sin(radians) * self.BULLET_SPEED)

            # Create bullet
            b = EnemyBullet(self.BULLET_IMAGE, Vec2(self.rect.center), Vec2(dx, dy), self.BULLET_DAMAGE)
            all_sprites_g.add(b)
            e_bullets_g.add(b)

    def rotate_gun(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0

            # Update Base image ======================
            self.base_image = self.images[self.imgdict_key]["BASE"][self.current_frame]

            # Update Gun image =======================
            # Calculate angle
            rel_x = self.player.rect.x - self.rect.x
            rel_y = self.player.rect.y - self.rect.y
            radians = -(math.atan2(rel_y, rel_x))
            #angle = (180 / math.pi) * -radians + 90
            angle = math.degrees(radians) + 90

            # Rotate the gun
            self.gun_image = pygame.transform.rotate(
                self.images[self.imgdict_key]["GUN"][self.current_frame], 
                int(angle)
            )
            self.gun_image.set_colorkey("BLACK")

    def update_image(self):
        # Update image - This one is buggy. Can be deleted.
        # self.image = pygame.Surface((32,32))
        # self.image.set_colorkey("BLACK")
        # self.image.blit(self.base_image, (0,0))
        # self.image.blit(
        #     self.gun_image, 
        #     (
        #         self.image.get_width() / 2 - self.gun_image.get_width() / 2, 
        #         self.image.get_height() / 2 - self.gun_image.get_height() / 2
        #     )
        # )
        self.assembled_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.assembled_image.set_colorkey("BLACK")
        self.assembled_image.blit(self.base_image, (0,0))
        self.assembled_image.blit(
            self.gun_image, 
            (
                self.image.get_width() / 2 - self.gun_image.get_width() / 2, 
                self.image.get_height() / 2 - self.gun_image.get_height() / 2
            )
        )
        self.image = self.assembled_image

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((32,32))
            points = pygame.mask.from_surface(self.assembled_image).outline()
            pygame.draw.polygon(flash_image,"WHITE",points,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

# POWERUP ======================================================================

class Powerup(pygame.sprite.Sprite):
    def __init__(self, images, position, pow_type, g_diff):
        # TODO - animation
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y 
        self.position = position
        self.SPEED = POWERUP_SPEED[g_diff]
        self.POW_TYPE = pow_type
        self.radius = POWERUP_RADIUS
        
        # For animation
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = 4

    def update(self, dt):
        # Run methods
        self._animate()

        # Kill sprite if it goes out of bounds
        if self.rect.top > WIN_RES["h"]:
            self.kill()

        # Update position
        self.position.y += self.SPEED * dt
        self.rect.x = self.position.x 
        self.rect.y = self.position.y

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.current_frame]

# SENTRY POWERUP ==============================

class Sentry(pygame.sprite.Sprite):
    def __init__(self, images, bullet_img, position):
        # Sprite defines
        super().__init__()
        self.images = images
        self.image = pygame.Surface((32,32))
        self.image.set_colorkey("BLACK")
        self.rect = self.image.get_rect()
        self.rect.x = position.x 
        self.rect.y = position.y 
        self.position = position
        self.radius = SENTRY_RADIUS

        # Settings
        self.health = SENTRY_HEALTH
        
        # States
        self.states_ = ("SPAWNING", "NORMAL")
        self.state_ = self.states_[0]

        # Images
        self.base_image = self.images["BASE"]
        self.gun_image = self.images["GUN"]
        self.assembled_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.assembled_image.set_colorkey("BLACK")

        # For animation
        self.animate_timer = pygame.time.get_ticks()
        self.animate_delay = 100
        self.current_frame = 0
        self.MAX_FRAMES = 4
        self.rot = 0

        # For shooting
        self.BULLET_SPEED = 500
        self.BULLET_DAMAGE = 0.5
        self.target = None
        self.shoot_delay = 300
        self.shoot_timer = pygame.time.get_ticks()
        self.BULLET_IMG = bullet_img

        # For flashing effect
        self._flash_delay = 300
        self._flash_timer = pygame.time.get_ticks()
        self.is_hurt = False
        self.prev_hurt = False

    def update(self, dt):
        if self.state_ == "NORMAL":
            # Run methods
            self.rotate_gun()
            self.find_enemy()
            self._shoot()
            self.update_image()
            self._flash()
            
        elif self.state_ == "SPAWNING":
            # Change image dictionary's key
            self.imgdict_key = "SPAWNING"
            
            # Run methods
            self._animate()

            # Change state check
            if self.current_frame >= self.MAX_FRAMES - 1:
                # Change image dictionary's key
                self.imgdict_key = "NORMAL"  

                self.state_ = self.states_[1]

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now

            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images["SPAWNING"][self.current_frame]

    def _shoot(self):
        if self.target != None:
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > self.shoot_delay:
                self.shoot_timer = now
                # Calculate radians, delta x, and delta y
                rel_y = self.rect.y - self.target.rect.y
                rel_x = self.rect.x - self.target.rect.x
                radians = math.atan2(rel_y, rel_x)
                dx = -(math.cos(radians) * self.BULLET_SPEED)
                dy = -(math.sin(radians) * self.BULLET_SPEED)

                # Create bullet
                b = SentryBullet(self.BULLET_IMG, Vec2(self.rect.center), Vec2(dx, dy), self.BULLET_DAMAGE)
                p_bullets_g.add(b)
                all_sprites_g.add(b)

    def rotate_gun(self):
        if self.target != None:
            now = pygame.time.get_ticks()
            if now - self.animate_timer > self.animate_delay:
                self.animate_timer = now

                # Calculate angle
                rel_x = self.target.rect.x - self.rect.x
                rel_y = self.target.rect.y - self.rect.y
                radians = -(math.atan2(rel_y, rel_x))
                angle = (180 / math.pi) * radians - 90

                # Rotate the gun
                self.gun_image = pygame.transform.rotate(self.images["GUN"], int(angle))
                self.gun_image.set_colorkey("BLACK")

    def find_enemy(self):
        if self.target == None:
            hostiles_list = list(hostiles_g)
            
            # Select random enemy
            if len(hostiles_list) > 0:
                self.target = random.choice(hostiles_list)
        else:
            # De-select enemy if enemy is killed
            if not self.target.groups():
                self.target = None

    def update_image(self):
        self.assembled_image = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.assembled_image.set_colorkey("BLACK")
        self.assembled_image.blit(self.base_image, (0,0))
        self.assembled_image.blit(
            self.gun_image, 
            (
                self.image.get_width() / 2 - self.gun_image.get_width() / 2, 
                self.image.get_height() / 2 - self.gun_image.get_height() / 2
            )
        )
        self.image = self.assembled_image

    def _flash(self):
        if self.is_hurt:
            # Make the image flash
            flash_image = pygame.Surface((32,32))
            points = pygame.mask.from_surface(self.assembled_image).outline()
            pygame.draw.polygon(flash_image,"WHITE",points,0)
            flash_image.set_colorkey("BLACK")
            self.image = flash_image

        # This is to correct the timing of the flash animation
        if self.prev_hurt != self.is_hurt:
            self.prev_hurt = self.is_hurt
            self._flash_timer = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self._flash_timer > self._flash_delay:
            self._flash_timer = now
            self.is_hurt = False

class SentryBullet(pygame.sprite.Sprite):
    def __init__(self, image, position, velocity, damage):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x 
        self.rect.centery = position.y 
        self.position = position
        self.velocity = velocity
        self.DAMAGE = damage
        self.radius = SENTRY_BULLET_RADIUS

    def update(self, dt):
        # Kill if it goes out of bounds
        if (self.rect.top > WIN_RES["h"] or 
            self.rect.bottom < 0 or
            self.rect.right < 0 or
            self.rect.left > WIN_RES["w"]):
            self.kill()

        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

# EFFECTS ====================================================================

class Explosion(pygame.sprite.Sprite):
    def __init__(self, images, position):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x 
        self.rect.centery = position.y 

        # For animation
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = 4

    def update(self, dt):
        # Run methods
        self._animate()

        # Kill sprite when last frame is reached
        if self.current_frame >= self.MAX_FRAMES - 1:
            self.kill() 

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.animate_timer > self.animate_delay:
            self.animate_timer = now 
            
            # Increment frames
            if self.current_frame < self.MAX_FRAMES - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            
            # Change image
            self.image = self.images[self.current_frame]

class Particle(pygame.sprite.Sprite):
    def __init__(self, position, velocity, color):
        super().__init__()
        # The surface
        self.image = pygame.Surface((32,32))
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.centery = position.y
        self.img_width = self.image.get_width()
        self.color = color

        self.position = position
        self.velocity = velocity
        
        # The circle
        self.MIN_RADIUS = 2
        self.MAX_RADIUS = random.randrange(4,8)
        self.update_timer = pygame.time.get_ticks()
        self.update_delay = 10
        self.radius = 2
        self.c_width = 5
        self.expand_amnt = 1
        self.deflate_amnt = 0.2

        # States 
        self.states_ = ("EXPANDING", "DEFLATING")
        self.state_ = self.states_[0]

    def update(self, dt):
        if self.state_ == "EXPANDING":
            # Run methods
            self._expand()
            self._update_image()

            # Update position
            self.position += self.velocity * dt 
            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y

            # Change state...
            if self.radius >= self.MAX_RADIUS:
                self.state_ = "DEFLATING"

        elif self.state_ == "DEFLATING":
            # Run methods
            self._deflate()
            self._update_image()

            # Update position
            self.position += self.velocity * dt 
            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y

            # Kill sprite check
            if self.radius <= self.MIN_RADIUS:
                self.kill()

    def _expand(self):
        now = pygame.time.get_ticks()
        if now - self.update_timer > self.update_delay:
            self.update_timer = now
            self.radius += self.expand_amnt

    def _deflate(self):
        now = pygame.time.get_ticks()
        if now - self.update_timer > self.update_delay:
            self.update_timer = now
            self.radius -= self.deflate_amnt

    def _update_image(self):
        self.image = pygame.Surface((64,64))
        self.image.set_colorkey("BLACK")
        pygame.draw.circle(self.image, self.color, self.image.get_rect().center, self.radius)
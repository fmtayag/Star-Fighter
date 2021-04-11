import pygame
import math
import random
import pygame.math
from data.scripts.defines import *
from data.scripts.muda import (
    SpriteState,
    SpriteStateManager
)

Vec2 = pygame.math.Vector2

# PLAYER =======================================================================

class Player(pygame.sprite.Sprite):
    def __init__(self, images, bullet_image):
        super().__init__()
        self.images = images
        self.image = self.images["N"]
        self.rect = self.image.get_rect()
        self.rect.x = WIN_RES["w"]*0.3
        self.rect.y = WIN_RES["h"]*0.9
        self.position = Vec2(self.rect.x,self.rect.y)
        self.velocity = Vec2(0,0)
        self.speed = PLAYER_SPEED
        self.gun_level = PLAYER_DEFAULT_GUN_LEVEL
        self.health = PLAYER_HEALTH
        self.radius = PLAYER_RADIUS
        
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

    def update(self, dt):
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        self.image = self.images["N"]
        self.velocity *= 0

        keyspressed = pygame.key.get_pressed()
        self.move(keyspressed)
        self.shoot(keyspressed)

        self.position += self.velocity * dt 
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.check_bounds()

    def move(self, keyspressed):
        if keyspressed[pygame.K_UP]:
            self.velocity.y = -self.speed
        if keyspressed[pygame.K_DOWN]:
            self.velocity.y = self.speed
        if keyspressed[pygame.K_LEFT]:
            self.image = self.images["L"]
            self.velocity.x = -self.speed
        if keyspressed[pygame.K_RIGHT]:
            self.image = self.images["R"]
            self.velocity.x = self.speed

    def check_bounds(self):
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
    
    def shoot(self,  keyspressed):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            if keyspressed[pygame.K_z]:
                if self.bullet_increase_timer >= self.bullet_increase_delay * 2 and self.gun_level == 3:
                    self.attack3()
                elif self.bullet_increase_timer >= self.bullet_increase_delay and self.gun_level >= 2:
                    self.attack2()
                else:
                    self.attack1()
                self.bullet_increase_timer += self.bullet_increase_tick
            else:
                self.bullet_increase_timer = 0

    def attack1(self):
        b = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx, self.rect.top), Vec2(0, -self.BULLET_SPEED))
        all_sprites_g.add(b)
        p_bullets_g.add(b)

    def attack2(self):
        b1 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx-10, self.rect.top+12), Vec2(0, -self.BULLET_SPEED))
        b2 = PlayerBullet(self.bullet_image, Vec2(self.rect.centerx+10, self.rect.top+12), Vec2(0, -self.BULLET_SPEED))
        all_sprites_g.add(b1)
        all_sprites_g.add(b2)
        p_bullets_g.add(b1)
        p_bullets_g.add(b2)

    def attack3(self):
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
            self.explode()

        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

        if self.rect.top > WIN_RES["h"] or self.rect.bottom < 0:
            self.kill()

    def explode(self):
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

class HellfighterSpawningState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "SPAWNING"

    def update(self, dt):
        self.sprite_.animate()

        # Change state...
        if self.sprite_.current_frame == self.sprite_.MAX_FRAMES - 1:
            self.manager.transition(HellfighterFightingState(self.sprite_))

class HellfighterFightingState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "NORMAL"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()
        self.follow_player()
        self.shoot()

        # Update position
        self.sprite_.position += self.sprite_.velocity * dt 
        self.sprite_.rect.x = self.sprite_.position.x
        self.sprite_.rect.y = self.sprite_.position.y

    def follow_player(self):
        # Calculate delta-x
        rel_y = self.sprite_.rect.y - self.sprite_.player.rect.y
        rel_x = self.sprite_.rect.x - self.sprite_.player.rect.x
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.sprite_.velocity.x = -(dx * self.sprite_.SPEED)

    def shoot(self):
        # Calculate radians
        rel_y = self.sprite_.rect.centery - self.sprite_.player.rect.centery
        rel_x = self.sprite_.rect.centerx - self.sprite_.player.rect.centerx
        radians = math.atan2(rel_y, rel_x)

        # Calculate x-component
        x_com = math.cos(radians)

        # Only shoot if in range
        if x_com > -self.sprite_.RANGE and x_com < self.sprite_.RANGE:
            now = pygame.time.get_ticks()
            if now - self.sprite_.shoot_timer > self.sprite_.SHOOT_DELAY:
                self.sprite_.shoot_timer = now

                # Calculate vertical direction
                dir_y = -(math.copysign(1, math.sin(radians)))

                b = EnemyBullet(
                    self.sprite_.BULLET_IMAGE,
                    Vec2(self.sprite_.rect.center),
                    Vec2(-x_com * (self.sprite_.BULLET_SPEED / 2), self.sprite_.BULLET_SPEED * dir_y),
                    self.sprite_.BULLET_DAMAGE
                )
                e_bullets_g.add(b)
                all_sprites_g.add(b)

class Hellfighter(pygame.sprite.Sprite):
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
        self.health = HELLFIGHTER_HEALTH[g_diff]
        self.SPEED = HELLFIGHTER_SPEED[g_diff]
        self.WORTH = SCORE_WORTH["HELLFIGHTER"]

        # State machine
        self.machine = SpriteStateManager(HellfighterSpawningState(self))
        
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

    def update(self, dt):
        self.machine.state.update(dt)

    def animate(self):
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

# FATTY ENEMY =================================

class FattySpawningState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "SPAWNING"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()

        # Change state...
        if self.sprite_.current_frame == self.sprite_.MAX_FRAMES - 1:
            self.manager.transition(FattyFightingState(self.sprite_))

class FattyFightingState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "NORMAL"
        self.bob_y = -2

    def update(self, dt):
        # Run methods
        self.sprite_.animate()
        self.follow_player()
        self.bob()
        self.shoot() 

        # Update position
        self.sprite_.position += self.sprite_.velocity * dt 
        self.sprite_.rect.x = self.sprite_.position.x
        self.sprite_.rect.y = self.sprite_.position.y

    def follow_player(self):
        # Calculate delta-x
        rel_y = self.sprite_.rect.y - self.sprite_.player.rect.y
        rel_x = self.sprite_.rect.x - self.sprite_.player.rect.x
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.sprite_.velocity.x = -(dx * self.sprite_.SPEED)

    def bob(self):
        self.sprite_.velocity.y = math.sin(self.bob_y) * 50
        self.bob_y += 0.1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.sprite_.shoot_timer > self.sprite_.SHOOT_DELAY:
            self.sprite_.shoot_timer = now

            b = FattyBullet(
                self.sprite_.LARGE_BULLET_IMAGE,
                self.sprite_.SMALL_BULLET_IMAGE,
                Vec2(self.sprite_.rect.centerx, self.sprite_.rect.bottom),
                Vec2(0,self.sprite_.BULLET_SPEED),
                self.sprite_.BULLET_DAMAGE,
                self.sprite_.SMALL_BULLET_SPEED
            )
            e_bullets_g.add(b)
            all_sprites_g.add(b)

class Fatty(pygame.sprite.Sprite):
    def __init__(self, images, bullet_imgs, position, player, g_diff):
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
        self.health = FATTY_HEALTH[g_diff]
        self.SPEED = FATTY_SPEED[g_diff]
        self.WORTH = SCORE_WORTH["FATTY"]

        # State machine
        self.machine = SpriteStateManager(FattySpawningState(self))

        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images[self.imgdict_key])

        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.SHOOT_DELAY = FATTY_SHOOT_DELAY[g_diff]
        self.BULLET_SPEED = FATTY_LARGE_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = FATTY_BULLET_DAMAGE[g_diff]
        self.SMALL_BULLET_SPEED = FATTY_SMALL_BULLET_SPEED[g_diff]
        self.BULLET_IMAGES = bullet_imgs
        self.LARGE_BULLET_IMAGE = self.BULLET_IMAGES["LARGE"]
        self.SMALL_BULLET_IMAGE = self.BULLET_IMAGES["SMALL"]

    def update(self, dt):
        # Update state
        self.machine.state.update(dt)

    def animate(self):
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

# RAIDER ENEMY ================================

class RaiderSpawningState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "SPAWNING"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()

        # Change state....
        if self.sprite_.current_frame == self.sprite_.MAX_FRAMES - 1:
            self.manager.transition(RaiderFollowingState(self.sprite_))

class RaiderFollowingState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.target_acquired = False
        self.sprite_.imgdict_key = "NORMAL"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()
        self.follow_player()
        
        # Update position
        self.sprite_.position += self.sprite_.velocity * dt
        self.sprite_.rect.x = self.sprite_.position.x
        self.sprite_.rect.y = self.sprite_.position.y

        # Change state...
        if self.target_acquired:
            self.manager.transition(RaiderDashingState(self.sprite_))

    def follow_player(self):
        # Calculate delta-x
        rel_x = self.sprite_.rect.x - self.sprite_.player.rect.x
        rel_y = self.sprite_.rect.y - self.sprite_.player.rect.y
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.sprite_.velocity.x = -(dx * self.sprite_.SPEED)
        if dx > -self.sprite_.DASH_RANGE and dx < self.sprite_.DASH_RANGE:
            self.target_acquired = True

class RaiderDashingState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.dash_x = -2
        self.sprite_.imgdict_key = "NORMAL"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()
        self.dash()

        # Update position
        self.sprite_.position += self.sprite_.velocity * dt
        self.sprite_.rect.x = self.sprite_.position.x
        self.sprite_.rect.y = self.sprite_.position.y
    
    def dash(self):
        if self.sprite_.velocity.y < self.sprite_.MAX_DASH_SPEED:
            self.sprite_.velocity.y += math.pow(self.dash_x, 3)
            self.dash_x += 0.1

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

        # State machine
        self.machine = SpriteStateManager(RaiderSpawningState(self))

        # For animation
        self.imgdict_key = "SPAWNING"
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images[self.imgdict_key])

    def update(self, dt):
        # Update state
        self.machine.state.update(dt)

        # Kill if it goes out of bounds
        if self.rect.top > WIN_RES["h"]:
            self.kill()

    def animate(self):
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

# HELLEYE ENEMY ===============================

class HelleyeSpawningState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "SPAWNING"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()

        # Change state....
        if self.sprite_.current_frame == self.sprite_.MAX_FRAMES - 1:
            self.manager.transition(HelleyeFightingState(self.sprite_))

class HelleyeFightingState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.sprite_.imgdict_key = "NORMAL"

    def update(self, dt):
        # Run methods
        self.sprite_.animate()
        self.follow_player()
        self.shoot()

        # Update position
        self.sprite_.position += self.sprite_.velocity * dt 
        self.sprite_.rect.x = self.sprite_.position.x
        self.sprite_.rect.y = self.sprite_.position.y

    def follow_player(self):
        # Calculate delta-x
        rel_y = self.sprite_.rect.y - self.sprite_.player.rect.y
        rel_x = self.sprite_.rect.x - self.sprite_.player.rect.x
        radians = math.atan2(rel_y, rel_x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.sprite_.velocity.x = -(dx * self.sprite_.SPEED)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.sprite_.shoot_timer > self.sprite_.SHOOT_DELAY:
            self.sprite_.shoot_timer = now

            for i in range(len(HELLEYE_BULLET_DIRECTION)):
                b = EnemyBullet(
                    self.sprite_.BULLET_IMAGE,
                    Vec2(self.sprite_.rect.center),
                    Vec2(HELLEYE_BULLET_DIRECTION[i] * self.sprite_.BULLET_SPEED),
                    self.sprite_.BULLET_DAMAGE
                )
                e_bullets_g.add(b)
                all_sprites_g.add(b)

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
        self.machine = SpriteStateManager(HelleyeSpawningState(self))

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
    
    def update(self, dt):
        # Update state
        self.machine.state.update(dt)

    def animate(self):
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

# SOLTURRET ENEMY =============================

class SolturretSpawningState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.imgdict_key = "SPAWNING"

    def update(self, dt):
        # Run methods
        self.animate()

        # Change state....
        if self.sprite_.current_frame == self.sprite_.MAX_FRAMES - 1:
            self.manager.transition(SolturretFightState(self.sprite_))

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.sprite_.animate_timer > self.sprite_.animate_delay:
            self.sprite_.animate_timer = now

            # Increment frames
            if self.sprite_.current_frame < self.sprite_.MAX_FRAMES - 1:
                self.sprite_.current_frame += 1
            else:
                self.sprite_.current_frame = 0
            
            # Change image
            self.sprite_.image = self.sprite_.images[self.imgdict_key][self.sprite_.current_frame]

class SolturretFightState(SpriteState):
    def __init__(self, sprite_):
        self.sprite_ = sprite_
        self.imgdict_key = "NORMAL"
        self.sprite_.image = pygame.Surface((32,32)) # note: adding this solved the weird "mimicking" bug
        self.sprite_.image.set_colorkey("BLACK")

    def update(self, dt):
        # Run methods
        self.animate()
        self.shoot()

        # Update image
        self.sprite_.image.fill("BLACK")
        self.sprite_.image.set_colorkey("BLACK")
        self.sprite_.image.blit(self.sprite_.base_image, (0,0))
        self.sprite_.image.blit(
            self.sprite_.gun_image, 
            (
                self.sprite_.image.get_width() / 2 - self.sprite_.gun_image.get_width() / 2, 
                self.sprite_.image.get_height() / 2 - self.sprite_.gun_image.get_height() / 2
            )
        )

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.sprite_.shoot_timer > self.sprite_.SHOOT_DELAY:
            self.sprite_.shoot_timer = now

            # Calculate delta x, and delta y
            rel_x = self.sprite_.player.rect.x - self.sprite_.rect.x
            rel_y = self.sprite_.player.rect.y - self.sprite_.rect.y
            radians = math.atan2(rel_y, rel_x)
            dx = (math.cos(radians) * self.sprite_.BULLET_SPEED)
            dy = (math.sin(radians) * self.sprite_.BULLET_SPEED)

            # Create bullet
            b = EnemyBullet(self.sprite_.BULLET_IMAGE, Vec2(self.sprite_.rect.center), Vec2(dx, dy), self.sprite_.BULLET_DAMAGE)
            all_sprites_g.add(b)
            e_bullets_g.add(b)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.sprite_.animate_timer > self.sprite_.animate_delay:
            self.sprite_.animate_timer = now

            # Increment frames
            if self.sprite_.current_frame < self.sprite_.MAX_FRAMES - 1:
                self.sprite_.current_frame += 1
            else:
                self.sprite_.current_frame = 0

            # Update Base image ======================
            self.sprite_.base_image = self.sprite_.images[self.imgdict_key]["BASE"][self.sprite_.current_frame]

            # Update Gun image =======================
            # Calculate angle
            rel_x = self.sprite_.player.rect.x - self.sprite_.rect.x
            rel_y = self.sprite_.player.rect.y - self.sprite_.rect.y
            radians = -(math.atan2(rel_y, rel_x))
            #angle = (180 / math.pi) * -radians + 90
            angle = math.degrees(radians) + 90

            # Rotate the gun
            self.sprite_.gun_image = pygame.transform.rotate(
                self.sprite_.images[self.imgdict_key]["GUN"][self.sprite_.current_frame], 
                int(angle)
            )
            self.sprite_.gun_image.set_colorkey("BLACK")

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

        # Settings
        self.player = player
        self.health = SOLTURRET_HEALTH[g_diff]
        self.WORTH = SCORE_WORTH["SOLTURRET"]

        # State machine
        self.machine = SpriteStateManager(SolturretSpawningState(self))

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

    def update(self, dt):
        # Update state
        self.machine.state.update(dt)

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
        self.animate()

        # Kill sprite if it goes out of bounds
        if self.rect.top > WIN_RES["h"]:
            self.kill()

        # Update position
        self.position.y += self.SPEED * dt
        self.rect.x = self.position.x 
        self.rect.y = self.position.y

    def animate(self):
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
        super().__init__()
        self.images = images
        self.image = pygame.Surface((32,32))
        self.rect = self.image.get_rect()
        self.rect.x = position.x 
        self.rect.y = position.y 
        self.position = position
        self.health = SENTRY_HEALTH
        self.radius = SENTRY_RADIUS

        # Images
        self.base_image = self.images["BASE"]
        self.gun_image = self.images["GUN"]

        # For shooting
        self.BULLET_SPEED = 500
        self.BULLET_DAMAGE = 0.5
        self.target = None
        self.shoot_delay = 300
        self.shoot_timer = pygame.time.get_ticks()
        self.BULLET_IMG = bullet_img

        # For animation
        self.frame_timer = pygame.time.get_ticks()
        self.FRAME_DELAY = 100
        self.rot = 0

    def update(self, dt):

        # Update surface
        self.rotate_gun()
        self.image.fill("BLACK")
        self.image.set_colorkey("BLACK")
        self.image.blit(self.base_image, (0,0))
        self.image.blit(
            self.gun_image, 
            (
                self.image.get_width()/2 - self.gun_image.get_width()/2, 
                self.image.get_height()/2 - self.gun_image.get_height()/2
            )
        )

        self.find_enemy()
        self.shoot()
        
    def shoot(self):
        if self.target != None:
            now = pygame.time.get_ticks()
            if now - self.shoot_timer > self.shoot_delay:
                self.shoot_timer = now
                # Calculate radians, delta x, and delta y
                radians = math.atan2(self.rect.y - self.target.rect.y, self.rect.x - self.target.rect.x)
                dx = -(math.cos(radians) * self.BULLET_SPEED)
                dy = -(math.sin(radians) * self.BULLET_SPEED)

                # Create bullet
                b = SentryBullet(self.BULLET_IMG, Vec2(self.rect.center), Vec2(dx, dy), self.BULLET_DAMAGE)
                p_bullets_g.add(b)
                all_sprites_g.add(b)

    def rotate_gun(self):
        if self.target != None:
            now = pygame.time.get_ticks()
            if now - self.frame_timer > self.FRAME_DELAY:
                self.frame_timer = now

                rel_x = self.target.rect.x - self.rect.x
                rel_y = self.target.rect.y - self.rect.y
                radians = -(math.atan2(rel_y, rel_x))
                angle = (180 / math.pi) * radians - 90
                #print(angle)

                # Rotate the gun
                self.gun_image = pygame.transform.rotozoom(self.images["GUN"], int(angle), 1)

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
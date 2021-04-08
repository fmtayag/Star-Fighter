import pygame
import math
import random
import pygame.math
from data.scripts.defines import *

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
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

        if self.rect.bottom < 0:
            self.kill()

# ENEMIES ======================================================================

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
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

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

class Hellfighter(pygame.sprite.Sprite):
    def __init__(self, images, bullet_img, position, player, g_diff):
        # TODO - animation
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x 
        self.rect.y = position.y 
        self.position = position
        self.velocity = Vec2(0,0)
        self.player = player
        self.SPEED = HELLFIGHTER_SPEED[g_diff]
        self.health = HELLFIGHTER_HEALTH[g_diff]
        self.WORTH = SCORE_WORTH["HELLFIGHTER"]
        self.radius = ENEMY_RADIUS

        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.SHOOT_DELAY = HELLFIGHTER_SHOOT_DELAY[g_diff]
        self.RANGE = HELLFIGHTER_RANGE[g_diff] 
        self.BULLET_SPEED = HELLFIGHTER_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = HELLFIGHTER_BULLET_DAMAGE[g_diff]
        self.BULLET_IMAGE = bullet_img

    def update(self, dt):
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        self.follow_player()
        self.shoot()
        self.position += self.velocity * dt 
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def follow_player(self):
        # Calculate delta-x
        radians = math.atan2(self.rect.y - self.player.rect.y, self.rect.x - self.player.rect.x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)

    def shoot(self):
        # Calculate radians
        radians = math.atan2(self.rect.centery - self.player.rect.centery, self.rect.centerx - self.player.rect.centerx)

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

class Fatty(pygame.sprite.Sprite):
    def __init__(self, images, bullet_imgs, position, player, g_diff):
        # TODO - animation
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.velocity = Vec2(0,0)
        self.player = player
        self.SPEED = FATTY_SPEED[g_diff]
        self.bob_y = 0
        self.health = FATTY_HEALTH[g_diff]
        self.WORTH = SCORE_WORTH["FATTY"]
        self.radius = ENEMY_RADIUS

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
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        self.follow_player()
        self.bob()
        self.shoot() 

        self.position += self.velocity * dt 
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def follow_player(self):
        # Calculate delta-x
        radians = math.atan2(self.rect.y - self.player.rect.y, self.rect.x - self.player.rect.x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)

    def bob(self):
        self.velocity.y = math.sin(self.bob_y) * 50
        self.bob_y += 0.1

    def shoot(self):
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

class Raider(pygame.sprite.Sprite):
    def __init__(self, images, position, player, g_diff):
        # TODO - animation
        super().__init__()
        self.images = images
        self.image = self.images["SPAWNING"][0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.velocity = Vec2(0,0)
        self.player = player
        self.SPEED = RAIDER_SPEED[g_diff]
        self.DASH_RANGE = RAIDER_DASH_RANGE[g_diff]
        self.MAX_DASH_SPEED = RAIDER_MAX_SPEED[g_diff]
        self.health = RAIDER_HEALTH[g_diff]
        self.is_dashing = False
        self.dash_x = -2
        self.WORTH = SCORE_WORTH["RAIDER"]
        self.radius = ENEMY_RADIUS

        # State - Values: SPAWNING & NORMAL
        self._state = "SPAWNING"

        # For animation
        self.animate_delay = 100
        self.animate_timer = pygame.time.get_ticks()
        self.current_frame = 0
        self.MAX_FRAMES = len(self.images["SPAWNING"]) # could be a constant. maybe 4.

    def update(self, dt):
        if self._state == "NORMAL":
            self.animate()

            # Kill if it goes out of bounds
            if self.rect.top > WIN_RES["h"]:
                self.kill()

            if not self.is_dashing:
                self.follow_player()
            else:
                self.dash()

            self.position += self.velocity * dt
            self.rect.x = self.position.x
            self.rect.y = self.position.y

            if DEBUG_MODE:
                pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

            
        elif self._state == "SPAWNING":
            self.animate()

            # Change state
            if self.current_frame == self.MAX_FRAMES - 1:
                self._state = "NORMAL"

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
            self.image = self.images[self._state][self.current_frame]


    def follow_player(self):
        # Calculate delta-x
        radians = math.atan2(self.rect.y - self.player.rect.y, self.rect.x - self.player.rect.x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)
        
        if dx > -self.DASH_RANGE and dx < self.DASH_RANGE:
            self.is_dashing = True

    def dash(self):
        if self.velocity.y < self.MAX_DASH_SPEED:
            self.velocity.y += math.pow(self.dash_x, 3)
            self.dash_x += 0.1

class Helleye(pygame.sprite.Sprite):
    def __init__(self, images, bullet_img, position, player, g_diff):
        # TODO - animation
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.velocity = Vec2(0,0)
        self.player = player
        self.SPEED = HELLEYE_SPEED[g_diff]
        self.health = HELLEYE_HEALTH[g_diff]
        self.WORTH = SCORE_WORTH["HELLEYE"]
        self.radius = ENEMY_RADIUS
    
        # For shooting
        self.SHOOT_DELAY = HELLEYE_SHOOT_DELAY[g_diff]
        self.BULLET_SPEED = HELLEYE_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = HELLEYE_BULLET_DAMAGE[g_diff]
        self.shoot_timer = pygame.time.get_ticks()
        self.BULLET_IMAGE = bullet_img
    
    def update(self, dt):
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)
            
        self.follow_player()
        self.shoot()
        self.position += self.velocity * dt 
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def follow_player(self):
        # Calculate delta-x
        radians = math.atan2(self.rect.y - self.player.rect.y, self.rect.x - self.player.rect.x)
        dx = math.cos(radians)

        # Add delta-x to velocity
        self.velocity.x = -(dx * self.SPEED)

    def shoot(self):
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

class Solturret(pygame.sprite.Sprite): 
    def __init__(self, images, bullet_img, position, player, g_diff):
        # TODO - animation
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y
        self.position = position
        self.player = player
        self.health = SOLTURRET_HEALTH[g_diff]
        self.WORTH = SCORE_WORTH["SOLTURRET"]
        self.radius = ENEMY_RADIUS

        # For shooting
        self.SHOOT_DELAY = SOLTURRET_SHOOT_DELAY[g_diff]
        self.BULLET_SPEED = SOLTURRET_BULLET_SPEED[g_diff]
        self.BULLET_DAMAGE = SOLTURRET_BULLET_DAMAGE[g_diff]
        self.shoot_timer = pygame.time.get_ticks()
        self.BULLET_IMAGE = bullet_img

    def update(self, dt):
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.SHOOT_DELAY:
            self.shoot_timer = now

            # Calculate radians, delta x, and delta y
            radians = math.atan2(self.rect.y - self.player.rect.y, self.rect.x - self.player.rect.x)
            dx = -(math.cos(radians) * self.BULLET_SPEED)
            dy = -(math.sin(radians) * self.BULLET_SPEED)

            # Create bullet
            b = EnemyBullet(self.BULLET_IMAGE, Vec2(self.rect.center), Vec2(dx, dy), self.BULLET_DAMAGE)
            all_sprites_g.add(b)
            e_bullets_g.add(b)

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

    def update(self, dt):
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        if self.rect.top > WIN_RES["h"]:
            self.kill()

        self.position.y += self.SPEED * dt
        self.rect.x = self.position.x 
        self.rect.y = self.position.y 

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

        # Base image
        self.base_image = self.images["BASE"]

        # Gun image
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
        self.FRAME_DELAY = 10
        self.rot = 0

    def update(self, dt):

        # Update surface
        self.rotate_gun()
        self.image.fill("BLACK")
        self.image.set_colorkey("BLACK")
        self.image.blit(self.base_image, (0,0))
        self.image.blit(
            self.gun_image, 
            (self.image.get_width()/2 - self.gun_image.get_width()/2, self.image.get_height()/2 - self.gun_image.get_height()/2))

        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

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

                # Zyenapz says: This fucking code took me 4 hours to figure out. Jesus Christ.
                rel_x = self.target.rect.x - self.rect.x
                rel_y = self.target.rect.y - self.rect.y
                radians = math.atan2(rel_y, rel_x)
                angle = (180 / math.pi) * -radians - 90
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
        if DEBUG_MODE:
            pygame.draw.circle(self.image, "WHITE", (self.image.get_width()/2, self.image.get_height()/2), self.radius, 2)

        # Kill if it goes out of bounds
        if (self.rect.top > WIN_RES["h"] or 
            self.rect.bottom < 0 or
            self.rect.right < 0 or
            self.rect.left > WIN_RES["w"]):
            self.kill()

        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y
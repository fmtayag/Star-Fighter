import pygame
import pygame.math
Vec2 = pygame.math.Vector2
import math
from data.scripts.settings import *
from data.scripts.MUDA import (
    load_img, 
    load_sound, 
    sort,
    read_savedata,
    write_savedata,
    Scene,
    SceneManager,
    draw_background, 
    draw_text,
    shake,
    slice_list
)

# Player =====================================

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
        self.speed = 225
        self.gun_level = 3
        
        # For shooting
        self.bullet_image = bullet_image
        self.shoot_delay = 125
        self.shoot_timer = pygame.time.get_ticks()
        self.bullet_increase_delay = 50
        self.bullet_increase_timer = 0
        self.bullet_increase_tick = 25
        self.weak_bullet_delay = 200
        self.weak_bullet_timer = pygame.time.get_ticks()
        self.weak_bullet_tick = 10

    def update(self, dt, sprites):
        self.image = self.images["N"]
        self.velocity *= 0

        keyspressed = pygame.key.get_pressed()
        self.move(keyspressed)
        self.shoot(sprites, keyspressed)

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
    
    def shoot(self, sprites, keyspressed):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            if keyspressed[pygame.K_z]:
                if self.bullet_increase_timer >= self.bullet_increase_delay * 2 and self.gun_level == 3:
                    self.attack3(sprites)
                elif self.bullet_increase_timer >= self.bullet_increase_delay and self.gun_level >= 2:
                    self.attack2(sprites)
                else:
                    self.attack1(sprites)
                self.bullet_increase_timer += self.bullet_increase_tick
            else:
                self.bullet_increase_timer = 0

    def attack1(self, sprites):
        sprites.add(PlayerBullet(self.bullet_image, Vec2(self.rect.centerx, self.rect.top), Vec2(0, -self.speed)))

    def attack2(self, sprites):
        sprites.add(PlayerBullet(self.bullet_image, Vec2(self.rect.centerx-10, self.rect.top+12), Vec2(0, -self.speed)))
        sprites.add(PlayerBullet(self.bullet_image, Vec2(self.rect.centerx+10, self.rect.top+12), Vec2(0, -self.speed)))

    def attack3(self, sprites):
        self.attack1(sprites)
        self.attack2(sprites)
    
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, image, position, velocity):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = position.x
        self.rect.bottom = position.y
        self.position = Vec2(self.rect.centerx, self.rect.bottom)
        self.velocity = Vec2(velocity.x, velocity.y*3)
        self.damage = PLAYER_DAMAGE

    def update(self, dt, sprites):
        self.position += self.velocity * dt 
        self.rect.centerx = self.position.x
        self.rect.bottom = self.position.y

        if self.rect.bottom < 0:
            self.kill()
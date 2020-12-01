import pygame, random, numpy

class Player(pygame.sprite.Sprite):
    def __init__(self, win_res, images, sprite_supergroup, Bullet, bullet_img, bullet_sfx):
        super().__init__()
        self.win_res = win_res
        self.images = images
        self.Bullet = Bullet
        self.bullet_img = bullet_img
        self.bullet_sfx = bullet_sfx
        self.orient = "normal"
        self.lvls = ["cadet", "captain", "admiral"]
        self.cur_lvl = 0
        self.lvl = self.lvls[self.cur_lvl]
        self.image = self.images[self.lvl][self.orient][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.win_res["w"]/2
        self.rect.bottom = self.win_res["h"]-64
        self.health = 10
        # Sprite groups
        self.sprite_supergroup = sprite_supergroup
        self.sprites = self.sprite_supergroup["sprites"]
        self.p_lasers = self.sprite_supergroup["p_lasers"]
        # Speed
        self.movspd = 6
        self.spdx = 0
        self.spdy = 0
        # Shooting
        self.shoot_delay = 250
        self.shoot_timer = pygame.time.get_ticks()
        # For animation
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        self.frame = 0
        # For collision detection
        self.radius = 16

    def update(self):
        # Reset ship's orientation
        self.orient = "normal"
        self.spdy = 0
        self.spdx = 0

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.spdy -= self.movspd
        if pressed[pygame.K_s]:
            self.spdy += self.movspd
        if pressed[pygame.K_a]:
            self.spdx -= self.movspd
            self.orient = "left"
        if pressed[pygame.K_d]:
            self.spdx += self.movspd
            self.orient = "right"
        if pressed[pygame.K_SPACE]:
            self.shoot()

        # Check if object collides with window bounds
        if self.rect.right > self.win_res["w"]:
            self.rect.right = self.win_res["w"]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.win_res["h"]:
            self.rect.bottom = self.win_res["h"]
        if self.rect.top < 0:
            self.rect.top = 0

        # Animate the sprite
        self.animate()

        # Move the object
        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            self.bullet_sfx.play()
            if self.lvl == "cadet":
                l = self.Bullet(self.win_res["h"], self.bullet_img, self.rect.centerx,
                          self.rect.top-32, 0, -8)
                self.sprites.add(l)
                self.p_lasers.add(l)
            elif self.lvl == "captain":
                offset_x = [-13,13]
                speed_x = [-1,1]
                for i in range(2):
                    l = self.Bullet(self.win_res["h"], self.bullet_img, self.rect.centerx+offset_x[i],
                              self.rect.top-32, speed_x[i], -8)
                    self.sprites.add(l)
                    self.p_lasers.add(l)
            elif self.lvl == "admiral":
                offset_x = [-13,0,13]
                offset_y = [-6,-32,-6]
                speed_x = [-1,0,1]
                for i in range(3):
                    l = self.Bullet(self.win_res["h"], self.bullet_img, self.rect.centerx+offset_x[i],
                              self.rect.top+offset_y[i], speed_x[i], -8)
                    self.sprites.add(l)
                    self.p_lasers.add(l)

    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images[self.lvl][self.orient][self.frame]
            self.rect = self.image.get_rect()
            #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
            self.rect.x = old_rectx
            self.rect.y = old_recty

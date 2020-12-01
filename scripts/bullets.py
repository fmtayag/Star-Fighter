import pygame, numpy

class Laser(pygame.sprite.Sprite):
    def __init__(self, win_h, image, xpos, ypos, spdx, spdy):
        super().__init__()
        self.win_h = win_h
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos
        self.spdx = spdx
        self.spdy = spdy
        self.damage = 1

    def update(self):
        self.rect.x += self.spdx
        self.rect.y += self.spdy

        if (self.rect.bottom < 0 or
            self.rect.top > self.win_h):
            self.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, win_res, image, xpos, ypos, spdx, movspd):
        super().__init__()
        self.win_res = win_res
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos
        self.movspd = movspd
        self.spdx = spdx
        self.spdy = self.movspd
        # Dissolve variables
        self.dissolve_delay = 500
        self.dissolve_timer = pygame.time.get_ticks()
        self.scaler = 1
        self.damage = 4

    def update(self):

        if self.rect.bottom > self.win_res["h"]:
            self.spdy = -self.movspd
        elif self.rect.top < 0:
            self.spdy = self.movspd
        elif self.rect.left < 0:
            self.spdx = self.movspd
        elif self.rect.right > self.win_res["w"]:
            self.spdx = -self.movspd

        if self.image.get_width() <= 5:
            self.kill()

        # Gradually dissolve
        self.dissolve()

        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def dissolve(self):
        now = pygame.time.get_ticks()
        if now - self.dissolve_timer > self.dissolve_delay:
            self.dissolve_timer = now
            x_scale = self.image.get_width() - self.scaler
            y_scale = self.image.get_height() - self.scaler
            self.image = pygame.transform.scale(self.image, (x_scale,y_scale))
            self.scaler += 1
            self.movspd -= 1
            self.damage -= 1
            self.damage = numpy.clip(self.damage,1,5)

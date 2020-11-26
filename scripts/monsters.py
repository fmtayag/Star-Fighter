import pygame, random, numpy

class Monster(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.surface = data["surface"]
        self.surf_w = self.surface.get_width()
        self.surf_h = self.surface.get_height()
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = data["coords"][0]
        self.rect.y = data["coords"][1]
        self.spritegroups = data["spritegroups"]
        self.sprites = self.spritegroups[0]
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100

    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect()
            #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
            self.rect.x = old_rectx
            self.rect.y = old_recty

    def explode(self, explode_func, xpos, ypos):
        explode_func(xpos, ypos)

class Hellfighter(Monster):
    def __init__(self, data):
        super().__init__(data)
        self.e_lasers = self.spritegroups[1]
        self.laser_img = data["bullet_img"]
        self.bullet = data["bullet_class"]
        self.health = 2
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.spdx = random.choice([-3,3])
        self.spdy = 1

    def update(self):
        # Decelerate on the y-axis
        if self.spdy < 1:
            self.spdy += 1

        if self.rect.left < 0:
            self.spdx = 3
        elif self.rect.right > self.surf_w:
            self.spdx = -3

        # Delete object if it goes off-screen or has <= 0 health
        if self.rect.top > self.surf_h or self.health <= 0:
            self.kill()

        self.animate()
        self.shoot()
        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            l = self.bullet(self.surface, self.laser_img, self.rect.centerx,
                      self.rect.bottom, 0, 8)
            self.sprites.add(l)
            self.e_lasers.add(l)

class Raider(Monster):
    def __init__(self, data):
        super().__init__(data)
        self.health = 4
        self.maxspd = 7
        self.spdy = 8

    def update(self):
        # Slow down when knockbacked
        if self.spdy < self.maxspd * 0.8:
            self.spdy += 1

        # Delete object if it goes off-screen or has <= 0 health
        if self.rect.top > self.surf_h or self.health <= 0:
            self.kill()

        self.animate()
        self.rect.y += self.spdy

class Fatty(Monster):
    def __init__(self, data):
        super().__init__(data)
        self.e_lasers = self.spritegroups[1]
        self.laser_img = data["bullet_img"]
        self.bullet = data["bullet_class"]
        self.health = 6
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 3000
        self.spdx = random.choice([-1,1])
        self.spdy = 0
        # the point at which the object will stop moving on the y-axis
        self.max_disty = self.surf_h * (random.randrange(2, 5) / 10)

    def update(self):

        # Slow down when knockbacked
        if self.spdy < 1:
            self.spdy += 1

        # Bounces object on the sides
        if self.rect.left < 0:
            self.spdx = 1
        elif self.rect.right > self.surf_w:
            self.spdx = -1

        # Stop on the y-axis
        if self.rect.bottom > self.max_disty:
            self.rect.y -= 1

        # Delete object if it goes off-screen or has <= 0 health
        if self.rect.top > self.surf_h or self.health <= 0:
            self.kill()

        self.animate()
        self.shoot()
        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            f1 = self.bullet(self.surface, self.laser_img, self.rect.centerx, self.rect.bottom, 10, 8)
            f2 = self.bullet(self.surface, self.laser_img, self.rect.centerx, self.rect.bottom, -10, 9)
            self.sprites.add(f1)
            self.sprites.add(f2)
            self.e_lasers.add(f1)
            self.e_lasers.add(f2)
            self.spdy -= 10 # Recoil effect

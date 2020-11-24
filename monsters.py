import pygame, random, numpy

class Hellfighter(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.surf = data["surface"]
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = data["coords"][0]
        self.rect.y = data["coords"][1]
        self.spritegroups = data["spritegroups"]
        self.sprites = self.spritegroups[0]
        self.e_lasers = self.spritegroups[1]
        self.laser_img = data["laser_img"]
        self.bullet = data["bullet"]
        self.health = 2
        # Variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # Variables for shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 1000
        #self.movspd = data["movspd"]
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
        
        # Animate the object
        self.animate()
        self.shoot()

        # Delete object if it goes off-screen or has <= 0 health
        if self.rect.top > self.surf_h or self.health <= 0:
            self.kill()

        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            l = self.bullet(self.surf, self.laser_img, self.rect.centerx,
                      self.rect.bottom, 0, 8)
            self.sprites.add(l)
            self.e_lasers.add(l)

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

class Raider(pygame.sprite.Sprite):
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
        self.sprites = self.spritegroups
        self.health = 3
        # Variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # Variables for moving
        self.maxspd = 7
        self.spdy = 8

    def update(self):
        # Slow down when knockbacked
        if self.spdy < self.maxspd * 0.8:
            self.spdy += 1
            
        self.animate()
        self.rect.y += self.spdy

        if self.rect.top > self.surf_h:
            self.kill()

        # Delete object if it goes off-screen or has <= 0 health
        if self.rect.top > self.surf_h or self.health <= 0:
            self.kill()

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

class Fatty(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.surf = data["surface"]
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = data["coords"][0]
        self.rect.y = data["coords"][1]
        self.spritegroups = data["spritegroups"]
        self.sprites = self.spritegroups[0]
        self.e_lasers = self.spritegroups[1]
        self.laser_img = data["laser_img"]
        self.bullet = data["bullet"]
        self.health = 4
        # Variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # Variables for shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 3000
        # Variables for moving
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
            f1 = self.bullet(self.surf, self.laser_img, self.rect.centerx, self.rect.bottom, 10, 8)
            f2 = self.bullet(self.surf, self.laser_img, self.rect.centerx, self.rect.bottom, -10, 9)
            self.sprites.add(f1)
            self.sprites.add(f2)
            self.e_lasers.add(f1)
            self.e_lasers.add(f2)
            self.spdy -= 10 # Recoil

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

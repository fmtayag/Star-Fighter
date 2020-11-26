import pygame, random, numpy

class Player(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.orient = "normal"
        self.lvls = ["cadet", "captain", "admiral"]
        self.cur_lvl = 0
        self.lvl = self.lvls[self.cur_lvl]
        self.surf = data["surface"]
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()
        self.images = data["images"]
        self.image = self.images[self.lvl][self.orient][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = data["coords"][0]
        self.rect.bottom = data["coords"][1]
        self.laser_img = data["laser_img"]
        self.laser_sfx = data["laser_sfx"]
        self.bullet = data["bullet_class"]
        self.health = 100
        # Sprite groups
        self.spritegroups = data["sprite_groups"]
        self.sprites = self.spritegroups[0]
        self.p_lasers = self.spritegroups[1]
        # Speed
        self.movspd = 1
        self.maxspd = 5
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
        # For spawning animation
        self.spawn_imgs = data["spawn_imgs"] # TODO

    def update(self):
        # Reset ship's orientation
        self.orient = "normal"

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.spdy -= self.movspd
            self.spdy = numpy.clip(self.spdy, -self.maxspd, self.maxspd)
        if pressed[pygame.K_s]:
            self.spdy += self.movspd
            self.spdy = numpy.clip(self.spdy, -self.maxspd, self.maxspd)
        if pressed[pygame.K_a]:
            self.spdx -= self.movspd
            self.spdx = numpy.clip(self.spdx, -self.maxspd, self.maxspd)
            self.orient = "left"
        if pressed[pygame.K_d]:
            self.spdx += self.movspd
            self.spdx = numpy.clip(self.spdx, -self.maxspd, self.maxspd)
            self.orient = "right"
        if pressed[pygame.K_SPACE]:
            self.shoot()

        # Check if object collides with window bounds
        if self.rect.top < 0:
            self.spdy = 1
        elif self.rect.bottom > self.surf_h:
            self.spdy = -1
        elif self.rect.left < 0:
            self.spdx = 1
        elif self.rect.right > self.surf_w:
            self.spdx = -1

        # Animate the sprite
        self.animate()

        # Move the object
        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            self.laser_sfx.play()
            if self.lvl == "cadet":
                l = self.bullet(self.surf, self.laser_img, self.rect.centerx,
                          self.rect.top-32, 0, -8)
                self.sprites.add(l)
                self.p_lasers.add(l)
            elif self.lvl == "captain":
                offset_x = [-13,13]
                speed_x = [-1,1]
                for i in range(2):
                    l = self.bullet(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
                              self.rect.top-32, speed_x[i], -8)
                    self.sprites.add(l)
                    self.p_lasers.add(l)
            elif self.lvl == "admiral":
                offset_x = [-13,0,13]
                offset_y = [-6,-32,-6]
                speed_x = [-1,0,1]
                for i in range(3):
                    l = self.bullet(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
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

    def explode(self, explode_func, xpos, ypos):
        explode_func(xpos, ypos)

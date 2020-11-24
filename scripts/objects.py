import pygame, numpy, random

# Classes =========================================================================
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

    def update(self):
        # Reset ship's orientation
        self.orient = "normal"
        #print(f"X: {self.spdx}, Y: {self.spdy}")
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
        #self.draw_hp()

        # Move the object
        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            if self.lvl == "cadet":
                l = Laser(self.surf, self.laser_img, self.rect.centerx,
                          self.rect.top-32, 0, -8)
                self.sprites.add(l)
                self.p_lasers.add(l)
            elif self.lvl == "captain":
                offset_x = [-13,13]
                speed_x = [-1,1]
                for i in range(2):
                    l = Laser(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
                              self.rect.top-32, speed_x[i], -8)
                    self.sprites.add(l)
                    self.p_lasers.add(l)
            elif self.lvl == "admiral":
                offset_x = [-13,0,13]
                offset_y = [-6,-32,-6]
                speed_x = [-1,0,1]
                for i in range(3):
                    l = Laser(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
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

class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, image, xpos, ypos, speedx, speedy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos
        self.spdx = speedx
        self.spdy = speedy
        self.surf = surface
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()

    def update(self):
        self.rect.x += self.spdx
        self.rect.y += self.spdy

        if (self.rect.bottom < 0 or
            self.rect.top > self.surf_h):
            self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self, image, xpos, ypos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.bottom = ypos
        self.lifetime = 100
        self.timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.timer > self.lifetime:
            self.kill()

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
        self.health = 2
        # Variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # Variables for shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 1500
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
            l = Laser(self.surf, self.laser_img, self.rect.centerx,
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

class SpawnAnim(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = data["coords"][0]
        self.rect.y = data["coords"][1]
        self.spritegroups = data["spritegroups"]
        self.sprites = self.spritegroups[0]
        self.enemies = self.spritegroups[1]
        self.spawndata = data["spawndata"]
        self.spawnclass = data["spawnclass"]
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        self.frame = 0

    def update(self):
        self.animate()
        if self.frame == 3:
            spawn = self.spawnclass(self.spawndata)
            self.sprites.add(spawn)
            self.enemies.add(spawn)
            self.kill()
            
    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame == 4:
                self.frame = 0
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect()
            #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
            self.rect.x = old_rectx
            self.rect.y = old_recty

class Explosion(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.surface = data["surface"]
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = data["xpos"]
        self.rect.bottom = data["ypos"]
        # variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1

            if self.frame == 4:
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

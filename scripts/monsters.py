import pygame, random, numpy

class Monster(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.WIN_RES = data["WIN_RES"]
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(64, WIN_RES["w"]-64)
        self.rect.y = random.randrange(0, 100)
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

class Hellfighter(pygame.sprite.Sprite):
    def __init__(self, win_res, images, sprite_supergroup, Bullet, bullet_img, player):
        super().__init__()
        self.win_res = win_res
        self.images = images
        self.image = self.images["spawning"][0]
        self.rect = self.image.get_rect()
        self.rect.x = 100 # TODO
        self.rect.y = 100 # TODO
        self.Bullet = Bullet
        self.bullet_img = bullet_img
        self.health = 2
        self.player = player
        # Sprite groups
        self.sprite_supergroup = sprite_supergroup
        self.sprites = sprite_supergroup["sprites"]
        self.e_lasers = sprite_supergroup["e_lasers"]
        # For animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 1000
        # For moving
        self.movspd = random.randrange(2,3)
        self.spdx = 0
        self.spdy = 2
        # For the "chase" mode
        self.chase_delay = random.randrange(250, 400)
        self.chase_timer = pygame.time.get_ticks()
        # The point at which the object will stop moving on the y-axis
        self.max_disty = self.win_res["w"] * (random.randrange(2, 5) / 10)
        # For spawn animation
        self.spawned = False
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 150
        self.spawn_frame = 0

    def update(self):
        if not self.spawned:
            self.spawn()
        else:
            # Decelerate on the y-axis, for the knockback effect
            if self.spdy < 1:
                self.spdy += 1

            # Check if monster collides with border
            if self.rect.left < 0:
                self.spdx = 3
            elif self.rect.right > self.win_res["w"]:
                self.spdx = -3

            # Stop on the specified y-axis line
            if self.rect.bottom > self.max_disty:
                self.rect.y -= 1

            # Delete object if it goes off-screen or has <= 0 health
            if self.rect.top > self.win_res["h"] or self.health <= 0:
                self.kill()

            self.animate()
            self.shoot()
            self.chase()
            self.rect.x += self.spdx
            self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay and self.player.rect.top > self.rect.y:
            self.shoot_timer = now
            l = self.Bullet(self.win_res["h"], self.bullet_img, self.rect.centerx,
                      self.rect.bottom, 0, 8)
            self.sprites.add(l)
            self.e_lasers.add(l)

    def chase(self):
        now = pygame.time.get_ticks()
        if now - self.chase_timer > self.chase_delay:
            self.chase_timer = now
            if self.rect.centerx < self.player.rect.centerx:
                self.spdx = self.movspd
            elif self.rect.centerx > self.player.rect.centerx:
                self.spdx = -self.movspd

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images["normal"][self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.spawn_timer = now
            self.spawn_frame += 1
            if self.spawn_frame == 3:
                self.spawned = True
            self.image = self.images["spawning"][self.spawn_frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

class Raider(pygame.sprite.Sprite):
    def __init__(self, win_res, images):
        super().__init__()
        self.win_res = win_res
        self.images = images
        self.image = self.images["spawning"][0]
        self.rect = self.image.get_rect()
        self.rect.x = 100 # TODO
        self.rect.y = 100 # TODO
        self.health = 4
        # For moving
        self.maxspd = 8
        self.spdy = 10
        # For animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # For spawning animation
        self.spawned = False
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 150
        self.spawn_frame = 0

    def update(self):
        if not self.spawned:
            self.spawn()
        else:
            # Slow down when knockbacked
            if self.spdy < self.maxspd * 0.8:
                self.spdy += 1

            # Delete object if it goes off-screen or has <= 0 health
            if self.rect.top > self.win_res["h"] or self.health <= 0:
                self.kill()

            self.animate()
            self.rect.y += self.spdy

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images["normal"][self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.spawn_timer = now
            self.spawn_frame += 1
            if self.spawn_frame == 3:
                self.spawned = True
            self.image = self.images["spawning"][self.spawn_frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

class Fatty(pygame.sprite.Sprite):
    def __init__(self, win_res, images, sprite_supergroup, Bullet, bullet_img):
        super().__init__()
        self.win_res = win_res
        self.images = images
        self.image = self.images["spawning"][0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.sprite_supergroup = sprite_supergroup
        self.sprites = self.sprite_supergroup["sprites"]
        self.e_lasers = self.sprite_supergroup["e_lasers"]
        self.Bullet = Bullet
        self.bullet_img = bullet_img
        self.health = 4
        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = 3000
        # For moving
        self.spdx = random.choice([-1,1])
        self.spdy = 0
        # For animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # For spawning animation
        self.spawned = False
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 150
        self.spawn_frame = 0
        # the point at which the object will stop moving on the y-axis
        self.max_disty = self.win_res["h"] * (random.randrange(2, 5) / 10)

    def update(self):
        if not self.spawned:
            self.spawn()
        else:
            # Slow down when knockbacked
            if self.spdy < 1:
                self.spdy += 1

            # Check if monster collides with border
            if self.rect.left < 0:
                self.spdx = 1
            elif self.rect.right > self.win_res["w"]:
                self.spdx = -1

            # Stop on the specified y-axis line
            if self.rect.bottom > self.max_disty:
                self.rect.y -= 1

            # Delete object if it goes off-screen or has <= 0 health
            if self.rect.top > self.win_res["h"] or self.health <= 0:
                f1 = self.Bullet(self.win_res, self.bullet_img, self.rect.centerx, self.rect.bottom, random.choice([10,-10]), 8)
                self.sprites.add(f1)
                self.e_lasers.add(f1)
                self.kill()

            self.animate()
            self.shoot()
            self.rect.x += self.spdx
            self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            f1 = self.Bullet(self.win_res, self.bullet_img, self.rect.centerx, self.rect.bottom, 10, 8)
            f2 = self.Bullet(self.win_res, self.bullet_img, self.rect.centerx, self.rect.bottom, -10, 9)
            self.sprites.add(f1)
            self.sprites.add(f2)
            self.e_lasers.add(f1)
            self.e_lasers.add(f2)
            self.spdy -= 10 # Recoil effect

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images["normal"][self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

    def spawn(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_timer > self.spawn_delay:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.spawn_timer = now
            self.spawn_frame += 1
            if self.spawn_frame == 3:
                self.spawned = True
            self.image = self.images["spawning"][self.spawn_frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

class Bomb(Monster):
    def __init__(self, data):
        super().__init__(data)

import pygame

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
        self.frame_delay = 150
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
        self.rect.centerx = data["coords"][0]
        self.rect.bottom = data["coords"][1]
        # variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # Play the explosion sound effect
        data["explosion_sfx"].play()

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

# Unused! =========================================================================
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

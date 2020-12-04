import pygame, random

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
        self.chosen_sfx = random.choice(data["explosions_sfx"])
        self.chosen_sfx.play()

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

class Particle():
    def __init__(self, window, win_res, x, y):
        self.window = window
        self.win_res = win_res
        self.x = x
        self.y = y
        self.spdx = random.choice([num for num in range(-8,8) if num not in [-1,0,1]])
        self.spdy = random.choice([num for num in range(-8,8) if num not in [-1,0,1]])
        self.size = random.choice([4,8])
        self.color = random.choice([(255,252,64),
                                    (255,213,65),
                                    (249,163,27)])

    def update(self):
        self.x += self.spdx
        self.y += self.spdy
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size))

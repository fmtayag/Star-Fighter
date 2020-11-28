import pygame, numpy

class Upgrade(pygame.sprite.Sprite):
    def __init__(self, surface, images, center):
        super().__init__()
        self.surf_h = surface.get_height()
        self.type = str()
        self.roll_type()
        self.images = images
        self.image = self.images[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        # For animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100

    def update(self):
        self.animate()
        self.rect.y += self.speedy
        # Delete self if it moves off window
        if self.rect.top > self.surf_h:
            self.kill()

    def roll_type(self):
        choices = ["gun", "coin", "hp"]
        roll = numpy.random.choice(choices, p=[0.05, 0.85, 0.10])
        self.type = roll

    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame == 4:
                self.frame = 0
            self.image = self.images[self.type][self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty

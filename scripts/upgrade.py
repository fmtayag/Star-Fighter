import pygame, numpy

class Upgrade(pygame.sprite.Sprite):
    def __init__(self, surface, images, center):
        super().__init__()
        self.surf_h = surface.get_height()
        self.type = str()
        self.roll_type()
        self.images = images
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # Delete self if it moves off window
        if self.rect.top > self.surf_h:
            self.kill()

    def roll_type(self):
        choices = ["gun", "coin", "hp"]
        roll = numpy.random.choice(choices, p=[0.05, 0.85, 0.10])
        self.type = roll

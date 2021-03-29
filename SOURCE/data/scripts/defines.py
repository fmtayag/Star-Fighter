import pygame

# Sprite groups
all_sprites_g = pygame.sprite.Group()
hostiles_g = pygame.sprite.Group()
p_bullets_g = pygame.sprite.Group()
e_bullets_g = pygame.sprite.Group()

# PLAYER DEFINES
PLAYER_SPEED = 255
PLAYER_BULLET_SPEED = 600
PLAYER_SHOOT_DELAY = 125
PLAYER_INCREASE_BULLET_DELAY = 50
PLAYER_INCREASE_BULLET_TICK = 25
PLAYER_WEAK_BULLET_DELAY = 200
PLAYER_WEAK_BULLET_TICK = 10
PLAYER_DEFAULT_GUN_LEVEL = 3 # Max of 3, Min of 1. Don't change unless debugging.
PLAYER_BULLET_DAMAGE = 1

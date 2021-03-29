import pygame

# GLOBAL DIFFICULTY VARIABLE
g_diff = "MEDIUM"

# SPRITE GROUPS
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

# HELLFIGHTER DEFINES
HELLFIGHTER_SPEED = {
    "EASY": 100,
    "MEDIUM": 200,
    "HARD": 300
}
HELLFIGHTER_SHOOT_DELAY = {
    "EASY": 500,
    "MEDIUM": 400,
    "HARD": 300
}
HELLFIGHTER_ACCURACY = {
    "EASY": 0.6,
    "MEDIUM": 0.4,
    "HARD": 0.2
} 
HELLFIGHTER_BULLET_SPEED = {
    "EASY": 200,
    "MEDIUM": 300,
    "HARD": 400
}
HELLFIGHTER_BULLET_DAMAGE = {
    "EASY": 0.5,
    "MEDIUM": 1,
    "HARD": 1.5
}
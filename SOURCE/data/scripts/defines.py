import pygame
import pygame.math

Vec2 = pygame.math.Vector2

# GLOBAL DIFFICULTY VARIABLE
g_diff = "MEDIUM" # TODO - pass this variable onto the sprites

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

# FATTY DEFINES
FATTY_SPEED = {
    "EASY": 100,
    "MEDIUM": 150,
    "HARD": 200
}
FATTY_SHOOT_DELAY = {
    "EASY": 2000,
    "MEDIUM": 1500,
    "HARD": 1200
}
FATTY_LARGE_BULLET_SPEED = {
    "EASY": 200,
    "MEDIUM": 300,
    "HARD": 400
}
FATTY_SMALL_BULLET_SPEED = {
    "EASY": 100,
    "MEDIUM": 200,
    "HARD": 300
}
FATTY_BULLET_DAMAGE = {
    "EASY": 0.5,
    "MEDIUM": 1,
    "HARD": 1.5
}
FATTY_BULLET_DIRECTION = [
    Vec2(1,0), # To Right
    Vec2(1,1), # To Bottom Right
    Vec2(0,1), # To Bottom
    Vec2(-1,1), # To Bottom Left
    Vec2(-1,0), # To Left
]
FATTY_BULLET_SPEED_X = [
    1,
    2,
    3,
    2,
    1
]
FATTY_BULLET_SPEED_Y = [
    2,
    1,
    2,
    1,
    2
]

# RAIDER DEFINES 
RAIDER_SPEED = {
    "EASY": 200,
    "MEDIUM": 250,
    "HARD": 300
}
RAIDER_DASH_THRESHOLD = {
    "EASY": 0.5,
    "MEDIUM": 0.3,
    "HARD": 0.2
}
RAIDER_MAX_SPEED = {
    "EASY": 500,
    "MEDIUM": 600,
    "HARD": 700
} 

# HELLEYE DEFINES
HELLEYE_BULLET_DIRECTION = (
    Vec2(0,-1),
    Vec2(1,-1),
    Vec2(1,0),
    Vec2(1,1),
    Vec2(0,1),
    Vec2(-1,1),
    Vec2(-1,0),
    Vec2(-1,-1)
)
HELLEYE_SHOOT_DELAY = {
    "EASY": 900,
    "MEDIUM": 700,
    "HARD": 500
}
HELLEYE_SPEED = {
    "EASY": 50,
    "MEDIUM": 100,
    "HARD": 200
}
HELLEYE_BULLET_SPEED = {
    "EASY": 50,
    "MEDIUM": 100,
    "HARD": 150
}
HELLEYE_BULLET_DAMAGE = {
    "EASY": 0.5,
    "MEDIUM": 1,
    "HARD": 1.5
}
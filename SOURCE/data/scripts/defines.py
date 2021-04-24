import pygame, pygame.math, os

Vec2 = pygame.math.Vector2

# WINDOW AND METADATA DEFINES ==================================================
WIN_RES = {"w": 320, "h": 480}
TITLE = "Star Fighter"
AUTHOR = "zyenapz"
VERSION = "1.1.0"

# DIRECTORIES ==================================================================
GAME_DIR = os.path.dirname("..") # This works apparently...what the fuck?
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "font")
IMG_DIR = os.path.join(DATA_DIR, "img")
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
GAME_FONT = os.path.join(FONT_DIR, "04B_03__.TTF")

# LOOP DEFINES =================================================================
FPS = 60
DEBUG_MODE = False

# BG AND PARALLAX DEFINES ======================================================
BG_SPD = 25
PAR_SPD = 50

# FONT AND IMAGE DEFINES =======================================================
SCALE = 2
FONT_SIZE = 16

# DIFFICULTY LIST ==============================================================
DIFFICULTIES = ("EASY", "MEDIUM", "HARD")

# SPRITE GROUPS ================================================================
all_sprites_g = pygame.sprite.Group()
hostiles_g = pygame.sprite.Group()
powerups_g = pygame.sprite.Group()
p_bullets_g = pygame.sprite.Group()
e_bullets_g = pygame.sprite.Group()
sentries_g = pygame.sprite.Group()
hellfighters_g = pygame.sprite.Group()

# EFFECTS DEFINES =============================================================
EP_YELLOW1 = (255,222,18)
EP_YELLOW2 = (255,205,5)
EP_YELLOW3 = (255,161,15)
EP_COLORS = (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3)

# Score Powerup Colors
SCR_BLUE1 = (67,169,247)
SCR_BLUE2 = (20,98,203)
SCR_YELLOW1 = (255,252,64)
SCR_YELLOW2 = (227,165,7)
SCR_COLORS = (SCR_BLUE1, SCR_BLUE2, SCR_YELLOW1, SCR_YELLOW2)

# Health Powerup Colors
HP_RED1 = (209,28,29)
HP_RED2 = (140,7,34)
HP_RED3 = (79,0,46)
HP_COLORS = (HP_RED1, HP_RED2)

# Gun powerup colors
WHITE1 = (255,255,255)
SKYBLUE1 = (145,246,255)
SKYBLUE2 = (118,219,245)
GP_COLORS = (WHITE1, SKYBLUE1, SKYBLUE2)

# Sentry powerup colors
PURPLE1 = (226,149,245)
PURPLE2 = (163,110,204)
SP_COLORS = (WHITE1, PURPLE1, PURPLE2) 

# ENTITIES' COLLISION RADII ====================================================
PLAYER_RADIUS = 14
PLAYER_BULLET_RADIUS = 8
SMALL_BULLET_RADIUS = 8
FATTY_BULLET_RADIUS = 8
ENEMY_RADIUS = 16
POWERUP_RADIUS = 24
SENTRY_RADIUS = 16
SENTRY_BULLET_RADIUS = 8

# ENEMY SPAWN DEFINES ===========================================================
GAME_STAGES = ("EARLY", "MID", "LATE")
SPAWN_ROLLS = {
    "EARLY": ("HELLFIGHTER", "RAIDER"),
    "MID": ("HELLFIGHTER", "RAIDER", "FATTY"),
    "LATE": ("HELLFIGHTER", "RAIDER", "FATTY", "SOLTURRET", "HELLEYE")
}
SPAWN_WEIGHTS = {
    "EARLY": (90, 20),
    "MID": (60, 10, 30),
    "LATE": (15, 10, 30, 30, 15)
}
MAX_ENEMY_COUNT = {
    "EARLY": 3,
    "MID": 4,
    "LATE": 5
}
SPAWN_DELAY = { # In ticks
    "EARLY": 1300,
    "MID": 1000,
    "LATE": 800
}
MID_STAGE_SCORE_TRIGGER = {
    "EASY": 500,
    "MEDIUM": 800,
    "HARD": 900
}
LATE_STAGE_SCORE_TRIGGER = {
    "EASY": 1200,
    "MEDIUM": 1600,
    "HARD": 2800
}
MAX_SOLTURRET_COUNT = 2
MAX_HELLEYE_COUNT = 1
MAX_FATTY_COUNT = 2

# SCORE DEFINES ================================================================
SCORE_MULTIPLIER = {
    "EASY": 0.50,
    "MEDIUM": 1.00,
    "HARD": 2.00
}

SCORE_WORTH = {
    "HELLFIGHTER": 10,
    "RAIDER": 20,
    "FATTY": 30,
    "SOLTURRET": 50,
    "HELLEYE": 70
}

# PLAYER DEFINES ===============================================================
PLAYER_SPEED = 250
PLAYER_BULLET_SPEED = 600
PLAYER_SHOOT_DELAY = 150
PLAYER_INCREASE_BULLET_DELAY = 50
PLAYER_INCREASE_BULLET_TICK = 25
PLAYER_WEAK_BULLET_DELAY = 200
PLAYER_WEAK_BULLET_TICK = 10
PLAYER_DEFAULT_GUN_LEVEL = 1 # Max of 3, Min of 1. Don't change unless debugging.
PLAYER_MAX_GUN_LEVEL = 3 # Don't change.
PLAYER_BULLET_DAMAGE = 1
PLAYER_HEALTH = 20
PLAYER_MAX_HEALTH = 20

# SENTRY DEFINES ===============================================================
SENTRY_HEALTH = 15
MAX_SENTRY_COUNT = 2

# POWERUP DEFINES ==============================================================
POWERUP_SPEED = {
    "EASY": 100,
    "MEDIUM": 200,
    "HARD": 300
}
POWERUP_TYPES = (
    "GUN",
    "HEALTH",
    "SCORE",
    "SENTRY"
)
POWERUP_TYPES_WEIGHTS_EARLY = (
    0, # GUN 
    20, # HEALTH
    80, # SCORE
    0 # SENTRY
)
POWERUP_TYPES_WEIGHTS_MID = (
    50, # GUN 
    30, # HEALTH
    15, # SCORE
    5 # SENTRY
)
POWERUP_TYPES_WEIGHTS_LATE = (
    25, # GUN 
    40, # HEALTH
    5, # SCORE
    30 # SENTRY
) 
POWERUP_TYPES_WEIGHTS = {
    "EARLY": POWERUP_TYPES_WEIGHTS_EARLY,
    "MID": POWERUP_TYPES_WEIGHTS_MID,
    "LATE": POWERUP_TYPES_WEIGHTS_LATE 
}
POWERUP_HEALTH_AMOUNT = {
    "EASY": 10,
    "MEDIUM": 5,
    "HARD": 4
}
POWERUP_ROLL_CHANCE = {
    "EASY": 10,
    "MEDIUM": 20,
    "HARD": 30
}
POWERUP_SCORE_BASE_WORTH = 50
HEALTH_PICKUP_HP_THRESHOLD = PLAYER_MAX_HEALTH * 0.6
SUBSTITUTE_POWERUP = "SCORE"

# ENEMY DEFINES ================================================================
ENEMY_COLLISION_DAMAGE = 10

# HELLFIGHTER DEFINES ==========================================================
HELLFIGHTER_SPEED = {
    "EASY": 150,
    "MEDIUM": 200,
    "HARD": 250
}
HELLFIGHTER_SHOOT_DELAY = {
    "EASY": 700,
    "MEDIUM": 600,
    "HARD": 500
}
HELLFIGHTER_RANGE = {
    "EASY": 0.1,
    "MEDIUM": 0.2,
    "HARD": 0.3
} 
HELLFIGHTER_BULLET_SPEED = {
    "EASY": 250,
    "MEDIUM": 300,
    "HARD": 350
}
HELLFIGHTER_BULLET_DAMAGE = {
    "EASY": 0.5,
    "MEDIUM": 1,
    "HARD": 1.5
}
HELLFIGHTER_HEALTH = {
    "EASY": 2,
    "MEDIUM": 3,
    "HARD": 4
}

# FATTY DEFINES ================================================================
FATTY_SPEED = {
    "EASY": 50,
    "MEDIUM": 75,
    "HARD": 100
}
FATTY_SHOOT_DELAY = {
    "EASY": 2000,
    "MEDIUM": 1500,
    "HARD": 1300
}
FATTY_LARGE_BULLET_SPEED = {
    "EASY": 200,
    "MEDIUM": 300,
    "HARD": 400
}
FATTY_SMALL_BULLET_SPEED = {
    "EASY": 125,
    "MEDIUM": 150,
    "HARD": 175
}
FATTY_BULLET_DAMAGE = {
    "EASY": 0.75,
    "MEDIUM": 1,
    "HARD": 1.25
}
FATTY_BULLET_DIRECTION = (
    Vec2(1,0), # To Right
    Vec2(1,1), # To Bottom Right
    Vec2(0,1), # To Bottom
    Vec2(-1,1), # To Bottom Left
    Vec2(-1,0), # To Left
)
FATTY_BULLET_SPEED_X = (
    1,
    2,
    3,
    2,
    1
)
FATTY_BULLET_SPEED_Y = (
    2,
    1,
    2,
    1,
    2
)
FATTY_HEALTH = {
    "EASY": 4,
    "MEDIUM": 5,
    "HARD": 6
}

# RAIDER DEFINES ===============================================================
RAIDER_SPEED = {
    "EASY": 200,
    "MEDIUM": 250,
    "HARD": 300
}
RAIDER_DASH_RANGE = {
    "EASY": 0.5,
    "MEDIUM": 0.3,
    "HARD": 0.2
}
RAIDER_MAX_SPEED = {
    "EASY": 500,
    "MEDIUM": 600,
    "HARD": 700
}
RAIDER_HEALTH = {
    "EASY": 2,
    "MEDIUM": 3,
    "HARD": 4
}

# SOLTURRET DEFINES ============================================================
SOLTURRET_SHOOT_DELAY = {
    "EASY": 700,
    "MEDIUM": 500,
    "HARD": 400
}
SOLTURRET_BULLET_SPEED = {
    "EASY": 200,
    "MEDIUM": 250,
    "HARD": 300
}
SOLTURRET_BULLET_DAMAGE = {
    "EASY": 1.5,
    "MEDIUM": 2.0,
    "HARD": 3.0
}
SOLTURRET_HEALTH = {
    "EASY": 8,
    "MEDIUM": 10,
    "HARD": 12
}

# HELLEYE DEFINES ==============================================================
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
    "HARD": 600
}
HELLEYE_SPEED = {
    "EASY": 50,
    "MEDIUM": 100,
    "HARD": 150
}
HELLEYE_BULLET_SPEED = {
    "EASY": 150,
    "MEDIUM": 200,
    "HARD": 225
}
HELLEYE_BULLET_DAMAGE = {
    "EASY": 1.5,
    "MEDIUM": 2.0,
    "HARD": 3.0
}
HELLEYE_HEALTH = {
    "EASY": 10,
    "MEDIUM": 15,
    "HARD": 18
}
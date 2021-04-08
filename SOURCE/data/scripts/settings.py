import os

# Loop =========================================================================
FPS = 60
DEBUG_MODE = False

# Background and Parallax ======================================================
BG_SPD = 25
PAR_SPD = 50

# Colors =======================================================================
BLACK = (0,0,0)
WHITE = (235,235,235)
GRAY = (100,100,100)
RED = (180,32,42)
GOLD = (255,215,0)
PURPLE = (219,84,180)

# Window Resolution and Metadata ===============================================
WIN_RES = {"w": 320, "h": 480}
TITLE = "Star Fighter"
AUTHOR = "zyenapz"
VERSION = "1.1.0"
SCALE = 2 # For image scale
FONT_SIZE = 16

# Directories ===================================================================
GAME_DIR = os.path.dirname("..") # This works apparently...what the fuck?
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "font")
IMG_DIR = os.path.join(DATA_DIR, "img")
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
GAME_FONT = os.path.join(FONT_DIR, "04B_03__.TTF")
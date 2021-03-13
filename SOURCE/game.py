#####################################
# StarFighter                       #
# Programmed by: zyenapz            #
#   - E-mail: zyenapz@gmail.com     #
#   - Website: zyenapz.github.io    #
# Soundtrack by: yoitsrion          #
#   - Soundcloud: yoitsrion         #
# Font: Press Start                 #
#   - By: codeman38 (awesome dude!!)#
#   - Downloaded from 1001fonts.com #
#####################################

# Import libraries =============================================================
try:
    import pygame, os, random, math
    from pygame.locals import *
    from itertools import repeat
    from data.scripts.bullets import Laser, Fireball
    from data.scripts.monsters import Hellfighter, Raider, Fatty, Bouncy
    from data.scripts.player import Player
    from data.scripts.effects import Explosion, Particle
    from data.scripts.difficulty import max_enemy, sd_subtractor
    from data.scripts.draw import draw_background, draw_text, draw_hp, shake
    from data.scripts.upgrade import Upgrade
    from data.scripts.MateriaEngine import (
            load_img, 
            load_sound, 
            sort,
            read_savedata,
            write_savedata,
            Scene,
            SceneManager
        )
except Exception as e:
    print(e)
    exit()

# Initialize pygame ============================================================
pygame.init()

# Program variables ============================================================
WIN_RES = {"w": 640, "h": 780}
TITLE = "Star Fighter"
AUTHOR = "zyenapz"
VERSION = "1.0"
# Colors
BLACK = (0,0,0)
WHITE = (235,235,235)
GRAY = (100,100,100)
RED = (180,32,42)
GOLD = (255,215,0)
PURPLE = (219,84,180)
# FPS and timing
spawn_delay = 2000
# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
FONT_DIR = os.path.join(DATA_DIR, "font")
game_font = os.path.join(FONT_DIR, "pixelart.ttf")
scores_path = os.path.join(SCRIPTS_DIR, "scores.dat")
# Other variables
hi_scores = sort(read_savedata(scores_path))
score = 0
background_y = 0 # For the background's y coordinate
backgroundp_y = 0 # For parallax's y coordinate
offset = repeat((0, 0)) # For screen shake
scale = 4 # For scaling images
particle_colors = [(255,252,64),(255,213,65),(249,163,27)]
LEGEND_SCORE = 999 # It's a secret ;)

# Images =======================================================================

player_imgs = dict()

# Load and store cadet player frames
player_cadet = dict()
player_cadet["left"] = [
    load_img("player_cadet_l1.png", IMG_DIR, scale),
    load_img("player_cadet_l2.png", IMG_DIR, scale)
]
player_cadet["normal"] = [
    load_img("player_cadet_n1.png", IMG_DIR, scale),
    load_img("player_cadet_n2.png", IMG_DIR, scale)
]
player_cadet["right"] = [
    load_img("player_cadet_r1.png", IMG_DIR, scale),
    load_img("player_cadet_r2.png", IMG_DIR, scale)
]
player_imgs["cadet"] = player_cadet

# Load and store captain player frames
player_captain = dict()
player_captain["left"] = [
    load_img("player_captain_l1.png", IMG_DIR, scale),
    load_img("player_captain_l2.png", IMG_DIR, scale)
]
player_captain["normal"] = [
    load_img("player_captain_n1.png", IMG_DIR, scale),
    load_img("player_captain_n2.png", IMG_DIR, scale)
]
player_captain["right"] = [
    load_img("player_captain_r1.png", IMG_DIR, scale),
    load_img("player_captain_r2.png", IMG_DIR, scale)
]
player_imgs["captain"] = player_captain

# Load and store admiral player frames
player_admiral = dict()
player_admiral["left"] = [
    load_img("player_admiral_l1.png", IMG_DIR, scale),
    load_img("player_admiral_l2.png", IMG_DIR, scale)
]
player_admiral["normal"] = [
    load_img("player_admiral_n1.png", IMG_DIR, scale),
    load_img("player_admiral_n2.png", IMG_DIR, scale)
]
player_admiral["right"] = [
    load_img("player_admiral_r1.png", IMG_DIR, scale),
    load_img("player_admiral_r2.png", IMG_DIR, scale)
]
player_imgs["admiral"] = player_admiral

# Load and store spawning player frames
player_imgs["spawning"] = [
    load_img("player_spawn1.png", IMG_DIR, scale),
    load_img("player_spawn2.png", IMG_DIR, scale),
    load_img("player_spawn3.png", IMG_DIR, scale),
    load_img("player_spawn4.png", IMG_DIR, scale)
]

# Load and store hellfighter images
hfighter_imgs = dict()
hfighter_imgs["normal"] = [
    load_img("hellfighter1.png", IMG_DIR, scale),
    load_img("hellfighter2.png", IMG_DIR, scale)
]
hfighter_imgs["spawning"] = [
    load_img("hf_spawn1.png", IMG_DIR, scale),
    load_img("hf_spawn2.png", IMG_DIR, scale),
    load_img("hf_spawn3.png", IMG_DIR, scale),
    load_img("hf_spawn4.png", IMG_DIR, scale)
]

# Load and store raider images
raider_imgs = dict()
raider_imgs["normal"] = [
    load_img("raider1.png", IMG_DIR, scale),
    load_img("raider2.png", IMG_DIR, scale)
]
raider_imgs["spawning"] = [
    load_img("raider_spawn1.png", IMG_DIR, scale),
    load_img("raider_spawn2.png", IMG_DIR, scale),
    load_img("raider_spawn3.png", IMG_DIR, scale),
    load_img("raider_spawn4.png", IMG_DIR, scale),
]

# Load and store fatty images
fatty_imgs = dict()
fatty_imgs["normal"] = [
    load_img("fatty1.png", IMG_DIR, scale),
    load_img("fatty2.png", IMG_DIR, scale)
]
fatty_imgs["spawning"] = [
    load_img("fatty_spawn1.png", IMG_DIR, scale),
    load_img("fatty_spawn2.png", IMG_DIR, scale),
    load_img("fatty_spawn3.png", IMG_DIR, scale),
    load_img("fatty_spawn4.png", IMG_DIR, scale)
]

# Load and store explosion images
explosion_imgs = [
    load_img("explosion1.png", IMG_DIR, scale),
    load_img("explosion2.png", IMG_DIR, scale),
    load_img("explosion3.png", IMG_DIR, scale),
    load_img("explosion4.png", IMG_DIR, scale)
]

# Load and store upgrade images
upgrade_imgs = dict()
upgrade_imgs["hp"] = [ load_img("upgrd_hp1.png", IMG_DIR, scale),
                       load_img("upgrd_hp2.png", IMG_DIR, scale),
                       load_img("upgrd_hp3.png", IMG_DIR, scale),
                       load_img("upgrd_hp4.png", IMG_DIR, scale) ]
upgrade_imgs["gun"] = [ load_img("upgrd_gun1.png", IMG_DIR, scale),
                        load_img("upgrd_gun2.png", IMG_DIR, scale),
                        load_img("upgrd_gun3.png", IMG_DIR, scale),
                        load_img("upgrd_gun4.png", IMG_DIR, scale) ]
upgrade_imgs["coin"] = [ load_img("upgrd_coin1.png", IMG_DIR, scale),
                         load_img("upgrd_coin2.png", IMG_DIR, scale),
                         load_img("upgrd_coin3.png", IMG_DIR, scale),
                         load_img("upgrd_coin4.png", IMG_DIR, scale) ]

p_laser_img = load_img("laser_player.png", IMG_DIR, scale)
e_laser_img = load_img("laser_enemy.png", IMG_DIR, scale)
fireball_img = load_img("fireball.png", IMG_DIR, scale)

dev_logo_img = load_img("dev_logo.png", IMG_DIR, 6, convert_alpha=True)

background_img = load_img("background.png", IMG_DIR, scale)
background_rect = background_img.get_rect()
backgroundp_img = load_img("background_parallax.png", IMG_DIR, scale)
backgroundp_rect = backgroundp_img.get_rect()

hp_bar_img = load_img("hp_bar.png", IMG_DIR, scale)
hp_bar_rect = hp_bar_img.get_rect()
hp_bar_rect.x = 20
hp_bar_rect.y = 20

score_img = load_img("score_icon.png", IMG_DIR, scale)
score_rect = score_img.get_rect()
score_rect.x = 10
score_rect.y = hp_bar_rect.y + 30

# Sounds =======================================================================

laser_sfx = load_sound("sfx_lasershoot.wav", SFX_DIR, 0.5)
upgrade_sfx = load_sound("sfx_powerup.wav", SFX_DIR, 0.5)
coin_sfx = load_sound("sfx_coinpickup.wav", SFX_DIR, 0.5)
typing_sfx = load_sound("sfx_typing.wav", SFX_DIR, 0.8)
denied_sfx = load_sound("sfx_denied.wav", SFX_DIR, 0.8)
explosions_sfx = [ load_sound("sfx_explosion1.wav", SFX_DIR, 0.5),
                   load_sound("sfx_explosion2.wav", SFX_DIR, 0.5),
                   load_sound("sfx_explosion3.wav", SFX_DIR, 0.5) ]

pygame.mixer.music.load(os.path.join(SFX_DIR, "ost_fighter.ogg"))
pygame.mixer.music.set_volume(0.3)

# Sprite Groups ================================================================

# Sprite groups
sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
p_lasers = pygame.sprite.Group()
e_lasers = pygame.sprite.Group()
upgrades = pygame.sprite.Group()
player_group = pygame.sprite.Group()
particles = list()
bouncies = list() # Bouncies


# Sprite supergroups
p_spr_supergroup = {"sprites": sprites, "p_lasers": p_lasers}
e_spr_supergroup = {"sprites": sprites, "e_lasers": e_lasers}

# Spawner Functions ============================================================

def spawn_explosion(Expl, data, xpos, ypos, sprites):
    data["coords"] = (xpos, ypos)
    e = Expl(data)
    sprites.add(e)

def spawn_hfighter():
    hfighter = Hellfighter(WIN_RES, hfighter_imgs, e_spr_supergroup, Laser, e_laser_img, player)
    enemies.add(hfighter)
    sprites.add(hfighter)

def spawn_raider():
    raider = Raider(WIN_RES, raider_imgs)
    enemies.add(raider)
    sprites.add(raider)

def spawn_fatty():
    fatty = Fatty(WIN_RES, fatty_imgs, e_spr_supergroup, Fireball, fireball_img)
    sprites.add(fatty)
    enemies.add(fatty)

def spawn_particles(x, y, amnt, colors):
    for _ in range(amnt):
        p = Particle(window, WIN_RES, random.randrange(x-10,x), random.randrange(y-10,y), colors)
        particles.append(p)

def spawn_bouncies(window, bouncies):
    for _ in range(5):
        b = Bouncy(window)
        bouncies.append(b)

def draw_bouncies(bouncies):
    for b in bouncies:
        b.draw()

def update_particles():
    for p in particles:
        p.update()

        if (p.x < -p.size or
            p.x > p.win_res["w"] + p.size or
            p.y < -p.size or
            p.y > p.win_res["h"] + p.size):
                particles.remove(p)
                del p

def roll_spawn(score):
    monsters = ["raider","hellfighter", "fatty"]
    roll = None
    if player.cur_lvl < 1 and score < 80:
        choices = random.choices(monsters, [0.25, 0.70, 0.05], k=10)
        roll = random.choice(choices)
    else:
        choices = random.choices(monsters, [0.30,0.55,0.15], k=10)
        roll = random.choice(choices)

    if roll == "raider":
        spawn_raider()
    elif roll == "hellfighter":
        spawn_hfighter()
    elif roll == "fatty":
        spawn_fatty()

# Game loop ====================================================================

class TitleMenu:
    def __init__(self):
        self.surface = pygame.Surface((WIN_RES["w"], 350))
        self.surf_rect = self.surface.get_rect()
        self.font_size = 38
        self.spacing = self.font_size / 2

        # Menu
        self.menu = ("PLAY", "SCORES", "OPTIONS", "CREDITS", "EXIT")
        self.act_m = [1,0,0,0,0] # Active menu
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive menu

        # Selector
        self.selector = pygame.Surface((WIN_RES["w"], self.font_size))
        self.selector.fill("white")
        self.sel_y = self.font_size + self.spacing
        self.sel_m = 0 # multiplier

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and self.sel_m < len(self.menu) - 1:
                    self.act_m[self.sel_m] = 0
                    self.sel_m += 1
                    self.act_m[self.sel_m] = 1
                if event.key == pygame.K_w and self.sel_m > 0:
                    self.act_m[self.sel_m] = 0
                    self.sel_m -= 1
                    self.act_m[self.sel_m] = 1
                if event.key == pygame.K_RETURN:
                    if self.sel_m == len(self.menu) - 1:
                        quit() # TODO - this isn't proper way of exiting the game.

    def update(self):
        self.sel_y = self.font_size*(self.sel_m+1) + self.spacing*(self.sel_m+1)

    def draw(self, window):
        self.surface.fill("black")
        self.surface.set_colorkey("black")
        self.surface.blit(self.selector, (0,self.sel_y))
        draw_text(self.surface, self.menu[0], self.font_size, game_font, self.surf_rect.centerx, self.font_size + self.spacing, self.colors[self.act_m[0]], "centered")
        draw_text(self.surface, self.menu[1], self.font_size, game_font, self.surf_rect.centerx, self.font_size*2 + self.spacing*2, self.colors[self.act_m[1]], "centered")
        draw_text(self.surface, self.menu[2], self.font_size, game_font, self.surf_rect.centerx, self.font_size*3  + self.spacing*3, self.colors[self.act_m[2]], "centered")
        draw_text(self.surface, self.menu[3], self.font_size, game_font, self.surf_rect.centerx, self.font_size*4  + self.spacing*4, self.colors[self.act_m[3]], "centered")
        draw_text(self.surface, self.menu[4], self.font_size, game_font, self.surf_rect.centerx, self.font_size*5  + self.spacing*5, self.colors[self.act_m[4]], "centered")
        window.blit(self.surface, (0,window.get_height()/2 - 80))

class TitleScene(Scene):
    def __init__(self):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, scale)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, scale)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0

        # Logo
        self.logo_img = load_img("logo.png", IMG_DIR, 8, convert_alpha=True)

        # Menu
        self.title_menu = TitleMenu()

    def handle_events(self, events):
        self.title_menu.handle_events(events)

    def update(self, dt):
        self.bg_y += 100 * dt
        self.par_y += 200 * dt
        self.title_menu.update()

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)
        window.blit(self.logo_img, (window.get_width()/2-240, -128))

        # Draw menu
        self.title_menu.draw(window)

def main():

    # Initialize the window
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    window = pygame.display.set_mode((WIN_RES["w"], WIN_RES["h"]))
    window_rect = window.get_rect()
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(load_img("hellfighter1.png", IMG_DIR, 1)) # TODO - change the icon name
    pygame.mouse.set_visible(False)

    # Scene Manager
    manager = SceneManager(TitleScene())

    # Loop variables
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    lf = 0 # Last frame. For calculating delta time (dt)

    # Temporary
    explosion_data = { "surface": window,
                   "images": explosion_imgs,
                   "explosions_sfx": explosions_sfx}
    
    while running:
        # Lock FPS
        clock.tick(FPS)
        pygame.display.set_caption(f"{TITLE} (FPS: {round(clock.get_fps())})")

        # Calculate delta time
        t = pygame.time.get_ticks()
        dt = (t-lf) / 1000.0
        lf = t

        if pygame.event.get(QUIT):
            running = False

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update(dt)
        manager.scene.draw(window)

        pygame.display.flip()

# Run main
main()

# Save high scores to file before exiting
write_savedata(hi_scores, scores_path)

# Quit pygame
pygame.quit()
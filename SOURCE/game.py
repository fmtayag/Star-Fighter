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
import pygame, os, random, math, time
from pygame.locals import *
from itertools import repeat
from data.scripts.bullets import Laser, Fireball
from data.scripts.monsters import Hellfighter, Raider, Fatty, Bouncy
from data.scripts.player import Player
from data.scripts.effects import Explosion, Particle
from data.scripts.difficulty import max_enemy, sd_subtractor
from data.scripts.upgrade import Upgrade
from data.scripts.settings import *
from data.scripts.MateriaEngine import (
    load_img, 
    load_sound, 
    sort,
    read_savedata,
    write_savedata,
    Scene,
    SceneManager,
    draw_background, 
    draw_text,
    shake,
    slice_list
)

# Initialize pygame ============================================================
pygame.init()

# Program variables ============================================================
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
game_font = os.path.join(FONT_DIR, "04B_03__.TTF")
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
pygame.mixer.music.play()

# Sprite Groups ================================================================

# Game loop ====================================================================

class TitleMenu:
    def __init__(self):
        # Surface
        # Warning - options may go beyond the surface and will be not rendered
        self.surface = pygame.Surface((WIN_RES["w"], 350))
        self.surf_rect = self.surface.get_rect()
        
        # Text settings
        self.font_size = 32
        self.spacing = self.font_size / 2

        # Menu
        self.options = ("PLAY", "SCORES", "OPTIONS", "CREDITS", "EXIT")
        self.act_opt = [0 for i in range(len(self.options))] # Active options
        self.act_opt[0] = 1
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive menu

        # Selector
        self.selector = pygame.Surface((WIN_RES["w"], self.font_size + 4))
        self.selector.fill("white")
        self.sel_y = self.font_size + self.spacing
        self.sel_i = 0 # index

    def update(self):
        self.sel_y = self.font_size*(self.sel_i+1) + self.spacing*(self.sel_i+1)

    def draw(self, window):
        self.surface.fill("black")
        self.surface.set_colorkey("black")
        self.surface.blit(self.selector, (0,self.sel_y-3))
        for i in range(len(self.options)):
            draw_text(self.surface, self.options[i], self.font_size, game_font, self.surf_rect.centerx, self.font_size*(i+1) + self.spacing*(i+1), self.colors[self.act_opt[i]], "centered")
        window.blit(self.surface, (0,window.get_height()/2 - 80))

    def select_up(self):
        if  self.sel_i > 0:
            self.act_opt[self.sel_i] = 0
            self.sel_i -= 1
            self.act_opt[self.sel_i] = 1
        else:
            self.act_opt[self.sel_i] = 0
            self.sel_i = len(self.options) - 1
            self.act_opt[self.sel_i] = 1

    def select_down(self):
        if self.sel_i < len(self.options) - 1:
            self.act_opt[self.sel_i] = 0
            self.sel_i += 1
            self.act_opt[self.sel_i] = 1
        else:
            self.act_opt[self.sel_i] = 0
            self.sel_i = 0
            self.act_opt[self.sel_i] = 1

    def get_selected(self):
        return self.options[self.sel_i]

class TitleScene(Scene):
    def __init__(self):
        # Text settings
        self.font_size = 32

        # Background
        self.bg_img = load_img("background.png", IMG_DIR, scale)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, scale)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0

        # Images
        self.logo_img = load_img("logo.png", IMG_DIR, 8, convert_alpha=True)

        # Sounds
        self.select_sfx = load_sound("sfx_select.wav", SFX_DIR, 0.5)

        # Menu object
        self.title_menu = TitleMenu()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.title_menu.select_up()
                    self.select_sfx.play()
                elif event.key == pygame.K_DOWN:
                    self.title_menu.select_down()
                    self.select_sfx.play()
                elif event.key == pygame.K_z:
                    if self.title_menu.get_selected() == "PLAY":
                        print("TODO - PLAY")
                    elif self.title_menu.get_selected() == "SCORES":
                        self.manager.go_to(ScoresScene())
                    elif self.title_menu.get_selected() == "OPTIONS":
                        print("TODO - OPTIONS")
                    elif self.title_menu.get_selected() == "CREDITS":
                        print("TODO - CREDITS")
                    elif self.title_menu.get_selected() == "EXIT":
                        print("TODO - EXIT")

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
        draw_text(window, "Actually...there's no copyright", int(self.font_size/2), game_font, window.get_rect().centerx, window.get_rect().bottom-(self.font_size/2)*2, "WHITE", "centered")

class ScoresTable():
    def __init__(self):
        # Text settings
        self.font_size = 32
        self.spacing = self.font_size / 2

        # Table
        self.table_surf = pygame.Surface((WIN_RES["w"], WIN_RES["h"] / 2))
        self.table_rect = self.table_surf.get_rect()
        #self.table_surf.fill('red')
        
        # Scores - TODO: Just an example
        self.scores = [
            ["MAN", 1000],
            ["WMN", 2100],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106],
            ["LOL", 102],
            ["XMS", 106],
            ["EBL", 107],
            ["LOL", 102],
            ["XMS", 106]
        ]
        self.splice_n = 5
        self.scores = slice_list(self.scores, self.splice_n)
        self.cur_tbl = 0

    def update(self):
        pass

    def draw(self, window):
        self.table_surf.fill("black")
        self.table_surf.set_colorkey("black")

        for i in range(len(self.scores[self.cur_tbl])):
            draw_text(self.table_surf, f"{(i+1)+(self.cur_tbl*self.splice_n)}.", self.font_size, game_font, self.table_rect.centerx * 0.5 + len(str(i)), self.font_size*(i+1) + self.spacing*(i+1), "YELLOW")
            draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][0]}", self.font_size, game_font, self.table_rect.centerx * 0.8, self.font_size*(i+1) + self.spacing*(i+1), "WHITE")
            draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][1]}", self.font_size, game_font, self.table_rect.centerx * 1.3, self.font_size*(i+1) + self.spacing*(i+1), "WHITE")

        # TODO - this is just a placeholder
        draw_text(window, f"PAGE {self.cur_tbl+1} OF {len(self.scores)}", self.font_size, game_font, self.table_rect.centerx, self.table_rect.bottom * 1.25, "WHITE", "centered")

        window.blit(self.table_surf,(0,WIN_RES["h"]/2 - 256))

    def next_table(self):
        if self.cur_tbl < len(self.scores) - 1:
            self.cur_tbl += 1
        
    def prev_table(self):
        if self.cur_tbl > 0:
            self.cur_tbl -= 1

class ScoresControlPanel():
    def __init__(self):
        # Text settings
        self.font_size = 32

        # Panels
        self.sub_panels = ("DIRECTION", "BACK")
        self.active_panel = self.sub_panels[0]
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive options

        # Direction Sub-panel
        self.direction_panel = pygame.Surface((WIN_RES["w"], 64))
        self.dp_rect = self.direction_panel.get_rect()

        # Direction Sub-panel Options
        self.dp_options = ("PREV", "NEXT")
        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[0] = 1

        # Back Sub-panel
        self.back_panel = pygame.Surface((WIN_RES["w"], 64))
        self.bp_rect = self.back_panel.get_rect()

        # Back Sub-panel Option
        self.bp_options = ("BACK")
        self.bp_active = 0

        # Selector
        self.selector = pygame.Surface((self.dp_rect.width*0.5, self.dp_rect.height))
        self.selector.fill("WHITE")
        self.sel_i = 0 # index

    def update(self):
        pass

    def draw(self, window):
        # Set colorkeys
        self.direction_panel.fill("BLACK")
        self.direction_panel.set_colorkey("BLACK")
        self.back_panel.fill("BLACK")
        self.back_panel.set_colorkey("BLACK")

        # Selector
        if self.active_panel == self.sub_panels[0]:
            self.direction_panel.blit(self.selector, (self.dp_rect.centerx*self.sel_i,0))
        elif self.active_panel == self.sub_panels[1]:
            self.back_panel.blit(self.selector, (self.back_panel.get_rect().width/4,0))

        # Direction panel
        draw_text(self.direction_panel, self.dp_options[0], self.font_size, game_font, self.dp_rect.centerx*0.5, self.dp_rect.centery*0.5, self.colors[self.dp_act_opt[0]], "centered")
        draw_text(self.direction_panel, self.dp_options[1], self.font_size, game_font, self.dp_rect.centerx*1.5, self.dp_rect.centery*0.5, self.colors[self.dp_act_opt[1]], "centered")
        window.blit(self.direction_panel, (0,window.get_rect().height*0.7))

        # Back panel
        draw_text(self.back_panel, "BACK", self.font_size, game_font, self.dp_rect.centerx, self.dp_rect.centery*0.5, self.colors[self.bp_active], "centered")
        window.blit(self.back_panel, (0,window.get_rect().height*0.8))

    def move_left(self):
        if self.active_panel == self.sub_panels[0]:
            if self.sel_i > 0:
                self.dp_act_opt[self.sel_i] = 0
                self.sel_i -= 1
                self.dp_act_opt[self.sel_i] = 1

        elif self.active_panel == self.sub_panels[1]:
            self.active_panel = self.sub_panels[0]
            self.sel_i = 0
            self.move_up()

    def move_right(self):
        if self.active_panel == self.sub_panels[0]:
            if self.sel_i < len(self.dp_options)-1:
                self.dp_act_opt[self.sel_i] = 0
                self.sel_i += 1
                self.dp_act_opt[self.sel_i] = 1

        elif self.active_panel == self.sub_panels[1]:
            self.active_panel = self.sub_panels[0]
            self.sel_i = len(self.dp_options)-1
            self.move_up()

    def move_up(self):
        self.active_panel = self.sub_panels[0]
        self.bp_active = 0

        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[self.sel_i] = 1

    def move_down(self):
        self.active_panel = self.sub_panels[1]
        self.bp_active = 1

        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[0] = 0

    def get_active_panel(self):
        return self.active_panel

    def get_dp_selected_option(self):
        if self.active_panel == self.sub_panels[0]:
            return self.dp_options[self.sel_i]

class ScoresScene(Scene):
    def __init__(self):
        # Background
        self.bg_img = load_img("background.png", IMG_DIR, scale)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_y = 0
        self.par_img = load_img("background_parallax.png", IMG_DIR, scale)
        self.par_rect = self.bg_img.get_rect()
        self.par_y = 0

        # Sounds
        self.select_sfx = load_sound("sfx_select.wav", SFX_DIR, 0.5)

        # Scores table
        self.scores_table = ScoresTable()

        # Control panel
        self.control_panel = ScoresControlPanel()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.control_panel.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.control_panel.move_right()
                elif event.key == pygame.K_UP:
                    self.control_panel.move_up()
                elif event.key == pygame.K_DOWN:
                    self.control_panel.move_down()

                elif event.key == pygame.K_z:
                    if self.control_panel.get_active_panel() == "DIRECTION":
                        if self.control_panel.get_dp_selected_option() == "PREV":
                            self.scores_table.prev_table()
                        elif self.control_panel.get_dp_selected_option() == "NEXT":
                            self.scores_table.next_table()
                    elif self.control_panel.get_active_panel() == "BACK":
                        self.manager.go_to(TitleScene())
    
    def update(self, dt):
        self.bg_y += 100 * dt
        self.par_y += 200 * dt

    def draw(self, window):
        draw_background(window, self.bg_img, self.bg_rect, self.bg_y)
        draw_background(window, self.par_img, self.par_rect, self.par_y)

        draw_text(window, "HALL OF FAME", 64, game_font, window.get_rect().centerx, 64, "WHITE", "centered")
        self.scores_table.draw(window)
        self.control_panel.draw(window)

def main():

    # Initialize the window
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    window = pygame.display.set_mode((WIN_RES["w"], WIN_RES["h"]))
    window_rect = window.get_rect()
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(load_img("hellfighter1.png", IMG_DIR, 1)) # TODO - change the icon name
    pygame.mouse.set_visible(False)

    # Scene Manager
    manager = SceneManager(ScoresScene())

    # Loop variables
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    prev_time = time.time()
    dt = 0

    # Temporary
    explosion_data = { "surface": window,
                   "images": explosion_imgs,
                   "explosions_sfx": explosions_sfx}
    
    while running:
        # Lock FPS
        clock.tick(FPS)
        pygame.display.set_caption(f"{TITLE} (FPS: {round(clock.get_fps())})")

        # Calculate delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        if pygame.event.get(QUIT):
            running = False

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update(dt)
        manager.scene.draw(window)

        pygame.display.flip()

# Run main
main()

# Quit pygame
pygame.quit()
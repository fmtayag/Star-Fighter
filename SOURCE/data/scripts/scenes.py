import pygame, sys, random, math
from PIL import Image, ImageDraw
from data.scripts.spawner import Spawner
from data.scripts.sprites import Player
from data.scripts.muda import (
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
    slice_list,
    clamp,
    image_at,
    scale_rect,
    draw_hpbar,
    draw_text2
)
from data.scripts.defines import *
from itertools import repeat

# TITLE SCENE ==================================================================

class TitleMenuWidget:
    def __init__(self, init_selected):
        # Surface
        # Warning - options may go beyond the surface and will be not rendered
        self.surface = pygame.Surface((WIN_RES["w"], 350))
        self.surf_rect = self.surface.get_rect()
        
        self.spacing = FONT_SIZE / 2

        # Menu
        self.options = ("PLAY", "SCORES", "OPTIONS", "CREDITS", "EXIT")
        self.act_opt = [0 for i in range(len(self.options))] # Active options
        self.act_opt[init_selected] = 1
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive menu

        # Selector
        self.selector = pygame.Surface((WIN_RES["w"], FONT_SIZE + 4))
        self.selector.fill("white")
        self.sel_y = FONT_SIZE + self.spacing
        self.sel_i = init_selected # index

    def update(self):
        self.sel_y = FONT_SIZE*(self.sel_i+1) + self.spacing*(self.sel_i+1)

    def draw(self, window):
        self.surface.fill("black")
        self.surface.set_colorkey("black")
        self.surface.blit(self.selector, (0,self.sel_y-3))
        for i in range(len(self.options)):
            draw_text(self.surface, self.options[i], FONT_SIZE, GAME_FONT, self.surf_rect.centerx, FONT_SIZE*(i+1) + self.spacing*(i+1), self.colors[self.act_opt[i]], "centered")
        window.blit(self.surface, (0,window.get_height()/2 - 32))

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
        return self.sel_i

class TitleScene(Scene):
    def __init__(self, init_selected=0):
        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Images
        self.logo_img = load_img("logo.png", IMG_DIR, 4, convert_alpha=True)
        self.logo_rect = self.logo_img.get_rect()
        self.logo_hw = self.logo_rect.width / 2

        # Menu object
        self.title_menu = TitleMenuWidget(init_selected)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.title_menu.select_up()
                elif event.key == pygame.K_DOWN:
                    self.title_menu.select_down()
                elif event.key == pygame.K_z:
                    if self.title_menu.get_selected() == 0:
                        self.manager.go_to(DifficultySelectionScene())
                    elif self.title_menu.get_selected() == 1:
                        self.manager.go_to(ScoresScene())
                    elif self.title_menu.get_selected() == 2:
                        self.manager.go_to(OptionsScene())
                    elif self.title_menu.get_selected() == 3:
                        self.manager.go_to(CreditsScene())
                    elif self.title_menu.get_selected() == 4:
                        sys.exit()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        self.title_menu.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)
        window.blit(self.logo_img, (WIN_RES["w"]/2 - self.logo_hw, -32))

        # Draw menu
        self.title_menu.draw(window)
        draw_text(window, "(Test Build v.Whatever)", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, 30, "WHITE", "centered")
        draw_text(window, "Copydown", FONT_SIZE, GAME_FONT, window.get_rect().centerx, window.get_rect().bottom-(FONT_SIZE/2)*2, "WHITE", "centered")

# SCORES SCENE =================================================================

class ScoresControlWidget():
    def __init__(self):
        # Panels
        self.sub_panels = ("DIRECTION", "BACK")
        self.active_panel = self.sub_panels[0]
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive options

        # Direction Sub-panel
        self.direction_panel = pygame.Surface((WIN_RES["w"], FONT_SIZE*2))
        self.dp_rect = self.direction_panel.get_rect()

        # Direction Sub-panel Options
        self.dp_options = ("PREV", "NEXT")
        self.dp_act_opt = [0 for i in range(len(self.dp_options))] # Active options
        self.dp_act_opt[0] = 1

        # Back Sub-panel
        self.back_panel = pygame.Surface((WIN_RES["w"], FONT_SIZE*2))
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
        draw_text(self.direction_panel, self.dp_options[0], FONT_SIZE, GAME_FONT, self.dp_rect.centerx*0.5, self.dp_rect.centery*0.5, self.colors[self.dp_act_opt[0]], "centered")
        draw_text(self.direction_panel, self.dp_options[1], FONT_SIZE, GAME_FONT, self.dp_rect.centerx*1.5, self.dp_rect.centery*0.5, self.colors[self.dp_act_opt[1]], "centered")
        window.blit(self.direction_panel, (0,window.get_rect().height*0.7))

        # Back panel
        draw_text(self.back_panel, "BACK", FONT_SIZE, GAME_FONT, self.dp_rect.centerx, self.dp_rect.centery*0.5, self.colors[self.bp_active], "centered")
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

class ScoresTableWidget():
    def __init__(self):
        self.spacing = FONT_SIZE / 2

        # Table
        self.table_surf = pygame.Surface((WIN_RES["w"], WIN_RES["h"] / 2))
        self.table_rect = self.table_surf.get_rect()
        #self.table_surf.fill('red')
        
        # Scores - TODO: Just an example. No sorting yet.
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
            draw_text(self.table_surf, f"{(i+1)+(self.cur_tbl*self.splice_n)}.", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.5 + len(str(i)), FONT_SIZE*(i+1) + self.spacing*(i+1), "YELLOW")
            draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][0]}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.8, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")
            draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][1]}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 1.3, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")

        # TODO - this is just a placeholder
        draw_text(window, f"PAGE {self.cur_tbl+1} OF {len(self.scores)}", FONT_SIZE, GAME_FONT, self.table_rect.centerx, self.table_rect.bottom * 1.25, "WHITE", "centered")

        window.blit(self.table_surf,(0,WIN_RES["h"]/2 - 128))

    def next_table(self):
        if self.cur_tbl < len(self.scores) - 1:
            self.cur_tbl += 1
        
    def prev_table(self):
        if self.cur_tbl > 0:
            self.cur_tbl -= 1

class ScoresScene(Scene):
    def __init__(self):
        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Scores table
        self.scores_table = ScoresTableWidget()

        # Control panel
        self.control_widget = ScoresControlWidget()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.control_widget.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.control_widget.move_right()
                elif event.key == pygame.K_UP:
                    self.control_widget.move_up()
                elif event.key == pygame.K_DOWN:
                    self.control_widget.move_down()

                elif event.key == pygame.K_z:
                    if self.control_widget.get_active_panel() == "DIRECTION":
                        if self.control_widget.get_dp_selected_option() == "PREV":
                            self.scores_table.prev_table()
                        elif self.control_widget.get_dp_selected_option() == "NEXT":
                            self.scores_table.next_table()
                    elif self.control_widget.get_active_panel() == "BACK":
                        self.manager.go_to(TitleScene(1))
                elif event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(1))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "HALL OF FAME", FONT_SIZE*2, GAME_FONT, window.get_rect().centerx, 64, "WHITE", "centered")
        self.scores_table.draw(window)
        self.control_widget.draw(window)

# OPTIONS SCENE ================================================================

class OptionsScene(Scene):
    def __init__(self):
        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(2))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "OPTIONS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, "DEV: Not yet done.", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2, "WHITE", "centered")

# CREDITS SCENE ================================================================

class CreditsScene(Scene):
    def __init__(self):
        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(3))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "CREDITS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, "DEV: Not yet done.", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2, "WHITE", "centered")

# DIFFICULTY SELECTION SCENE ================================================================

class DifficultySelectionScene(Scene):
    def __init__(self):
        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(0))
                elif event.key == pygame.K_1:
                    self.manager.go_to(GameScene(0))
                elif event.key == pygame.K_2:
                    self.manager.go_to(GameScene(1))
                elif event.key == pygame.K_3:
                    self.manager.go_to(GameScene(2))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "SELECT DIFFICULTY", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, "1 - Lenient", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2 - 64, "WHITE", "centered")
        draw_text(window, "2 - Fair", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2, "WHITE", "centered")
        draw_text(window, "3 - Cruel", FONT_SIZE, GAME_FONT, WIN_RES["w"]/2, WIN_RES["h"]/2 + 64, "WHITE", "centered")

# GAME SCENE ===================================================================

class GameScene(Scene):
    def __init__(self, difficulty=1):
        # SCENE DEFINES 
        self.g_diff = DIFFICULTIES[difficulty]
        self.score = 0
        self.score_multiplier = SCORE_MULTIPLIER[self.g_diff]
        self.win_offset = repeat((0,0)) 
        self.hp_pref = "PIE"
        self.gg_timer = pygame.time.get_ticks()
        self.gg_delay = 3000
        self.is_gg = False

        # PLAYER AND BULLET IMAGES - If you are reading this...uhh...good luck lol
        PLAYER_SPRITESHEET = load_img("player_sheet.png", IMG_DIR, SCALE)
        PLAYER_IMGS = {
            "SPAWNING": [
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,144,16,16]), True),
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,144,16,16]), True),
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,144,16,16]), True),
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,144,16,16]), True)
            ],
            "NORMAL": {
                "LV1": {
                    "FORWARD": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,0,16,16]), True)
                    ],
                    "LEFT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,16,16,16]), True)
                    ],
                    "RIGHT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,32,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,32,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,32,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,32,16,16]), True)
                    ]
                },
                "LV2": {
                    "FORWARD": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,48,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,48,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,48,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,48,16,16]), True)
                    ],
                    "LEFT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,64,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,64,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,64,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,64,16,16]), True)
                    ],
                    "RIGHT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,80,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,80,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,80,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,80,16,16]), True)
                    ]
                },
                "LV3": {
                    "FORWARD": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,96,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,96,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,96,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,96,16,16]), True)
                    ],
                    "LEFT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,112,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,112,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,112,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,112,16,16]), True)
                    ],
                    "RIGHT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,128,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,128,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,128,16,16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,128,16,16]), True)
                    ]
                }
            },
            "LEVELUP": {
                "1-2": [
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,160,16,16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,160,16,16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,160,16,16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,160,16,16]), True)
                ],
                "2-3": [
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0,176,16,16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16,176,16,16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32,176,16,16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48,176,16,16]), True)
                ]
            }
        }
        BULLET_SPRITESHEET = load_img("bullet_sheet.png", IMG_DIR, SCALE)
        BULLET_IMG = image_at(BULLET_SPRITESHEET, scale_rect(SCALE, [16,0,8,8]), True)

        # BG AND PARALLAX IMAGES & DEFINES 
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # HP Bar Image
        self.hp_surf = pygame.Surface((128,16))
        self.hpbar_outline = load_img("hpbar_outline.png", IMG_DIR, SCALE)
        self.hpbar_color = load_img("hpbar_color.png", IMG_DIR, SCALE)

        # HP Pie Image
        PIE_SHEET = load_img("hppie_sheet.png", IMG_DIR, SCALE) # It's not a sheet for hippies
        self.pie_surf = pygame.Surface((32,32))
        self.pie_health = image_at(PIE_SHEET, scale_rect(SCALE, [0,0,16,16]), True)
        self.pie_outline = image_at(PIE_SHEET, scale_rect(SCALE, [16,0,16,16]), True)
        self.pie_rect = self.pie_surf.get_rect()
        self.pie_rect.x = WIN_RES["w"] * 0.77
        self.pie_rect.y = 4

        # Difficulty icons
        DIFFICULTY_SPRITESHEET = load_img("difficulty_sheet.png", IMG_DIR, SCALE)
        self.DIFFICULTY_ICONS = {
            "EASY": {
                "EARLY": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [0,0,16,16]), True),
                "MID": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [16,0,16,16]), True),
                "LATE": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [32,0,16,16]), True)
            },
            "MEDIUM": {
                "EARLY": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [0,16,16,16]), True),
                "MID": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [16,16,16,16]), True),
                "LATE": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [32,16,16,16]), True)
            },
            "HARD": {
                "EARLY": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [0,32,16,16]), True),
                "MID": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [16,32,16,16]), True),
                "LATE": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [32,32,16,16]), True)
            }
        }
        self.difficulty_icon = pygame.Surface((32,32))

        # Clear the sprite groups
        all_sprites_g.empty()
        hostiles_g.empty()
        p_bullets_g.empty()
        powerups_g.empty()
        e_bullets_g.empty()
        sentries_g.empty()
        hellfighters_g.empty()

        # Initialize the player
        self.player = Player(PLAYER_IMGS, BULLET_IMG)
        all_sprites_g.add(self.player)

        # Create a spawner
        self.spawner = Spawner(self.player, self.g_diff)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(0))
                if event.key == pygame.K_l and DEBUG_MODE:
                    self.player.gun_level += 1

        self.spawner.handle_events(events)
    
    def update(self, dt):
        # Update parallax and background
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        
        # Handle collisions
        if not self.is_gg:
            # HOSTILES - PLAYER BULLET COLLISION
            for bullet in p_bullets_g:
                hits = pygame.sprite.spritecollide(bullet, hostiles_g, False, pygame.sprite.collide_circle)
                for hit in hits:
                    # Deduct enemy health
                    hit.health -= self.player.BULLET_DAMAGE

                    # Spawn small explosion
                    bullet_x = bullet.rect.centerx
                    bullet_y = bullet.rect.centery
                    bullet_pos = Vec2(bullet_x, bullet_y)
                    self.spawner.spawn_explosion(bullet_pos, "SMALL")

                    # Spawn explosion particles
                    self.spawner.spawn_exp_particles(
                        (hit.rect.centerx, hit.rect.centery),
                        (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                        3
                    )
                    
                    # Set boolean to True for flash effect
                    hit.is_hurt = True

                    # Kill bullet
                    bullet.kill()

                    # Logic if enemy is dead
                    if hit.health <= 0:
                        hit.kill()

                        # Add score
                        self.score += hit.WORTH * self.score_multiplier

                        # Spawn powerup
                        spawn_roll = random.randrange(1,100)
                        if spawn_roll <= POWERUP_ROLL_CHANCE[self.g_diff]:
                            self.spawner.spawn_powerup(hit.position)

                        # Spawn big explosion
                        bullet_x = hit.rect.centerx
                        bullet_y = hit.rect.centery
                        bullet_pos = Vec2(bullet_x, bullet_y)
                        self.spawner.spawn_explosion(bullet_pos, "BIG")

                        # Spawn explosion particles
                        self.spawner.spawn_exp_particles(
                            (hit.rect.centerx, hit.rect.centery),
                            (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                            30
                        )

                        # Generate screen shake
                        self.win_offset = shake(10,5)

            # PLAYER - ENEMY BULLET COLLISION
            hits = pygame.sprite.spritecollide(self.player, e_bullets_g, True, pygame.sprite.collide_circle)
            for hit in hits:
                # Damage player
                self.player.health -= hit.DAMAGE

                # Spawn small explosion
                bullet_x = hit.rect.centerx
                bullet_y = hit.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "SMALL")

                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (hit.rect.centerx, hit.rect.centery),
                    (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                    5
                )

                # Generate screen shake
                self.win_offset = shake(10,5)

                # Hurt player
                self.player.is_hurt = True

            # PLAYER - ENEMY COLLISION
            hits = pygame.sprite.spritecollide(self.player, hostiles_g, True, pygame.sprite.collide_circle)
            for hit in hits:
                self.player.health -= ENEMY_COLLISION_DAMAGE

                # Spawn big explosion on player
                bullet_x = self.player.rect.centerx
                bullet_y = self.player.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "BIG")

                # Spawn big explosion on hit
                bullet_x = hit.rect.centerx
                bullet_y = hit.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "BIG")

                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (hit.rect.centerx, hit.rect.centery),
                    EP_COLORS,
                    30
                )

                # Generate screen shake
                self.win_offset = shake(20,5)

                hit.kill()

            # PLAYER - POWERUP COLLISION
            hits = pygame.sprite.spritecollide(self.player, powerups_g, True)
            for hit in hits:
                particles_color = ((255,255,255)) # Default case
                if hit.POW_TYPE == "GUN":
                    if self.player.gun_level >= PLAYER_MAX_GUN_LEVEL:
                        self.player.gun_level = 3
                    else:
                        self.player.gun_level += 1
                    # Set particle colors
                    particles_color = GP_COLORS

                elif hit.POW_TYPE == "HEALTH":
                    self.player.health += POWERUP_HEALTH_AMOUNT[self.g_diff]
                    if self.player.health >= PLAYER_MAX_HEALTH:
                        self.player.health = PLAYER_MAX_HEALTH
                    # Set particle colors
                    particles_color = HP_COLORS
                        
                elif hit.POW_TYPE == "SCORE":
                    self.score += POWERUP_SCORE_BASE_WORTH * self.score_multiplier
                    # Set particle colors
                    particles_color = SCR_COLORS

                elif hit.POW_TYPE == "SENTRY":
                    self.spawner.spawn_sentry()
                    # Set particle colors
                    particles_color = SP_COLORS

                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (hit.rect.centerx, hit.rect.centery),
                    particles_color,
                    30
                )

            # SENTRY - ENEMY COLLISION
            for sentry in sentries_g:
                hits = pygame.sprite.spritecollide(sentry, hostiles_g, False, pygame.sprite.collide_circle)
                for hit in hits:
                    sentry.kill()
                    hit.kill()

                    # Spawn big explosion on sentry
                    bullet_x = sentry.rect.centerx
                    bullet_y = sentry.rect.centery
                    bullet_pos = Vec2(bullet_x, bullet_y)
                    self.spawner.spawn_explosion(bullet_pos, "BIG")

                    # Spawn big explosion on hit
                    bullet_x = hit.rect.centerx
                    bullet_y = hit.rect.centery
                    bullet_pos = Vec2(bullet_x, bullet_y)
                    self.spawner.spawn_explosion(bullet_pos, "BIG")

                    # Spawn explosion particles
                    self.spawner.spawn_exp_particles(
                        (hit.rect.centerx, hit.rect.centery),
                        (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                        30
                    )

            # SENTRY - ENEMY BULLET COLLISION
            for sentry in sentries_g:
                hits = pygame.sprite.spritecollide(sentry, e_bullets_g, True, pygame.sprite.collide_circle)
                for hit in hits:
                    # Deduct sentry health
                    sentry.health -= hit.DAMAGE

                    # Set boolean to True for flash effect
                    sentry.is_hurt = True

                    # Spawn small explosion
                    bullet_x = hit.rect.centerx
                    bullet_y = hit.rect.centery
                    bullet_pos = Vec2(bullet_x, bullet_y)
                    self.spawner.spawn_explosion(bullet_pos, "SMALL")

                    # Spawn explosion particles
                    self.spawner.spawn_exp_particles(
                        (hit.rect.centerx, hit.rect.centery),
                        (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                        5
                    )

                    if sentry.health <= 0:
                        # Spawn big explosion
                        bullet_x = sentry.rect.centerx
                        bullet_y = sentry.rect.centery
                        bullet_pos = Vec2(bullet_x, bullet_y)
                        self.spawner.spawn_explosion(bullet_pos, "BIG")

                        # Spawn explosion particles
                        self.spawner.spawn_exp_particles(
                            (sentry.rect.centerx, sentry.rect.centery),
                            (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                            30
                        )

                        sentry.kill()

        # END GAME IF PLAYER HAS LESS THAN 0 HEALTH
        if self.player.health <= 0 and not self.is_gg:
            # Spawn big explosion on player
            bullet_x = self.player.rect.centerx
            bullet_y = self.player.rect.centery
            bullet_pos = Vec2(bullet_x, bullet_y)
            self.spawner.spawn_explosion(bullet_pos, "BIG")

            # Spawn explosion particles
            self.spawner.spawn_exp_particles(
                (self.player.rect.centerx, self.player.rect.centery),
                (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                100
            )   

            # Generate screen shake
            self.win_offset = shake(30,5)

            # Set to game over
            self.player.kill()
            self.is_gg = True
            self.gg_timer = pygame.time.get_ticks()

        # Transition to game over scene
        if self.is_gg:
            now = pygame.time.get_ticks()
            if now - self.gg_timer > self.gg_delay:
                self.manager.go_to(GameOverScene(self.score))

        self.spawner.update(self.score)
        all_sprites_g.update(dt)

    def draw(self, window):
        # Draw background
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        # Draw sprites
        all_sprites_g.draw(window)

        # Draw score
        cur_score = str(int(self.score)).zfill(6)
        draw_text2(window, f"{cur_score}", GAME_FONT, int(FONT_SIZE*1.4), (12, 10), HP_RED2, italic=True)
        draw_text2(window, f"{cur_score}", GAME_FONT, int(FONT_SIZE*1.4), (12, 8), "WHITE", italic=True)

        # Draw hp bar
        if self.hp_pref == "SQUARE":
            # Draw square hp bar
            self.hp_surf.fill("BLACK")
            self.hp_surf.set_colorkey("BLACK")
            draw_hpbar(self.hp_surf, self.hpbar_color, (4,4,96,8), self.player.health, "WHITE")
            self.hp_surf.blit(self.hpbar_outline, (0,0))
            window.blit(self.hp_surf, 
                (
                    (window.get_width()/2) - 38,
                    10
                )
            )

        elif self.hp_pref == "PIE":
            # Draw pie hp bar
            semicirc_size = 32
            semicirc_start = 360 - (self.player.health * (360 / PLAYER_MAX_HEALTH))
            semicirc = Image.new("RGBA", (semicirc_size, semicirc_size))
            semicirc_d = ImageDraw.Draw(semicirc)
            semicirc_d.pieslice((0, 0, semicirc_size-1, semicirc_size-1), 1, semicirc_start + 1, fill="BLACK")
            semicirc_surf = pygame.image.fromstring(semicirc.tobytes(), semicirc.size, semicirc.mode)

            self.pie_surf.fill("BLACK")
            self.pie_surf.set_colorkey("BLACK")
            self.pie_surf.blit(self.pie_health, (0,0))
            self.pie_surf.blit(semicirc_surf, (0,0))
            self.pie_surf.blit(self.pie_outline, (0,0))
            window.blit(self.pie_surf, 
                (
                    window.get_width()/2,
                    4
                )
            )

        # Draw difficulty icon
        self.difficulty_icon = self.DIFFICULTY_ICONS[self.g_diff][self.spawner.current_stage]
        window.blit(self.difficulty_icon, (window.get_width() * 0.885,4))

        if self.is_gg:
            draw_text2(
                window, 
                "GAME OVER", 
                GAME_FONT, 
                int(FONT_SIZE*3), 
                (window.get_width()/2, window.get_height()/2), 
                "WHITE", 
                italic=True, 
                align="center"
            )

        # Debug mode stats
        if DEBUG_MODE:
            draw_text(window, f"{int(self.score)}", FONT_SIZE, GAME_FONT, 48, 8, "WHITE", "centered")
            draw_text(window, f"HP: {int(self.player.health)}", FONT_SIZE, GAME_FONT, 48, 16 + FONT_SIZE, "WHITE", "centered")
            draw_text(window, f"STAGE: {self.spawner.current_stage}", FONT_SIZE, GAME_FONT, 48, 32 + FONT_SIZE, "WHITE")
            draw_text(window, f"DIFF: {self.g_diff}", FONT_SIZE, GAME_FONT, 48, 64 + FONT_SIZE, "WHITE", )

        window.blit(window, next(self.win_offset))

# GAME OVER SCENE ================================================================

class GameOverScene(Scene):
    def __init__(self, score=0):
        # Scene variables
        self.score = score
        self.name = str()
        self.bckspace_timer = pygame.time.get_ticks()
        self.bckspace_delay = 200
        self.MAX_CHAR = 3

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Enter button
        self.enter_button = pygame.Surface((128,32))
        self.enter_button.fill("WHITE")

        # # Enter image
        # ENTER_SPRITESHEET = load_img("enter_sheet.png", IMG_DIR, SCALE)
        # self.ENTER_IMG = [
        #     image_at(ENTER_SPRITESHEET, scale_rect(SCALE, [0,0,32,16]), True),
        #     image_at(ENTER_SPRITESHEET, scale_rect(SCALE, [32,0,32,16]), True)
        # ]
        # self.frame_timer = pygame.time.get_ticks()
        # self.frame_delay = 400
        # self.current_frame = 0
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if str(event.unicode).isalpha() and len(self.name) < self.MAX_CHAR:
                    self.name += event.unicode
                elif event.key == pygame.K_RETURN and len(self.name) == self.MAX_CHAR:
                    self.manager.go_to(TitleScene())
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_BACKSPACE]:
            now = pygame.time.get_ticks()
            if now - self.bckspace_timer > self.bckspace_delay:
                self.bckspace_timer = now
                self.name = self.name[:-1]

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        # # Update frame of enter button
        # now = pygame.time.get_ticks()
        # if now - self.frame_timer > self.frame_delay:
        #     self.frame_timer = now
        #     self.current_frame = 1 - self.current_frame

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "GAME OVER!", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, f"{self.score}", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 128, "WHITE", "centered")
        
        if len(self.name) == 0:
            draw_text2(window, "ENTER NAME", GAME_FONT, int(FONT_SIZE*2), (WIN_RES["w"]/2, WIN_RES["h"]/2), "GRAY", align="center")
        else:
            draw_text2(window, f"{self.name.upper()}", GAME_FONT, int(FONT_SIZE*2), (WIN_RES["w"]/2, WIN_RES["h"]/2), "WHITE", align="center")
        
        if len(self.name) == self.MAX_CHAR:
            draw_text2(
                self.enter_button, 
                "ENTER", 
                GAME_FONT, 
                FONT_SIZE, 
                (self.enter_button.get_width()/2, (self.enter_button.get_height()/2) - FONT_SIZE / 2), 
                "BLACK", 
                align="center"
            )
            self.enter_button.set_colorkey("BLACK")
            window.blit(
                self.enter_button,
                (
                    window.get_width()/2 - self.enter_button.get_width()/2,
                    WIN_RES["h"]*0.7
                )
            )
        
        # if len(self.name) == self.MAX_CHAR:
        #     window.blit(self.ENTER_IMG[self.current_frame], (WIN_RES["w"]/2 - self.ENTER_IMG[self.current_frame].get_width()/2, WIN_RES["h"]*0.6))
            
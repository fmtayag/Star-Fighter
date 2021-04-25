import pygame, sys, random, math, pickle
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
from data.scripts.widgets import * 
from itertools import repeat

# TITLE SCENE ==================================================================

class TitleScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Images
        self.logo_img = load_img("logo_notilt.png", IMG_DIR, 4, convert_alpha=False)
        self.logo_rect = self.logo_img.get_rect()
        self.logo_hw = self.logo_rect.width / 2

        # Menu object
        self.title_menu = TitleMenuWidget(self.P_Prefs.title_selected)

        # Logo bob
        self.bob_timer = pygame.time.get_ticks()
        self.bob_m = 0

        self.exit = False # Dumb hack

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.title_menu.select_up()
                elif event.key == pygame.K_DOWN:
                    self.title_menu.select_down()
                elif event.key == pygame.K_z:
                    if self.title_menu.get_selected() == 0:
                        self.P_Prefs.title_selected = 0
                        self.manager.go_to(DifficultySelectionScene(self.P_Prefs))

                    elif self.title_menu.get_selected() == 1:
                        self.P_Prefs.title_selected = 1
                        self.manager.go_to(ScoresScene(self.P_Prefs))

                    elif self.title_menu.get_selected() == 2:
                        self.P_Prefs.title_selected = 2
                        self.manager.go_to(OptionsScene(self.P_Prefs))

                    elif self.title_menu.get_selected() == 3:
                        self.P_Prefs.title_selected = 3
                        self.manager.go_to(CreditsScene(self.P_Prefs))

                    elif self.title_menu.get_selected() == 4:
                        self.exit = True

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        self.title_menu.update()

    def draw(self, window):
        now = pygame.time.get_ticks()
        if now - self.bob_timer > 500:
            self.bob_timer = now 
            self.bob_m = 1 - self.bob_m

        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)
        window.blit(self.logo_img, (WIN_RES["w"]/2 - self.logo_hw, -64 + (2*self.bob_m)))

        # Draw menu
        self.title_menu.draw(window)
        #draw_text(window, "(Test Build v.Whatever)", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, 30, "WHITE", "centered")
        draw_text(window, "Game v1.1.0", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, window.get_rect().bottom-32, "WHITE", "centered")
        draw_text(window, "Pygame v2.0.1", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, window.get_rect().bottom-24, "WHITE", "centered")
        draw_text(window, "(c) 2020-2021 zyenapz", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, window.get_rect().bottom-16, "WHITE", "centered")
        draw_text(window, "All rights reserved.", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, window.get_rect().bottom-8, "WHITE", "centered")

# SCORES SCENE =================================================================

class ScoresScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences
        self.P_Prefs = P_Prefs

        # Load scores list
        self.scores_list = list()
        try:
            with open(SCORES_FILE, 'rb') as f:
                self.scores_list = pickle.load(f)
        except:
            pass

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Scores table
        self.scores_table = ScoresTableWidget(self.scores_list)

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
                        self.manager.go_to(TitleScene(self.P_Prefs))

                elif event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(self.P_Prefs))
    
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
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs
        
        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = OptionsSceneMenuWidget(self.P_Prefs.options_scene_selected)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.P_Prefs.options_scene_selected = 0
                    self.manager.go_to(TitleScene(self.P_Prefs))

                elif event.key == pygame.K_UP:
                    self.menu_widget.select_up()

                elif event.key == pygame.K_DOWN:
                    self.menu_widget.select_down()

                elif event.key == pygame.K_z:
                    if self.menu_widget.get_selected_str() == "VIDEO":
                        self.P_Prefs.options_scene_selected = 0
                        self.manager.go_to(VideoOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "SOUND":
                        self.P_Prefs.options_scene_selected = 1
                        self.manager.go_to(SoundOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "GAME":
                        self.P_Prefs.options_scene_selected = 2
                        self.manager.go_to(GameOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "CONTROLS":
                        self.P_Prefs.options_scene_selected = 3
                        self.manager.go_to(ControlsOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "BACK":
                        self.P_Prefs.options_scene_selected = 0
                        self.manager.go_to(TitleScene(self.P_Prefs))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "OPTIONS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        self.menu_widget.draw(window)

class VideoOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = VideoOptionsSceneMenuWidget(self.P_Prefs)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))
                if event.key == pygame.K_x:
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                # Testing
                if event.key == pygame.K_UP:
                    self.menu_widget.select_up()
                if event.key == pygame.K_DOWN:
                    self.menu_widget.select_down()
                if event.key == pygame.K_LEFT:
                    self.menu_widget.select_left()
                if event.key == pygame.K_RIGHT:
                    self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "VIDEO OPTIONS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        self.menu_widget.draw(window)

class SoundOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = SoundOptionsSceneMenuWidget(self.P_Prefs)

        # Key press delay
        self.press_timer = pygame.time.get_ticks()
        self.press_delay = 75

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))
                if event.key == pygame.K_x:
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                if event.key == pygame.K_UP:
                    self.menu_widget.select_up()
                if event.key == pygame.K_DOWN:
                    self.menu_widget.select_down()

        now = pygame.time.get_ticks()
        if now - self.press_timer > self.press_delay:
            self.press_timer = now

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.menu_widget.select_left()
            elif pressed[pygame.K_RIGHT]:
                self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "SOUND OPTIONS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        self.menu_widget.draw(window)

class GameOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = GameOptionsSceneMenuWidget(self.P_Prefs)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))
                if event.key == pygame.K_x:
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                # Testing
                if event.key == pygame.K_UP:
                    self.menu_widget.select_up()
                if event.key == pygame.K_DOWN:
                    self.menu_widget.select_down()
                if event.key == pygame.K_LEFT:
                    self.menu_widget.select_left()
                if event.key == pygame.K_RIGHT:
                    self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "GAME OPTIONS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        self.menu_widget.draw(window)

class ControlsOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = GameOptionsSceneMenuWidget()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))
                if event.key == pygame.K_x:
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                # Testing
                if event.key == pygame.K_UP:
                    self.menu_widget.select_up()
                if event.key == pygame.K_DOWN:
                    self.menu_widget.select_down()
                if event.key == pygame.K_LEFT:
                    self.menu_widget.select_left()
                if event.key == pygame.K_RIGHT:
                    self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "CONTROLS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        self.menu_widget.draw(window)

# CREDITS SCENE ================================================================

class CreditsScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Button
        self.back_button = pygame.Surface((128,32))
        self.back_button.fill("WHITE")

        # Devs' pictures
        DEVS_SHEET = load_img("devs_sheet.png", IMG_DIR, SCALE)
        self.zye_icon = image_at(DEVS_SHEET, scale_rect(SCALE, [0,0,16,16]), True)
        self.rio_icon = image_at(DEVS_SHEET, scale_rect(SCALE, [16,0,16,16]), True)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_z:
                    self.manager.go_to(TitleScene(self.P_Prefs))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "CREDITS", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        window.blit(self.zye_icon, (WIN_RES["w"]/2 - self.zye_icon.get_width()/2, WIN_RES["h"]*0.20))
        draw_text2(window, "zyenapz", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.270), "YELLOW", align="center")
        draw_text2(window, "code,art,sfx", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.300), "WHITE", align="center")

        window.blit(self.rio_icon, (WIN_RES["w"]/2 - self.rio_icon.get_width()/2, WIN_RES["h"]*0.350))
        draw_text2(window, "YoItsRion", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.430), "YELLOW", align="center")
        draw_text2(window, "music", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.460), "WHITE", align="center")

        draw_text2(window, "Special thanks", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.560), "WHITE", align="center")
        draw_text2(window, "@ooshkei,", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.600), "WHITE", align="center")
        draw_text2(window, "the pygame community,", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.630), "WHITE", align="center")
        draw_text2(window, "and you!", GAME_FONT, FONT_SIZE, (WIN_RES["w"]/2, WIN_RES["h"]*0.665), "WHITE", align="center")

        draw_text2(
            self.back_button, 
            "BACK", 
            GAME_FONT, 
            FONT_SIZE, 
            (self.back_button.get_width()/2 - FONT_SIZE, self.back_button.get_height()/2 - FONT_SIZE/2), 
            "BLACK", 
            align="center"
        )
        window.blit(self.back_button, (window.get_width()/2 - self.back_button.get_width()/2,window.get_rect().height*0.8))

# DIFFICULTY SELECTION SCENE ================================================================

class DifficultySelectionScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Difficulty Menu widget
        DEFAULT_SELECTED = 1
        self.w_diffmenu = DifficultyMenuWidget(DEFAULT_SELECTED)
        self.selected_diff = DEFAULT_SELECTED

        # Difficulty icons
        DIFFICULTY_SPRITESHEET = load_img("difficulty_sheet.png", IMG_DIR, SCALE*2)
        self.DIFFICULTY_ICONS = {
            0: image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE*2, [0,0,16,16]), True),
            1: image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE*2, [0,16,16,16]), True),
            2: image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE*2, [0,32,16,16]), True)
        }

        # # Description box
        # self.desc_surf = pygame.Surface((WIN_RES["w"]*0.75, 64))
        # self.desc_surf.fill("WHITE")
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.w_diffmenu.select_up()
                    self.selected_diff = self.w_diffmenu.get_selected()
                elif event.key == pygame.K_DOWN:
                    self.w_diffmenu.select_down()
                    self.selected_diff = self.w_diffmenu.get_selected()
                elif event.key == pygame.K_z:
                    if self.w_diffmenu.get_selected_str() != "BACK":
                        self.P_Prefs.game_difficulty = self.selected_diff
                        self.manager.go_to(GameScene(self.P_Prefs))
                    elif self.w_diffmenu.get_selected_str() == "BACK":
                        self.manager.go_to(TitleScene(self.P_Prefs))
                elif event.key == pygame.K_x:
                    self.manager.go_to(TitleScene(self.P_Prefs))
    
    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.w_diffmenu.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "SELECT DIFFICULTY", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        try:
            window.blit(
                self.DIFFICULTY_ICONS[self.selected_diff], 
                (window.get_width()/2 - self.DIFFICULTY_ICONS[self.selected_diff].get_width() / 2, window.get_height()*0.30)
            )
        except:
            pass
        self.w_diffmenu.draw(window)

# GAME SCENE ===================================================================

class GameScene(Scene):
    def __init__(self, P_Prefs):
        # Player Preferences
        self.P_Prefs = P_Prefs

        # SCENE DEFINES 
        self.g_diff = DIFFICULTIES[self.P_Prefs.game_difficulty]
        self.score = 0
        self.score_multiplier = SCORE_MULTIPLIER[self.g_diff]
        self.win_offset = repeat((0,0)) 
        self.hp_pref = HP_OPTIONS[self.P_Prefs.hp_pref]
        self.gg_timer = pygame.time.get_ticks()
        self.gg_delay = 3000
        self.is_gg = False
        self.can_pause = self.P_Prefs.can_pause
        self.paused = False

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

        # Sounds
        self.sfx_explosions = [
            load_sound("sfx_explosion1.wav", SFX_DIR, self.P_Prefs.sfx_vol),
            load_sound("sfx_explosion2.wav", SFX_DIR, self.P_Prefs.sfx_vol),
            load_sound("sfx_explosion3.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        ]
        self.sfx_hit = [
            load_sound("sfx_hit.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        ]
        self.sfx_shoot = load_sound("sfx_lasershoot.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        self.channel0 = pygame.mixer.Channel(0)
        self.channel1 = pygame.mixer.Channel(1)
        self.channel2 = pygame.mixer.Channel(2)

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

        # Exit progress bar
        self.exit_bar = pygame.Surface((32,32))
        self.exit_timer = pygame.time.get_ticks()
        self.exit_delay = 2000
        self.is_exiting = False
        self.timer_resetted = False

        # Killfeed
        self.scorefeed = Scorefeed()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l and DEBUG_MODE:
                    self.player.gun_level += 1

                if self.can_pause and not self.is_gg:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused # Dirty toggling hack
                    
                    if event.key == pygame.K_x and self.paused:
                        self.manager.go_to(TitleScene(self.P_Prefs))

        if not self.is_gg and not self.can_pause:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_x] or pressed[pygame.K_ESCAPE]:
                self.is_exiting = True
                if self.timer_resetted == False:
                    self.exit_timer = pygame.time.get_ticks()
                    self.timer_resetted = True
            else:
                self.is_exiting = False
                self.timer_resetted = False

        self.spawner.handle_events(events)
    
    def update(self, dt):
        if not self.paused:
            # Update parallax and background
            self.bg_y += BG_SPD * dt
            self.par_y += PAR_SPD * dt

            # Exit progress
            if self.is_exiting:
                now = pygame.time.get_ticks()
                if now - self.exit_timer > self.exit_delay:
                    self.player.health -= PLAYER_HEALTH * 999
                    self.win_offset = shake(30,5)
                    self.is_exiting = False
            
            # Collisions
            if not self.is_gg:
                self._handle_collisions()

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

            # Transition to game over scene if game is over
            if self.is_gg:
                now = pygame.time.get_ticks()
                if now - self.gg_timer > self.gg_delay:
                    self.P_Prefs.score = self.score
                    self.manager.go_to(GameOverScene(self.P_Prefs))

            self.spawner.update(self.score)
            self.scorefeed.update()
            all_sprites_g.update(dt)

    def draw(self, window):
        if not self.paused:
            # Draw background
            draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
            draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

            # Draw sprites
            all_sprites_g.draw(window)
            
            # Draw score feed
            self.scorefeed.draw(window)

            # Draw exit progress
            self._draw_exitprogress(window)

            # Draw score
            cur_score = str(int(self.score)).zfill(6)
            draw_text2(window, f"{cur_score}", GAME_FONT, int(FONT_SIZE*1.4), (12, 10), HP_RED2, italic=True)
            draw_text2(window, f"{cur_score}", GAME_FONT, int(FONT_SIZE*1.4), (12, 8), "WHITE", italic=True)
            
            # Draw hp bar
            self._draw_hpbar(window)

            # Draw difficulty icon
            self.difficulty_icon = self.DIFFICULTY_ICONS[self.g_diff][self.spawner.current_stage]
            window.blit(self.difficulty_icon, (window.get_width() * 0.885,4))

            if self.is_gg:
                draw_text2(
                    window, 
                    "GAME OVER", 
                    GAME_FONT, 
                    int(FONT_SIZE*3), 
                    (window.get_width()/2, window.get_height()*0.4), 
                    "WHITE", 
                    italic=True, 
                    align="center"
                )

            # Draw debug text
            self._draw_debugtext(window)
        else:
            self._draw_pausetext(window)

    def _handle_collisions(self):
        # Call collision functions
        self._hostile_player_collide()
        self._player_enemybullet_collide()
        self._player_enemy_collide()
        self._player_powerup_collide()
        self._player_enemy_collide()
        self._sentry_enemy_collide()
        self._sentry_enemybullet_collide()

    def _hostile_player_collide(self):
        # HOSTILES - PLAYER BULLET COLLISION
        for bullet in p_bullets_g:
            hits = pygame.sprite.spritecollide(bullet, hostiles_g, False, pygame.sprite.collide_circle)
            for hit in hits:
                # Play sound
                self.channel0.play(random.choice(self.sfx_hit))

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
                    # Play explosion sound
                    self.channel1.play(random.choice(self.sfx_explosions))

                    # Kill sprite
                    hit.kill()

                    # Add score
                    score_worth = hit.WORTH * self.score_multiplier
                    self.score += score_worth
                    self.scorefeed.add(score_worth)

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

    def _player_enemybullet_collide(self):
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

    def _player_enemy_collide(self):
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

    def _player_powerup_collide(self):
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
                # Add score
                p_score = POWERUP_SCORE_BASE_WORTH * self.score_multiplier
                self.score += p_score
                self.scorefeed.add(p_score)

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

            # Produce a flashing effect
            # The player is not really hurt, the variable is just named that way because I was stupid
            # enough not to foresee other uses...now im too lazy to change it.
            self.player.is_hurt = True

    def _sentry_enemy_collide(self):
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

    def _sentry_enemybullet_collide(self):
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

    def _draw_exitprogress(self, window): 
        if self.is_exiting:
            now = pygame.time.get_ticks()
            bar_length = int((now - self.exit_timer) / 8)
            bar_color = "WHITE"
            if now - self.exit_timer > self.exit_delay / 2:
                bar_color = HP_RED1
            self.exit_bar = pygame.Surface((bar_length,16))
            self.exit_bar.fill(bar_color)
            draw_text2(
                self.exit_bar,
                "EXITING",
                GAME_FONT,
                FONT_SIZE,
                (self.exit_bar.get_width()/2, 0),
                "BLACK",
                align="center"
            )
            window.blit(
                self.exit_bar,
                (window.get_width()/2 - self.exit_bar.get_width()/2, window.get_height()/2)
            )

    def _draw_hpbar(self, window):
        if self.hp_pref == HP_OPTIONS[1]:
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

        elif self.hp_pref == HP_OPTIONS[0]:
            # Draw circle hp bar
            semicirc_size = 32
            semicirc_end = 360 - (self.player.health * (360 / PLAYER_MAX_HEALTH)) + 270
            semicirc = Image.new("RGBA", (semicirc_size, semicirc_size))
            semicirc_d = ImageDraw.Draw(semicirc)
            semicirc_d.pieslice((0, 0, semicirc_size-1, semicirc_size-1), 271, semicirc_end + 1, fill="BLACK")
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

    def _draw_debugtext(self, window):
        # Debug mode stats
        if DEBUG_MODE:
            draw_text(window, f"{int(self.score)}", FONT_SIZE, GAME_FONT, 48, 8, "WHITE", "centered")
            draw_text(window, f"HP: {int(self.player.health)}", FONT_SIZE, GAME_FONT, 48, 16 + FONT_SIZE, "WHITE", "centered")
            draw_text(window, f"STAGE: {self.spawner.current_stage}", FONT_SIZE, GAME_FONT, 48, 32 + FONT_SIZE, "WHITE")
            draw_text(window, f"DIFF: {self.g_diff}", FONT_SIZE, GAME_FONT, 48, 64 + FONT_SIZE, "WHITE", )

        window.blit(window, next(self.win_offset))

    def _draw_pausetext(self, window):
        draw_text2(
            window, 
            "PAUSED", 
            GAME_FONT, 
            int(FONT_SIZE*3), 
            (window.get_width()/2, window.get_height()*0.4), 
            "WHITE", 
            italic=True, 
            align="center"
        )
        draw_text2(
            window, 
            "ESC to Resume", 
            GAME_FONT, 
            int(FONT_SIZE*2), 
            (window.get_width()/2, window.get_height()*0.5), 
            "WHITE", 
            italic=True, 
            align="center"
        )
        draw_text2(
            window, 
            "X to Exit", 
            GAME_FONT, 
            int(FONT_SIZE*2), 
            (window.get_width()/2, window.get_height()*0.55), 
            "WHITE", 
            italic=True, 
            align="center"
        )
# GAME OVER SCENE ================================================================

class GameOverScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences 
        self.P_Prefs = P_Prefs

        # Scene variables
        self.score = self.P_Prefs.score
        self.name = str()
        self.bckspace_timer = pygame.time.get_ticks()
        self.bckspace_delay = 200
        self.MAX_CHAR = 3
        self.score_comment = self._get_comment(self.score)
        self.difficulty = self.P_Prefs.game_difficulty

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

        # Ranks
        RANKS_SHEET = load_img("ranks_sheet.png", IMG_DIR, SCALE*2)
        self.RANKS_IMGS = {
            "RECRUIT": image_at(RANKS_SHEET, scale_rect(SCALE*2, [0,0,16,16]), True),
            "ENSIGN": image_at(RANKS_SHEET, scale_rect(SCALE*2, [16,0,16,16]), True),
            "LIEUTENANT": image_at(RANKS_SHEET, scale_rect(SCALE*2, [32,0,16,16]), True),
            "COMMANDER": image_at(RANKS_SHEET, scale_rect(SCALE*2, [48,0,16,16]), True),
            "CAPTAIN": image_at(RANKS_SHEET, scale_rect(SCALE*2, [64,0,16,16]), True),
            "ADMIRAL": image_at(RANKS_SHEET, scale_rect(SCALE*2, [80,0,16,16]), True)
        }
        self.rank = self.score_comment.upper()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if str(event.unicode).isalpha() and len(self.name) < self.MAX_CHAR:
                    self.name += event.unicode
                elif event.key == pygame.K_RETURN and len(self.name) == self.MAX_CHAR:
                    self._exit_scene()
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_BACKSPACE]:
            now = pygame.time.get_ticks()
            if now - self.bckspace_timer > self.bckspace_delay:
                self.bckspace_timer = now
                self.name = self.name[:-1]

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        # Draw game over and score
        draw_text(window, "GAME OVER!", FONT_SIZE*2, GAME_FONT, WIN_RES["w"]/2, 64, "WHITE", "centered")
        draw_text(window, f"{int(self.score)}", FONT_SIZE*4, GAME_FONT, WIN_RES["w"]/2, 104, HP_RED1, "centered")
        draw_text(window, f"{int(self.score)}", FONT_SIZE*4, GAME_FONT, WIN_RES["w"]/2, 100, "WHITE", "centered")

        # Draw rank and image
        #draw_text2(window, "Your Rank", GAME_FONT, int(FONT_SIZE*2), (WIN_RES["w"]/2, WIN_RES["h"]*0.35), "WHITE", align="center")
        try:
            window.blit(
                self.RANKS_IMGS[self.rank], 
                (window.get_width()/2 - self.RANKS_IMGS[self.rank].get_width()/2, window.get_height()*0.35)
            )
        except:
            pass
        draw_text2(window, f"Rank: {self.score_comment.capitalize()}", GAME_FONT, int(FONT_SIZE), (WIN_RES["w"]/2, WIN_RES["h"]*0.5), "WHITE", align="center")

        # if self.score_comment.upper() == "RECRUIT":
        #     draw_text2(window, f"You don't deserve symmetry", GAME_FONT, int(FONT_SIZE), (WIN_RES["w"]/2, WIN_RES["h"]*0.), "WHITE", align="center")

        # Draw  textbox
        if len(self.name) == 0:
            draw_text2(window, "ENTER NAME", GAME_FONT, int(FONT_SIZE*2), (WIN_RES["w"]/2, WIN_RES["h"]*0.645), "GRAY", align="center")
        else:
            draw_text2(window, f"> {self.name.upper()} <", GAME_FONT, int(FONT_SIZE*2), (WIN_RES["w"]/2, WIN_RES["h"]*0.645), "WHITE", align="center")
        
        # Draw enter button
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
                    WIN_RES["h"]*0.75
                )
            )

    def _exit_scene(self):
        # Load scores list
        scores_list = list()
        try:
            with open(SCORES_FILE, 'rb') as f:
                scores_list = pickle.load(f)
        except:
            pass

        # Save score data to file
        score_dat = (self.name, int(self.score), self.difficulty)
        scores_list.append(score_dat)
        with open(SCORES_FILE, 'wb') as f:
            pickle.dump(scores_list, f)

        # Go to title scene
        self.manager.go_to(TitleScene(self.P_Prefs))

    def _get_comment(self, score):
        if score < 0:
            return "bugged"
        elif score == 0:
            return "recruit"
        elif score < 1000:
            return "ensign"
        elif score >= 1000 and score < 3000:
            return "lieutenant"
        elif score >= 3000 and score < 6000:
            return "commander"
        elif score >= 6000 and score < 9000:
            return "captain"
        elif score >= 9000:
            return "admiral"
import pygame
from data.scripts.defines import * 
from data.scripts.muda import (
    draw_text2,
    draw_text,
    slice_list,
    load_sound
)

# Title Scene Widgets ==========================================================
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

# Scores Scene Widgets =========================================================

class ScoresControlWidget:
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

class ScoresTableWidget:
    def __init__(self, scores_list):
        # Font spacing
        self.spacing = FONT_SIZE / 2

        # Table
        self.table_surf = pygame.Surface((WIN_RES["w"], WIN_RES["h"] / 2))
        self.table_rect = self.table_surf.get_rect()

        # Scores list
        self.scores = sorted(scores_list,key=lambda x: x[1],reverse=True) # Sort by the SCORE column
        self.splice_n = 5
        self.scores = slice_list(self.scores, self.splice_n)
        self.cur_tbl = 0

    def update(self):
        pass

    def draw(self, window):
        self.table_surf.fill("black")
        self.table_surf.set_colorkey("black")
        # Draw labels
        if len(self.scores) != 0:
            draw_text(self.table_surf, "RANK", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.25, 0, "YELLOW")
            draw_text(self.table_surf, "NAME", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.60, 0, "YELLOW")
            draw_text(self.table_surf, "SCORE", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 1.05, 0, "YELLOW")
            draw_text(self.table_surf, "DIFF.", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 1.50, 0, "YELLOW")

        if len(self.scores) != 0:
            for i in range(len(self.scores[self.cur_tbl])):
                name = self.scores[self.cur_tbl][i][0].upper()
                score = self.scores[self.cur_tbl][i][1]
                difficulty = DIFFICULTIES_LORE[self.scores[self.cur_tbl][i][2]]

                # If difficulty is HARD, then set color to yellow
                difficulty_color = "WHITE"
                if difficulty == DIFFICULTIES_LORE[2]:
                    difficulty_color = "RED"

                # Draw text
                draw_text(self.table_surf, f"{(i+1)+(self.cur_tbl*self.splice_n)}.", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.25 + len(str(i)), FONT_SIZE*(i+1) + self.spacing*(i+1), "YELLOW")
                draw_text(self.table_surf, f"{name}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.60, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")
                draw_text(self.table_surf, f"{score}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 1.05, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")
                draw_text2(self.table_surf, f"{difficulty}", GAME_FONT, FONT_SIZE, (self.table_rect.centerx * 1.50, FONT_SIZE*(i+1) + self.spacing*(i+1)), difficulty_color)

                # Draw page text
                draw_text(window, f"PAGE {self.cur_tbl+1} OF {len(self.scores)}", FONT_SIZE, GAME_FONT, self.table_rect.centerx, self.table_rect.bottom * 1.25, "WHITE", "centered")
        else:
            draw_text2(self.table_surf, "No scores yet...", GAME_FONT, FONT_SIZE, (self.table_rect.centerx, 64), "WHITE", align="center")
            draw_text2(self.table_surf, "Go play the game!", GAME_FONT, FONT_SIZE, (self.table_rect.centerx, 96), "WHITE", align="center")

        window.blit(self.table_surf,(0,WIN_RES["h"]/2 - 128))

    def next_table(self):
        if self.cur_tbl < len(self.scores) - 1:
            self.cur_tbl += 1
        
    def prev_table(self):
        if self.cur_tbl > 0:
            self.cur_tbl -= 1

# Options Scenes Widgets =======================================================

class TextSelector:
    def __init__(self, init_value, options, position, alignment="LEFT", active=False):
        self.options = options
        self.alignment = alignment
        self.index = init_value
        self.ts_surf = pygame.Surface((64,32))
        self.position = position
        self.active = active

        # Arrow animations
        self.jut_m = 0 # Jut multiplier for the arrows
        self.jut_timer = pygame.time.get_ticks()
        self.jut_delay = 500

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.jut_timer > self.jut_delay:
            self.jut_timer = now
            self.jut_m = 1 - self.jut_m # Toggle between 0 and 1. Neat, huh?

    def draw(self, surface):
        # Automatically resize surface depending on text size
        text_length = len(self.options[self.index])
        surf_length = (text_length+2) * FONT_SIZE
        self.ts_surf = pygame.Surface((surf_length, 32))

        self.ts_surf.fill("BLACK")
        self.ts_surf.set_colorkey("BLACK")

        if self.active:
            # Draw the arrows. There has to be a better way to do this...
            # But it will work for now (narrator: it will work this way forever)
            draw_text2(
                self.ts_surf, 
                "<", 
                GAME_FONT, 
                FONT_SIZE, 
                (
                    FONT_SIZE/2 - (2*self.jut_m),
                    self.ts_surf.get_height()/2 - FONT_SIZE/2
                ),
                "WHITE"
            )
            draw_text2(
                self.ts_surf, 
                ">", 
                GAME_FONT, 
                FONT_SIZE, 
                (
                    self.ts_surf.get_width() - FONT_SIZE + (2*self.jut_m),
                    self.ts_surf.get_height()/2 - FONT_SIZE/2
                ),
                "WHITE"
            )

        # Draw text
        draw_text2(
            self.ts_surf, 
            self.options[self.index], 
            GAME_FONT, 
            FONT_SIZE, 
            (0,self.ts_surf.get_height()/2 - FONT_SIZE/2),
            "WHITE",
            align="center"
        )
        
        # Draw selector to surface
        if self.alignment == "CENTER":
            surface.blit(
                self.ts_surf, 
                (surface.get_width()/2 - self.ts_surf.get_width()/2 + self.position[0], self.position[1])
            )

    def go_left(self):
        if self.index <= 0:
            self.index = len(self.options)-1
        else:
            self.index -= 1

    def go_right(self):
        if self.index >= len(self.options)-1:
            self.index = 0
        else:
            self.index += 1

    def get_selected(self):
        return self.index

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

class RangeSelector:
    def __init__(self, init_value, minmax, position, alignment="LEFT", active=False):
        self.min_ = minmax[0]
        self.max_ = minmax[1]
        self.value = init_value
        self.alignment = alignment
        self.index = 0
        self.ts_surf = pygame.Surface((64,32))
        self.position = position
        self.active = active

        # Arrow animations
        self.jut_m = 0 # Jut multiplier for the arrows
        self.jut_timer = pygame.time.get_ticks()
        self.jut_delay = 500

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.jut_timer > self.jut_delay:
            self.jut_timer = now
            self.jut_m = 1 - self.jut_m # Toggle between 0 and 1. Neat, huh?

    def draw(self, surface):
        # Automatically resize surface depending on text size
        text_length = len(str(int(self.value)))
        surf_length = (text_length+2) * FONT_SIZE
        self.ts_surf = pygame.Surface((surf_length, 32))

        self.ts_surf.fill("BLACK")
        self.ts_surf.set_colorkey("BLACK")

        if self.active:
            # Draw the arrows.
            if self.value > 0:
                draw_text2(
                    self.ts_surf, 
                    "<", 
                    GAME_FONT, 
                    FONT_SIZE, 
                    (
                        FONT_SIZE/2 - (2*self.jut_m),
                        self.ts_surf.get_height()/2 - FONT_SIZE/2
                    ),
                    "WHITE"
                )

            if self.value < self.max_:
                draw_text2(
                    self.ts_surf, 
                    ">", 
                    GAME_FONT, 
                    FONT_SIZE, 
                    (
                        self.ts_surf.get_width() - FONT_SIZE + (2*self.jut_m),
                        self.ts_surf.get_height()/2 - FONT_SIZE/2
                    ),
                    "WHITE"
                )

        # Draw text
        draw_text2(
            self.ts_surf, 
            str(int(self.value)), 
            GAME_FONT, 
            FONT_SIZE, 
            (0,self.ts_surf.get_height()/2 - FONT_SIZE/2),
            "WHITE",
            align="center"
        )
        
        # Draw selector to surface
        if self.alignment == "CENTER":
            surface.blit(
                self.ts_surf, 
                (surface.get_width()/2 - self.ts_surf.get_width()/2 + self.position[0], self.position[1])
            )

    def decrease(self):
        if self.value <= self.min_:
            self.value = 0
        else:
            self.value -= 1 

    def increase(self):
        if self.value >= self.max_:
            self.value = self.max_
        else:
            self.value += 1

    def get_value(self):
        return self.value

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

class Button:
    def __init__(self, text, size, position):
        self.image = pygame.Surface(size)
        self.text = text 
        self.position = position
        self.active = False
        self.text_color = "WHITE"
        self.surface_color = "BLACK"

    def update(self):
        pass

    def draw(self, surface):
        self.image.fill(self.surface_color)
        self.image.set_colorkey("BLACK")

        # Draw text
        draw_text2(
            self.image,
            self.text,
            GAME_FONT,
            FONT_SIZE,
            (self.image.get_width()/2 , self.image.get_height()/2 - FONT_SIZE/2),
            self.text_color,
            align="center"
        )
        surface.blit(self.image, self.position)

    def activate(self):
        self.text_color = "BLACK"
        self.surface_color = "WHITE"
        self.active = True

    def deactivate(self):
        self.text_color = "WHITE"
        self.surface_color = "BLACK"
        self.active = False

class Textbox:
    def __init__(self, key_, size, position):
        self.image = pygame.Surface(size)
        self.key_ = key_
        if self.key_ == None:
            self.text = "UNDEFINED"
        else:
            self.text = pygame.key.name(self.key_).upper()
        self.position = position
        self.text_color = "WHITE"
        self.surface_color = "BLACK"

        self.active = False
        self.selected = False
        self.font_size = FONT_SIZE

    def update(self):
        pass

    def draw(self, surface):
        self.image.fill(self.surface_color)
        self.image.set_colorkey("BLACK")

        # Draw outline / change colors of image and text
        if self.active and not self.selected:
            pygame.draw.rect(self.image, "WHITE", ((0,0),self.image.get_size()), 4)
        elif self.active and self.selected:
            self.text_color = "BLACK"
            self.surface_color = "WHITE"

        # Draw text
        if self.key_ == None:
            self.text = "UNDEFINED"
            self.text_color = "RED"
        else:
            self.text = pygame.key.name(self.key_).upper()
        draw_text2(
            self.image,
            self.text,
            GAME_FONT,
            self.font_size,
            (self.image.get_width()/2 , self.image.get_height()/2 - self.font_size/2),
            self.text_color,
            align="center"
        )
        surface.blit(self.image, self.position)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False
        self.text_color = "WHITE"
        self.surface_color = "BLACK"

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def change_text(self, key_):
        self.key_ = key_
        self.text = pygame.key.name(self.key_).upper()
        if len(self.text) > 5:
            self.font_size = int(FONT_SIZE / 2)
        else:
            self.font_size = FONT_SIZE

class VideoOptionsSceneMenuWidget:
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs
        self.image = pygame.Surface((WIN_RES["w"], 350))
        x_alignment = self.image.get_width()*0.30
        btn_x_size = 128

        # Options
        self.ts_fullscreen_y = 16
        self.ts_frameless_y = 64
        self.ts_fullscreen = TextSelector(self.P_Prefs.is_fullscreen, YESNO_OPTIONS, (x_alignment,self.ts_fullscreen_y), alignment="CENTER", active=True)
        self.ts_frameless = TextSelector(self.P_Prefs.is_frameless, YESNO_OPTIONS, (x_alignment, self.ts_frameless_y), alignment="CENTER")
        self.btn_back = Button(
            "BACK", 
            (btn_x_size,32), 
            (self.image.get_width()/2 - btn_x_size/2,self.image.get_height()*0.7)
        )
        
        # Options list
        self.options = (
            self.ts_fullscreen,
            self.ts_frameless,
            self.btn_back # Note: Back buttons should always be put at the last index of an options list
        )
        self.MAX_OPTIONS = len(self.options) 
        self.index = 0
        
        # To display the disclaimer
        self.settings_changed = False

    def update(self):
        for option in self.options:
            option.update()

        # Update preferences
        self.P_Prefs.is_fullscreen = self.ts_fullscreen.get_selected()
        self.P_Prefs.is_frameless = self.ts_frameless.get_selected()

    def draw(self, window):
        self.image.fill("BLACK")
        self.image.set_colorkey("BLACK")

        # Draw Labels
        draw_text2(self.image, "FULLSCREEN", GAME_FONT, FONT_SIZE, (32, self.ts_fullscreen_y + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "FRAMELESS", GAME_FONT, FONT_SIZE, (32, self.ts_frameless_y + FONT_SIZE/2), "WHITE")

        # Draw text selectors
        for option in self.options:
            option.draw(self.image)

        # Draw disclaimer
        if self.settings_changed:
            draw_text2(self.image, "Please restart the game", GAME_FONT, FONT_SIZE, (32, self.image.get_height()*0.4), "WHITE", align="center")
            draw_text2(self.image, "to apply changes.", GAME_FONT, FONT_SIZE, (32, self.image.get_height()*0.45), "WHITE", align="center")

        # Draw the widget to the screen
        window.blit(self.image, (0,window.get_height()*0.3))

    def select_up(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        # Move current text selector 
        if self.index <= 0:
            self.index = self.MAX_OPTIONS - 1
        else:
            self.index -= 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_down(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        # Move current text selector 
        if self.index >= self.MAX_OPTIONS - 1:
            self.index = 0
        else:
            self.index += 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_left(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == TextSelector:
            selected_option.go_left()

        if not self.settings_changed:
            self.settings_changed = True

    def select_right(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == TextSelector:
            selected_option.go_right()

        if not self.settings_changed:
            self.settings_changed = True

    def get_selected(self):
        return self.index

    def get_max_index(self):
        return self.MAX_OPTIONS - 1

class SoundOptionsSceneMenuWidget:
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs
        self.image = pygame.Surface((WIN_RES["w"], 350))
        x_alignment = self.image.get_width()*0.30
        btn_x_size = 128

        # Options
        self.rs_sfx_y = 16
        self.rs_ost_y = 64
        self.rs_sfx = RangeSelector(self.P_Prefs.sfx_vol * 100, SFX_RANGE, (x_alignment,self.rs_sfx_y), alignment="CENTER", active=True)
        self.rs_ost = RangeSelector(self.P_Prefs.music_vol * 100, MUSIC_RANGE, (x_alignment, self.rs_ost_y), alignment="CENTER")
        self.btn_back = Button(
            "BACK", 
            (btn_x_size,32), 
            (self.image.get_width()/2 - btn_x_size/2,self.image.get_height()*0.7)
        )
        
        # Options list
        self.options = (
            self.rs_sfx,
            self.rs_ost,
            self.btn_back # Note: Back buttons should always be put at the last index of an options list
        )
        self.MAX_OPTIONS = len(self.options) 
        self.index = 0

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def update(self):
        for option in self.options:
            option.update()

        # Update preferences
        self.P_Prefs.sfx_vol = self.rs_sfx.get_value() / 100
        self.P_Prefs.music_vol = self.rs_ost.get_value() / 100

        # Update sound volumes
        self.sfx_keypress.set_volume(self.P_Prefs.sfx_vol)

        pygame.mixer.music.set_volume(self.P_Prefs.music_vol)

    def draw(self, window):
        self.image.fill("BLACK")
        self.image.set_colorkey("BLACK")

        # Draw Labels
        draw_text2(self.image, "SFX", GAME_FONT, FONT_SIZE, (32, self.rs_sfx_y + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "MUSIC", GAME_FONT, FONT_SIZE, (32, self.rs_ost_y + FONT_SIZE/2), "WHITE")

        # Draw text selectors
        for option in self.options:
            option.draw(self.image)

        # Draw the widget to the screen
        window.blit(self.image, (0,window.get_height()*0.3))

    def select_up(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        # Move current text selector 
        if self.index <= 0:
            self.index = self.MAX_OPTIONS - 1
        else:
            self.index -= 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_down(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        # Move current text selector 
        if self.index >= self.MAX_OPTIONS - 1:
            self.index = 0
        else:
            self.index += 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_left(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == RangeSelector:
            # Play sound
            if selected_option.get_value() > selected_option.min_:
                self.sfx_keypress.play()

            # Decrease value 
            selected_option.decrease()

    def select_right(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == RangeSelector:
            # Play sound
            if selected_option.get_value() > selected_option.min_:
                self.sfx_keypress.play()
                
            selected_option.increase()

    def get_selected(self):
        return self.index

    def get_max_index(self):
        return self.MAX_OPTIONS - 1

class GameOptionsSceneMenuWidget:
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        self.image = pygame.Surface((WIN_RES["w"], 350))
        x_alignment = self.image.get_width()*0.30
        btn_x_size = 128

        # Options
        self.ts_hp_y = 16
        self.ts_canpause_y = 64
        self.ts_hp = TextSelector(self.P_Prefs.hp_pref, HP_OPTIONS, (x_alignment,self.ts_hp_y), alignment="CENTER", active=True)
        self.ts_canpause = TextSelector(self.P_Prefs.can_pause, YESNO_OPTIONS, (x_alignment, self.ts_canpause_y), alignment="CENTER")
        self.btn_back = Button(
            "BACK", 
            (btn_x_size,32), 
            (self.image.get_width()/2 - btn_x_size/2,self.image.get_height()*0.7)
        )
        
        # Options list
        self.options = (
            self.ts_hp,
            self.ts_canpause,
            self.btn_back # Note: Back buttons should always be put at the last index of an options list
        )
        self.MAX_OPTIONS = len(self.options) 
        self.index = 0

    def update(self):
        for option in self.options:
            option.update()

        # Update preferences
        self.P_Prefs.hp_pref = self.ts_hp.get_selected()
        self.P_Prefs.can_pause = self.ts_canpause.get_selected()

    def draw(self, window):
        self.image.fill("BLACK")
        self.image.set_colorkey("BLACK")

        # Draw Labels
        draw_text2(self.image, "HP BAR STYLE", GAME_FONT, FONT_SIZE, (32, self.ts_hp_y + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "CAN PAUSE", GAME_FONT, FONT_SIZE, (32, self.ts_canpause_y + FONT_SIZE/2), "WHITE")

        # Draw text selectors
        for option in self.options:
            option.draw(self.image)

        # Draw the widget to the screen
        window.blit(self.image, (0,window.get_height()*0.3))

    def select_up(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        # Move current text selector 
        if self.index <= 0:
            self.index = self.MAX_OPTIONS - 1
        else:
            self.index -= 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_down(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        # Move current text selector 
        if self.index >= self.MAX_OPTIONS - 1:
            self.index = 0
        else:
            self.index += 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_left(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == TextSelector:
            selected_option.go_left()

    def select_right(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == TextSelector:
            selected_option.go_right()

    def get_selected(self):
        return self.index

    def get_max_index(self):
        return self.MAX_OPTIONS - 1

class ControlsOptionsSceneMenuWidget:
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs
        self.is_changingkey = False
        
        # Menu surface
        self.image = pygame.Surface((WIN_RES["w"], 350))
        x_alignment = self.image.get_width()*0.6
        btn_x_size = 128

        # Initialize textboxes
        self.txtbox_up = Textbox(self.P_Prefs.key_up, (108,24), (x_alignment,0))
        self.txtbox_down = Textbox(self.P_Prefs.key_down, (108,24), (x_alignment,32))
        self.txtbox_left = Textbox(self.P_Prefs.key_left, (108,24), (x_alignment,64))
        self.txtbox_right = Textbox(self.P_Prefs.key_right, (108,24), (x_alignment,96))
        self.txtbox_fire = Textbox(self.P_Prefs.key_fire, (108,24), (x_alignment,128))
        self.txtbox_exit = Textbox(self.P_Prefs.key_back, (108,24), (x_alignment,160))
        self.btn_back = Button(
            "APPLY & EXIT", 
            (btn_x_size,32), 
            (self.image.get_width()/2 - btn_x_size/2,self.image.get_height()*0.7)
        )
        self.options = (
            self.txtbox_up,
            self.txtbox_down,
            self.txtbox_left,
            self.txtbox_right,
            self.txtbox_fire,
            self.txtbox_exit,
            self.btn_back
        )
        self.options[0].activate()
        self.MAX_OPTIONS = len(self.options)
        self.index = 0

        self.has_undefined = False

    def update(self):
        pass

    def draw(self, window):
        self.image.fill("BLACK")
        self.image.set_colorkey("BLACK")

        # Draw labels
        draw_text2(self.image, "FORWARD", GAME_FONT, FONT_SIZE, (32, 0 + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "BACKWARD", GAME_FONT, FONT_SIZE, (32, 32 + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "LEFT", GAME_FONT, FONT_SIZE, (32, 64 + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "RIGHT", GAME_FONT, FONT_SIZE, (32, 96 + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "SHOOT/ENTER", GAME_FONT, FONT_SIZE, (32, 128 + FONT_SIZE/2), "WHITE")
        draw_text2(self.image, "EXIT/BACK", GAME_FONT, FONT_SIZE, (32, 160 + FONT_SIZE/2), "WHITE")

        # Draw textboxes
        for option in self.options:
            option.draw(self.image)

        # Draw disclaimer if there are duplicate keys
        self.has_undefined = False
        for option in self.options:
            if type(option) == Textbox:
                if option.key_ == None:
                    draw_text2(
                        self.image, 
                        "Has undefined keys.", 
                        GAME_FONT, 
                        FONT_SIZE, 
                        (self.image.get_width()/2 - FONT_SIZE/2, self.image.get_height()*0.55), 
                        "WHITE",
                        align="center"
                    )
                    draw_text2(
                        self.image, 
                        "Settings will not be saved.", 
                        GAME_FONT, 
                        FONT_SIZE, 
                        (self.image.get_width()/2 - FONT_SIZE/2, self.image.get_height()*0.6), 
                        "WHITE",
                        align="center"
                    )
                    self.has_undefined = True

        window.blit(self.image, (0,window.get_height()*0.3))
    
    def save_prefs(self):
        if not self.has_undefined:
            self.P_Prefs.key_up = self.txtbox_up.key_
            self.P_Prefs.key_down = self.txtbox_down.key_
            self.P_Prefs.key_left = self.txtbox_left.key_
            self.P_Prefs.key_right = self.txtbox_right.key_
            self.P_Prefs.key_fire = self.txtbox_fire.key_
            self.P_Prefs.key_back = self.txtbox_exit.key_

    def change_key(self, key_):
        if type(self.options[self.index]) == Textbox:
            # Duplicate check
            has_duplicate = False
            loc = 0
            for option in self.options:
                if type(option) == Textbox:
                    if option.key_ == key_:
                        has_duplicate = True
                        loc = self.options.index(option)
                        break
                    else:
                        continue

            if has_duplicate:
                self.options[loc].key_ = None
            else:
                self.options[self.index].change_text(key_)

    def highlight(self):
        if type(self.options[self.index]) == Textbox:
            self.options[self.index].select()
            self.is_changingkey = True

    def unhighlight(self):
        if type(self.options[self.index]) == Textbox:
            self.options[self.index].deselect()
            self.is_changingkey = False

    def select_up(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        self.unhighlight()

        # Move current text selector 
        if self.index <= 0:
            self.index = self.MAX_OPTIONS - 1
        else:
            self.index -= 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_down(self):
        # Deactivate current text selector
        selected_option = self.options[self.index]
        selected_option.deactivate()

        self.unhighlight()

        # Move current text selector 
        if self.index >= self.MAX_OPTIONS - 1:
            self.index = 0
        else:
            self.index += 1

        # Activate current text selector
        selected_option = self.options[self.index]
        selected_option.activate()

    def select_left(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == TextSelector:
            selected_option.go_left()

    def select_right(self):
        selected_option = self.options[self.index]
        option_type = type(selected_option)
        if option_type == TextSelector:
            selected_option.go_right()

    def get_selected(self):
        return self.index

    def get_max_index(self):
        return self.MAX_OPTIONS - 1

class OptionsSceneMenuWidget:
    def __init__(self, init_selected=0):
        # Surface
        # Warning - options may go beyond the surface and will be not rendered
        self.surface = pygame.Surface((WIN_RES["w"], 350))
        self.surf_rect = self.surface.get_rect()
        
        self.spacing = FONT_SIZE 

        # Menu
        self.options = ("VIDEO", "SOUND", "GAME", "CONTROLS", "BACK")
        self.act_opt = [0 for i in range(len(self.options))] # Active options
        self.act_opt[init_selected] = 1
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive menu

        # Selector
        self.selector = pygame.Surface((WIN_RES["w"], FONT_SIZE + 4))
        self.selector.fill("white")
        self.sel_y = FONT_SIZE + self.spacing
        self.sel_i = init_selected # index

        # Back button
        self.back_button = pygame.Surface((128,32))

    def update(self):
        self.sel_y = FONT_SIZE*(self.sel_i+1) + self.spacing*(self.sel_i+1)

    def draw(self, window):
        self.back_button.fill("BLACK")
        self.back_button.set_colorkey("BLACK")
        self.surface.fill("black")
        self.surface.set_colorkey("black")

        # Change selector size and draw
        if self.options[self.sel_i] != "BACK":
            self.selector = pygame.Surface((WIN_RES["w"], FONT_SIZE + 4))
            self.selector.fill("white")
            self.surface.blit(self.selector, (0,self.sel_y-3))
        else:
            self.selector = pygame.Surface((128,32))
            self.selector.fill("white")
            self.back_button.blit(
                self.selector, 
                (0,0)
            )

        # Draw menu
        for i in range(len(self.options)):
            if self.options[i] != "BACK":
                draw_text(self.surface, self.options[i], FONT_SIZE, GAME_FONT, self.surf_rect.centerx, FONT_SIZE*(i+1) + self.spacing*(i+1), self.colors[self.act_opt[i]], "centered")
            else:
                draw_text2(
                    self.back_button, 
                    "BACK", 
                    GAME_FONT, 
                    FONT_SIZE, 
                    (self.back_button.get_width()/2, self.back_button.get_height()/2 - FONT_SIZE/2), 
                    self.colors[self.act_opt[i]], 
                    align="center"
                )
                window.blit(
                    self.back_button, 
                    (window.get_width()/2 - self.back_button.get_width()/2, window.get_height()*0.8)
                )

        # Draw the menu widget surface
        window.blit(self.surface, (0,window.get_height()*0.3))

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

    def get_selected_str(self):
        return self.options[self.sel_i]

# Difficulty Scene Widgets =====================================================

class DifficultyMenuWidget:
    def __init__(self, init_selected):
        # Surface
        # Warning - options may go beyond the surface and will be not rendered
        self.surface = pygame.Surface((WIN_RES["w"], 350))
        self.surf_rect = self.surface.get_rect()
        
        self.spacing = FONT_SIZE 

        # Menu
        self.options = ("LENIENT", "FAIR", "CRUEL", "BACK")
        self.act_opt = [0 for i in range(len(self.options))] # Active options
        self.act_opt[init_selected] = 1
        self.colors = {0: "white", 1: "black"} # Colors for active/inactive menu

        # Selector
        self.selector = pygame.Surface((WIN_RES["w"], FONT_SIZE + 4))
        self.selector.fill("white")
        self.sel_y = FONT_SIZE + self.spacing
        self.sel_i = init_selected # index

        # Back button
        self.back_button = pygame.Surface((128,32))

    def update(self):
        self.sel_y = FONT_SIZE*(self.sel_i+1) + self.spacing*(self.sel_i+1)

    def draw(self, window):
        self.back_button.fill("BLACK")
        self.back_button.set_colorkey("BLACK")
        self.surface.fill("black")
        self.surface.set_colorkey("black")

        # Change selector size and draw
        if self.options[self.sel_i] != "BACK":
            self.selector = pygame.Surface((WIN_RES["w"], FONT_SIZE + 4))
            self.selector.fill("white")
            self.surface.blit(self.selector, (0,self.sel_y-3))
        else:
            self.selector = pygame.Surface((128,32))
            self.selector.fill("white")
            self.back_button.blit(
                self.selector, 
                (0,0)
            )

        # Draw menu
        for i in range(len(self.options)):
            if self.options[i] != "BACK":
                draw_text(self.surface, self.options[i], FONT_SIZE, GAME_FONT, self.surf_rect.centerx, FONT_SIZE*(i+1) + self.spacing*(i+1), self.colors[self.act_opt[i]], "centered")
            else:
                draw_text2(
                    self.back_button, 
                    "BACK", 
                    GAME_FONT, 
                    FONT_SIZE, 
                    (self.back_button.get_width()/2, self.back_button.get_height()/2 - FONT_SIZE/2), 
                    self.colors[self.act_opt[i]], 
                    align="center"
                )
                window.blit(
                    self.back_button, 
                    (window.get_width()/2 - self.back_button.get_width()/2, window.get_height()*0.8)
                )

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

    def get_selected_str(self):
        return self.options[self.sel_i]

# Scores Scene Widgets =========================================================
class Scorefeed():
    def __init__(self):
        self.feed = list()
        self.MAX_SIZE = 3

        # Surface
        self.feed_surf = pygame.Surface((96,128))

        # Delete timer
        self.delete_timer = pygame.time.get_ticks()
        self.delete_delay = 2000
        self.is_empty = False

    def update(self):
        if len(self.feed) > 0:
            self.is_empty = False
        else:
            self.is_empty = True

        if not self.is_empty:
            now = pygame.time.get_ticks()
            if now - self.delete_timer > self.delete_delay:
                self.delete_timer = now

                if len(self.feed) > 0:
                    self.feed.pop()
        else:
            self.delete_timer = pygame.time.get_ticks()

    def draw(self, window):
        self.feed_surf.fill("BLACK")
        self.feed_surf.set_colorkey("BLACK")
        for i in range(len(self.feed)):
            draw_text2(
                self.feed_surf, 
                f"+{int(self.feed[i])} pts", 
                GAME_FONT, FONT_SIZE, 
                (4, FONT_SIZE*(i)),
                "WHITE"
            )
        window.blit(self.feed_surf, (8,32))

    def add(self, item):
        if len(self.feed) >= self.MAX_SIZE:
            self.feed.pop()
            self.feed.insert(0, item)
        else:
            self.feed.insert(0, item)

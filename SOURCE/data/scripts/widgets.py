import pygame
from data.scripts.defines import * 
from data.scripts.muda import (
    draw_text2,
    draw_text,
    slice_list
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
            ("ZYE", "231", "HARD")
        ]
        self.splice_n = 5
        self.scores = slice_list(self.scores, self.splice_n)
        self.cur_tbl = 0

    def update(self):
        pass

    def draw(self, window):
        self.table_surf.fill("black")
        self.table_surf.set_colorkey("black")

        if len(self.scores) != 0:
            for i in range(len(self.scores[self.cur_tbl])):
                draw_text(self.table_surf, f"{(i+1)+(self.cur_tbl*self.splice_n)}.", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.35 + len(str(i)), FONT_SIZE*(i+1) + self.spacing*(i+1), "YELLOW")
                draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][0]}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 0.6, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")
                draw_text(self.table_surf, f"{self.scores[self.cur_tbl][i][1]}", FONT_SIZE, GAME_FONT, self.table_rect.centerx * 1.0, FONT_SIZE*(i+1) + self.spacing*(i+1), "WHITE")
                draw_text2(self.table_surf, f"{self.scores[self.cur_tbl][i][2]}", GAME_FONT, FONT_SIZE, (self.table_rect.centerx * 1.4, FONT_SIZE*(i+1) + self.spacing*(i+1)), "WHITE")
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
    def __init__(self, options, position, alignment="LEFT", active=False):
        self.options = options
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
        # elif self.alignment == "LEFT":
        #     surface.blit(
        #         self.ts_surf, 
        #         (self.position[0], self.position[1])
        #     )
        # elif self.alignment == "RIGHT":
        #     surface.blit(
        #         self.ts_surf, 
        #         (surface.get_width() - self.ts_surf.get_width() - self.position[0], self.position[1])
        #     )

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

class GameOptionsSceneMenuWidget:
    def __init__(self):
        self.image = pygame.Surface((WIN_RES["w"], 350))
        x_alignment = self.image.get_width()*0.30
        btn_x_size = 128

        # Options
        self.ts_hp_y = 16
        self.ts_canpause_y = 64
        self.ts_hp = TextSelector(HP_OPTIONS, (x_alignment,self.ts_hp_y), alignment="CENTER", active=True)
        self.ts_canpause = TextSelector(YESNO_OPTIONS, (x_alignment, self.ts_canpause_y), alignment="CENTER")
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

class OptionsMenuWidget:
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

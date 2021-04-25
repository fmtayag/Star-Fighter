# Star Fighter
# An arcade shoot 'em up (shmup) set in outer space.
# Version: 2.0.0
#   > Release date: March 30th 2021
# Written in: Python, pygame 2.0.0
# Author: zyenapz
#   > Email: zyenapz@gmail.com
#   > Website: zyenapz.github.io
#   > GitHub: github.com/zyenapz
#   > Twitter: @zyenapz

import pygame, os, random, math, time, pickle
from pygame.locals import *
from pygame._sdl2.video import Window
from data.scripts.scenes import *
from data.scripts.defines import FPS, WIN_RES, TITLE
from data.scripts.muda import (
    load_img, 
    load_sound, 
    read_savedata,
    write_savedata,
    SceneManager
)
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
pygame.mixer.init()

# Player Preferences class =====================================================
class PlayerPrefs:
    def __init__(self):
        self.is_fullscreen = False
        self.is_frameless = True
        self.music_vol = 0.15
        self.sfx_vol = 0.30
        self.game_difficulty = 0
        self.hp_pref = 0
        self.can_pause = False

        self.score = 0
        self.title_selected = 0
        self.options_scene_selected = 0

# Game loop ====================================================================

def main():
    # Load / create PlayerPrefs object
    P_Prefs = None
    try:
        with open(USERDAT_FILE, 'rb') as f:
            P_Prefs = pickle.load(f)

            # Reset these variables
            P_Prefs.title_selected = 0
            P_Prefs.options_scene_selected = 0
    except:
        P_Prefs = PlayerPrefs()

    # Play music
    pygame.mixer.music.load("data/sfx/ost_fighter.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(P_Prefs.music_vol)

    # Initialize the window
    window = None
    if P_Prefs.is_fullscreen:
        window = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), FULLSCREEN, NOFRAME)
    else:
        window = pygame.display.set_mode((int(WIN_RES["w"]), int(WIN_RES["h"])), NOFRAME)

    # Create a scene manager
    manager = SceneManager(TitleScene(P_Prefs))

    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(load_img("icon.png", IMG_DIR, 1))
    pygame.mouse.set_visible(False)

    # Create Render target
    render_target = pygame.Surface((WIN_RES["w"], WIN_RES["h"]))

    # Loop variables
    clock = pygame.time.Clock()
    running = True
    prev_time = time.time()
    dt = 0

    while running:
        # Lock FPS
        clock.tick(FPS)
        pygame.display.set_caption(f"{TITLE} (FPS: {round(clock.get_fps(),2)})")

        # Calculate delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        if pygame.event.get(QUIT) or (type(manager.scene) == TitleScene and manager.scene.exit): # TODO - This is a dumb hack but it will work for now.
            # Save player preferences
            try:
                with open(USERDAT_FILE, 'wb') as f:
                    pickle.dump(P_Prefs, f)
            except:
                print("ERROR: Failed to save.")
            
            # Exit loop and function
            running = False
            return

            
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update(dt)
        manager.scene.draw(render_target)   

        # Draw screen

        if P_Prefs.is_fullscreen:
            xscale = window.get_rect().width / WIN_RES["w"]
            yscale = window.get_rect().height / WIN_RES["h"]
            if xscale < 1 and yscale < 1:
                scale = max(xscale, yscale)
            elif xscale > 1 and yscale > 1:
                scale = min(xscale, yscale)
            else:
                scale = 1.0
            #print(xscale, yscale)
            targetx = int(WIN_RES["w"] * xscale)
            targety = int(WIN_RES["h"] * yscale)

            window.fill("BLACK")
            window.blit(pygame.transform.scale(render_target, (round(WIN_RES["w"]*2.25), targety)), (window.get_rect().width / 2 - WIN_RES["w"]*1.125, 0))
            
        else:
            window.blit(pygame.transform.scale(render_target,(window.get_width(), window.get_height())),(0,0))

        pygame.display.flip()

if __name__ == "__main__":
    # Run main
    main()

    # Quit pygame
    pygame.quit()
# Star Fighter
# Version: 2.0.0
#   > Release date: March 30th 2021
# A space shoot 'em up (shmup) made in the style of old arcade games.
# Written in: Python, pygame 2.0.0
# Author: zyenapz
#   > Email: zyenapz@gmail.com
#   > Website: zyenapz.github.io
#   > GitHub: github.com/zyenapz
#   > Twitter: @zyenapz

# Import libraries =============================================================
import pygame, os, random, math, time
from pygame.locals import *
from itertools import repeat
from data.scripts.settings import *
from data.scripts.scenes import *
from data.scripts.MUDA import (
    load_img, 
    load_sound, 
    read_savedata,
    write_savedata,
    SceneManager
)

# Initialize pygame ============================================================

pygame.init()

# Game loop ====================================================================

def main():

    # Initialize the window
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    #window = pygame.display.set_mode((int(WIN_RES["w"]*2), int(WIN_RES["h"]*2)))
    window = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
    window_rect = window.get_rect()
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(load_img("player.png", IMG_DIR, 1)) # TODO - change the icon name
    pygame.mouse.set_visible(False)

    # Render target
    render_target = pygame.Surface((WIN_RES["w"], WIN_RES["h"]))

    # Scene Manager
    manager = SceneManager(GameScene())

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

        if pygame.event.get(QUIT):
            running = False

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update(dt)
        manager.scene.draw(render_target)   

        # TODO - render target for multiple resolutions

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

        window.fill((15,15,30))
        window.blit(pygame.transform.scale(render_target, (round(WIN_RES["w"]*2.25), targety)), (window.get_rect().width / 2 - WIN_RES["w"]*1.125, 0))
        #window.blit(pygame.transform.scale(render_target,(window.get_width(), window.get_height())),(0,0))

        pygame.display.flip()

# Run main
main()

# Quit pygame
pygame.quit()
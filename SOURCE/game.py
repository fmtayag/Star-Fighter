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
            write_savedata
        )
except Exception as e:
    print(e)
    exit()

# Initialize pygame ============================================================
pygame.init()
pygame.mouse.set_visible(False) # Hide the mouse

# Program variables ============================================================
WIN_RES = {"w": 640, "h": 676}
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
clock = pygame.time.Clock()
FPS = 60
spawn_delay = 2000
# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
FONT_DIR = os.path.join(DATA_DIR, "font")
game_font = os.path.join(FONT_DIR, "prstartk.ttf")
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

# Initialize the window ========================================================
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode((WIN_RES["w"], WIN_RES["h"]))
window_rect = window.get_rect()
pygame.display.set_caption(TITLE)

# Images =======================================================================

window_icon = load_img("hellfighter1.png", IMG_DIR, 1)
pygame.display.set_icon(window_icon)

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

logo_img = load_img("logo.png", IMG_DIR, 8, convert_alpha=True)
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

explosion_data = { "surface": window,
                   "images": explosion_imgs,
                   "explosions_sfx": explosions_sfx}

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

running = True
in_devlogo_screen = True
menu = False
gaming = False
in_scores = False
game_over = False
paused = False
played_once = False

while running:

    # Initialize the game objects and variables ================================

    # Empty the sprites
    sprites.empty()
    enemies.empty()
    p_lasers.empty()
    e_lasers.empty()
    upgrades.empty()
    particles[:] = []
    bouncies[:] = []
    

    # Instantiate the player
    player = Player(WIN_RES, player_imgs, p_spr_supergroup, Laser, p_laser_img, laser_sfx)
    player_group.add(player)
    sprites.add(player)

    # Reset the scores, and others
    spawn_timer = 0
    score = 0
    name = str()
    fade_timer = pygame.time.get_ticks()
    ts_timer = pygame.time.get_ticks() # Title screen timer
    dev_logo_alpha = 256
    logo_alpha = 0
    has_faded = False # for menu

    spawn_bouncies(window, bouncies)

    while in_devlogo_screen:

         # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_devlogo_screen = False
        
        # Draw processes =======================================================
        
        now = pygame.time.get_ticks()
        if now - ts_timer > 3000:
            now = pygame.time.get_ticks()
            if now - fade_timer > 1000:
                dev_logo_alpha -= 5
                dev_logo_img.set_alpha(dev_logo_alpha)
                window.fill(BLACK)
                draw_bouncies(bouncies)
                window.blit(dev_logo_img, ( (WIN_RES["w"] / 2) - (dev_logo_img.get_width() / 2) * 2.8, WIN_RES["h"] * 0.3) )
                pygame.display.flip()

            if dev_logo_alpha < 0: # If image has almost faded out
                # Play the soundtrack
                pygame.mixer.music.play(loops=-1)
                in_devlogo_screen = False
                menu = True
        else:
            window.fill(BLACK)
            draw_bouncies(bouncies)
            window.blit(dev_logo_img, ( (WIN_RES["w"] / 2) - (dev_logo_img.get_width() / 2) * 2.8, WIN_RES["h"] * 0.3) )
            draw_text(window, "a game by", 32, game_font, WIN_RES["w"] / 2.3, WIN_RES["h"] * 0.4, WHITE)
            draw_text(window, "zyenapz", 32, game_font, WIN_RES["w"] / 2.3, WIN_RES["h"] * 0.45, WHITE)
            draw_text(window, "(c) 2020 zyenapz. All rights reserved.", 14, game_font, WIN_RES["w"] / 2, WIN_RES["h"] * 0.97, WHITE, "centered")
                
        # Update the window
        pygame.display.flip()

    while menu:

        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 2
        backgroundp_y += 4

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            elif event.type == pygame.KEYDOWN and has_faded:
                if event.key == pygame.K_z:
                    menu = False
                    gaming = True
                    played_once = True
                elif event.key == pygame.K_s:
                    menu = False
                    in_scores = True
                elif event.key == pygame.K_x:
                    running = False
                    menu = False

        # Update processes =====================================================
        if not played_once:
            if logo_alpha < 255:
                logo_alpha += 3
                logo_img.set_alpha(logo_alpha)
        else:
            logo_alpha = 255
            
        if logo_alpha >= 255:
            has_faded = True

        # Draw objects =========================================================

        # Draw the background and the parallax
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)

        # Draw the title screen texts and images
        window.blit(logo_img, (window_rect.centerx-240, -64))
        if has_faded:
            draw_text(window, "powered by pygame", 16, game_font, window_rect.centerx, window_rect.centery-32, GRAY, "centered")
            draw_text(window, "[Z] Play", 32, game_font, window_rect.centerx, window_rect.centery+64, WHITE, "centered")
            draw_text(window, "  [S] Scores", 32, game_font, window_rect.centerx, window_rect.centery+96, WHITE, "centered")
            draw_text(window, "[X] Exit", 32, game_font, window_rect.centerx, window_rect.centery+128, WHITE, "centered")
            draw_text(window, "(c) 2020 zyenapz.", 16, game_font, window_rect.centerx, window_rect.bottom-98, GRAY, "centered")
            draw_text(window, "All rights reserved.", 16, game_font, window_rect.centerx, window_rect.bottom-82, GRAY, "centered")
            draw_text(window, "Game & Art by zyenapz", 16, game_font, window_rect.centerx, window_rect.bottom-66, GRAY, "centered")
            draw_text(window, "Music by YoItsRion", 24, game_font, window_rect.centerx, window_rect.bottom-45, GRAY, "centered")

        # Update the window
        pygame.display.flip()

    while in_scores:

        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 2
        backgroundp_y += 4

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_scores = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    menu = True
                    in_scores = False

        # Draw objects =========================================================
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
        draw_text(window, "High Scores", 32, game_font, window_rect.centerx, window_rect.top+32, WHITE, "centered")
        draw_text(window, "[X] Back", 32, game_font, window_rect.centerx, window_rect.bottom-64, WHITE, "centered")

        # Draw highscores
        if hi_scores != []:
            for i in range(len(hi_scores[:8])):
                name = hi_scores[i][0].upper()
                score = str(hi_scores[i][1]).zfill(4)
                if i == 0:
                    if hi_scores[i][1] > LEGEND_SCORE:
                        draw_text(window, f"{name} L{score}", 40, game_font, window_rect.centerx, 156, PURPLE, "centered")
                    else:
                        draw_text(window, f"{name} {score}", 40, game_font, window_rect.centerx, 156, GOLD, "centered")
                else:
                    if hi_scores[i][1] > LEGEND_SCORE:
                        draw_text(window, f"{name:<6} L{score}", 40, game_font, window_rect.centerx, 156+(40*(i+1)), PURPLE, "centered")
                    else:
                        draw_text(window, f"{name} {score}", 40, game_font, window_rect.centerx, 156+(40*(i+1)), WHITE, "centered")
        else:
            draw_text(window, f"No scores yet", 32, game_font, window_rect.centerx, window_rect.centery, WHITE, "centered")

        # Update the window
        pygame.display.flip()

    while gaming:
        if not paused:

            if spawn_timer == 0:
                spawn_timer = pygame.time.get_ticks()

            # Lock the FPS
            clock.tick(FPS)

            # Increment the background and parallax's ypos
            background_y += 1
            backgroundp_y += 2

            # Get input ========================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        paused = True

            # Update objects ===================================================

            # Spawn an enemy
            now = pygame.time.get_ticks()
            if (now - spawn_timer > spawn_delay - sd_subtractor(score) and
                len(enemies) < max_enemy(score)):
                spawn_timer = now
                roll_spawn(score)

            # Check if enemy is hit by lasers
            hits = pygame.sprite.groupcollide(enemies, p_lasers, False, True)
            for hit in hits:
                hit.spdy = -6 # Knockback effect
                hit.health -= 1
                spawn_explosion(Explosion, explosion_data, hit.rect.centerx, hit.rect.bottom, sprites)
                if hit.health <= 0:
                    offset = shake(15, 5)
                    u = Upgrade(window, upgrade_imgs, hit.rect.center, score)
                    sprites.add(u)
                    upgrades.add(u)
                    spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(10,16), particle_colors)

            # Check if the player collides with an enemy
            hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= 5
                spawn_explosion(Explosion, explosion_data, hit.rect.centerx, hit.rect.bottom, sprites)
                spawn_explosion(Explosion, explosion_data, player.rect.centerx, player.rect.bottom, sprites)
                offset = shake(20, 10)
                spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(10,16), particle_colors)

            # Check if player is hit by enemy lasers
            hits = pygame.sprite.spritecollide(player, e_lasers, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= hit.damage
                spawn_explosion(Explosion, explosion_data, player.rect.centerx, player.rect.bottom, sprites)
                offset = shake(20, 10)

            # Check if player picks up an upgrade
            hits = pygame.sprite.spritecollide(player, upgrades, True, pygame.sprite.collide_circle)
            for hit in hits:
                if hit.type == "gun":
                    if player.cur_lvl < 2:
                        player.cur_lvl += 1
                        if player.cur_lvl >= 2:
                            player.cur_lvl = 2
                        player.lvl = player.lvls[player.cur_lvl]
                    else:
                        player.health += 1
                        if player.health >= 10:
                            player.health = 10
                    upgrade_sfx.play()
                elif hit.type == "hp":
                    player.health += 2
                    if player.health >= 10:
                        player.health = 10
                    upgrade_sfx.play()
                elif hit.type == "coin":
                    score += 1
                    coin_sfx.play()

            # Check if player has no health
            if player.health <= 0:
                spawn_particles(player.rect.centerx, player.rect.centery, 50, particle_colors)
                gaming = False
                game_over = True
                player.kill()

            sprites.update()

            # Draw objects =====================================================

            # Draw the background and the parallax
            draw_background(window, background_img, background_rect, background_y)
            draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)

            # Draw the sprites
            sprites.draw(window)
            update_particles()

            # Draw the HUD
            window.blit(score_img, (score_rect.x, score_rect.y))
            if score > LEGEND_SCORE:
                draw_text(window, f"LEGEND", 24, game_font, score_rect.x*12, score_rect.y+4, GOLD, "centered")
            else:
                draw_text(window, f"{str(score).zfill(4)}", 24, game_font, score_rect.x*9.5, score_rect.y+4, WHITE, "centered")
            window.blit(upgrade_imgs["gun"][0], (score_rect.x, score_rect.y*1.8))
            draw_text(window, f"{player.cur_lvl+1}/3", 24, game_font, score_rect.x*8.5, score_rect.y*2, WHITE, "centered")
            draw_hp(window, 10, 10, player.health, RED, hp_bar_img)

            # Screen shake
            window.blit(window, next(offset))

            # Update the window
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_x:
                        paused = False
                        gaming = False
                        menu = True

            # Draw the pause texts
            draw_text(window, f"PAUSED", 32, game_font, window_rect.centerx, window_rect.centery-32, WHITE, "centered")
            draw_text(window, f"[ESC][P] Resume", 24, game_font, window_rect.centerx, window_rect.centery+32, WHITE, "centered")
            draw_text(window, f"   [X] Quit", 24, game_font, window_rect.centerx, window_rect.centery+66, WHITE, "centered")

            # Update the window
            pygame.display.flip()

    while game_over:
        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 1
        backgroundp_y += 2

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1] # Remove the last character
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        menu = True
                        game_over = False
                        hi_scores.append([name, score])
                        hi_scores = sort(hi_scores)
                        write_savedata(hi_scores, scores_path)
                else:
                    if chr(event.key) in 'abcdefghijklmnopqrstuvwxyz0123456789':
                        if len(name) < 5:
                            name = name + chr(event.key) # Concatenate the letter to the string
                            typing_sfx.play()
                        else:
                            denied_sfx.play()

        # Update objects =======================================================

        sprites.update()

        # Draw objects =========================================================

        # Draw the background and the parallax
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)

        # Draw the sprites
        sprites.draw(window)
        update_particles()

        # Draw the HUD
        window.blit(score_img, (10, 50))
        if score > LEGEND_SCORE:
            draw_text(window, f"LEGEND {score}", 24, game_font, score_rect.x*18, score_rect.y+4, GOLD, "centered")
        else:
            draw_text(window, f"{str(score).zfill(4)}", 24, game_font, score_rect.x*9.5, score_rect.y+4, WHITE, "centered")
        draw_hp(window, 10, 10, player.health, RED, hp_bar_img)
        window.blit(upgrade_imgs["gun"][0], (score_rect.x, score_rect.y*1.8))

        # Draw the Game Over texts
        draw_text(window, f"{player.cur_lvl+1}/3", 24, game_font, score_rect.x*8.5, score_rect.y*2, WHITE, "centered")
        draw_text(window, "GAME OVER", 64, game_font, window_rect.centerx, window_rect.centery-64, WHITE, "centered")
        draw_text(window, "Enter name", 32, game_font, window_rect.centerx, window_rect.centery+32, WHITE, "centered")
        draw_text(window, f"{name.upper()}", 32, game_font, window_rect.centerx, window_rect.centery+74, WHITE, "centered")
        if len(name) > 2:
            draw_text(window, "Press ENTER", 24, game_font, window_rect.centerx, window_rect.centery+132, WHITE, "centered")

        # Screen shake
        window.blit(window, next(offset))

        # Update the window
        pygame.display.flip()

# Save high scores to file before exiting
write_savedata(hi_scores, scores_path)

# Quit pygame
pygame.quit()

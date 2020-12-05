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

# Import libraries
try:
    import pygame, os, random, math
    from itertools import repeat
    from data.scripts.bullets import Laser, Fireball
    from data.scripts.monsters import Hellfighter, Raider, Fatty
    from data.scripts.player import Player
    from data.scripts.effects import Explosion, Particle
    from data.scripts.difficulty import max_enemy, sd_subtractor
    from data.scripts.draw import draw_background, draw_text, draw_hp, shake
    from data.scripts.upgrade import Upgrade
except Exception as e:
    print(e)
    exit()

# Initialize pygame
pygame.init()

# Program variables
WIN_RES = {"w": 640, "h": 676}
TITLE = "Star Fighter"
AUTHOR = "zyenapz"
VERSION = "1.0"
# Colors
BLACK = (0,0,0)
WHITE = (235,235,235)
GRAY = (100,100,100)
RED = (180,32,42)
# FPS an d timing
clock = pygame.time.Clock()
FPS = 60
spawn_delay = 2000
# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
game_font = "data/font/prstartk.ttf"
# Game loop booleans
running = True
game_over = False
paused = False
# Other variables
score = 0
background_y = 0 # For the background's y coordinate
backgroundp_y = 0 # For parallax's y coordinate
offset = repeat((0, 0)) # For screen shake
scale = 4 # For scaling images

# Initialize the window
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode((WIN_RES["w"], WIN_RES["h"]))
window_rect = window.get_rect()
pygame.display.set_caption(TITLE)

# Images ==========================================================================
def load_png(file, directory, scale):
    try:
        path = os.path.join(directory, file)
        img = pygame.image.load(path).convert_alpha()
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(e)
        exit()

window_icon = load_png("hellfighter1.png", IMG_DIR, 1)
pygame.display.set_icon(window_icon)

player_imgs = dict()

# Load and store cadet player frames
player_cadet = dict()
player_cadet["left"] = [
    load_png("player_cadet_l1.png", IMG_DIR, scale),
    load_png("player_cadet_l2.png", IMG_DIR, scale)
]
player_cadet["normal"] = [
    load_png("player_cadet_n1.png", IMG_DIR, scale),
    load_png("player_cadet_n2.png", IMG_DIR, scale)
]
player_cadet["right"] = [
    load_png("player_cadet_r1.png", IMG_DIR, scale),
    load_png("player_cadet_r2.png", IMG_DIR, scale)
]
player_imgs["cadet"] = player_cadet

# Load and store captain player frames
player_captain = dict()
player_captain["left"] = [
    load_png("player_captain_l1.png", IMG_DIR, scale),
    load_png("player_captain_l2.png", IMG_DIR, scale)
]
player_captain["normal"] = [
    load_png("player_captain_n1.png", IMG_DIR, scale),
    load_png("player_captain_n2.png", IMG_DIR, scale)
]
player_captain["right"] = [
    load_png("player_captain_r1.png", IMG_DIR, scale),
    load_png("player_captain_r2.png", IMG_DIR, scale)
]
player_imgs["captain"] = player_captain

# Load and store admiral player frames
player_admiral = dict()
player_admiral["left"] = [
    load_png("player_admiral_l1.png", IMG_DIR, scale),
    load_png("player_admiral_l2.png", IMG_DIR, scale)
]
player_admiral["normal"] = [
    load_png("player_admiral_n1.png", IMG_DIR, scale),
    load_png("player_admiral_n2.png", IMG_DIR, scale)
]
player_admiral["right"] = [
    load_png("player_admiral_r1.png", IMG_DIR, scale),
    load_png("player_admiral_r2.png", IMG_DIR, scale)
]
player_imgs["admiral"] = player_admiral

# Load and store spawning player frames
player_imgs["spawning"] = [
    load_png("player_spawn1.png", IMG_DIR, scale),
    load_png("player_spawn2.png", IMG_DIR, scale),
    load_png("player_spawn3.png", IMG_DIR, scale),
    load_png("player_spawn4.png", IMG_DIR, scale)
]

# Load and store hellfighter images
hfighter_imgs = dict()
hfighter_imgs["normal"] = [
    load_png("hellfighter1.png", IMG_DIR, scale),
    load_png("hellfighter2.png", IMG_DIR, scale)
]
hfighter_imgs["spawning"] = [
    load_png("hf_spawn1.png", IMG_DIR, scale),
    load_png("hf_spawn2.png", IMG_DIR, scale),
    load_png("hf_spawn3.png", IMG_DIR, scale),
    load_png("hf_spawn4.png", IMG_DIR, scale)
]

# Load and store raider images
raider_imgs = dict()
raider_imgs["normal"] = [
    load_png("raider1.png", IMG_DIR, scale),
    load_png("raider2.png", IMG_DIR, scale)
]
raider_imgs["spawning"] = [
    load_png("raider_spawn1.png", IMG_DIR, scale),
    load_png("raider_spawn2.png", IMG_DIR, scale),
    load_png("raider_spawn3.png", IMG_DIR, scale),
    load_png("raider_spawn4.png", IMG_DIR, scale),
]

# Load and store fatty images
fatty_imgs = dict()
fatty_imgs["normal"] = [
    load_png("fatty1.png", IMG_DIR, scale),
    load_png("fatty2.png", IMG_DIR, scale)
]
fatty_imgs["spawning"] = [
    load_png("fatty_spawn1.png", IMG_DIR, scale),
    load_png("fatty_spawn2.png", IMG_DIR, scale),
    load_png("fatty_spawn3.png", IMG_DIR, scale),
    load_png("fatty_spawn4.png", IMG_DIR, scale)
]

# Load and store explosion images
explosion_imgs = [
    load_png("explosion1.png", IMG_DIR, scale),
    load_png("explosion2.png", IMG_DIR, scale),
    load_png("explosion3.png", IMG_DIR, scale),
    load_png("explosion4.png", IMG_DIR, scale)
]

# Load and store upgrade images
upgrade_imgs = dict()
upgrade_imgs["hp"] = [ load_png("upgrd_hp1.png", IMG_DIR, scale),
                       load_png("upgrd_hp2.png", IMG_DIR, scale),
                       load_png("upgrd_hp3.png", IMG_DIR, scale),
                       load_png("upgrd_hp4.png", IMG_DIR, scale) ]
upgrade_imgs["gun"] = [ load_png("upgrd_gun1.png", IMG_DIR, scale),
                        load_png("upgrd_gun2.png", IMG_DIR, scale),
                        load_png("upgrd_gun3.png", IMG_DIR, scale),
                        load_png("upgrd_gun4.png", IMG_DIR, scale) ]
upgrade_imgs["coin"] = [ load_png("upgrd_coin1.png", IMG_DIR, scale),
                         load_png("upgrd_coin2.png", IMG_DIR, scale),
                         load_png("upgrd_coin3.png", IMG_DIR, scale),
                         load_png("upgrd_coin4.png", IMG_DIR, scale) ]

p_laser_img = load_png("laser_player.png", IMG_DIR, scale)
e_laser_img = load_png("laser_enemy.png", IMG_DIR, scale)
fireball_img = load_png("fireball.png", IMG_DIR, scale)
logo_img = load_png("logo.png", IMG_DIR, 8)
background_img = load_png("background.png", IMG_DIR, scale)
background_rect = background_img.get_rect()
backgroundp_img = load_png("background_parallax.png", IMG_DIR, scale)
backgroundp_rect = backgroundp_img.get_rect()
hp_bar_img = load_png("hp_bar.png", IMG_DIR, scale)
hp_bar_rect = hp_bar_img.get_rect()
hp_bar_rect.x = 20
hp_bar_rect.y = 20
score_img = load_png("score_icon.png", IMG_DIR, scale)
score_rect = score_img.get_rect()
score_rect.x = 10
score_rect.y = hp_bar_rect.y + 30

# Sounds ==========================================================================

def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

laser_sfx = load_sound("sfx_lasershoot.wav", SFX_DIR, 0.5)
upgrade_sfx = load_sound("sfx_powerup.wav", SFX_DIR, 0.5)
coin_sfx = load_sound("sfx_coinpickup.wav", SFX_DIR, 0.5)
explosions_sfx = [ load_sound("sfx_explosion1.wav", SFX_DIR, 0.5),
                   load_sound("sfx_explosion2.wav", SFX_DIR, 0.5),
                   load_sound("sfx_explosion3.wav", SFX_DIR, 0.5) ]

pygame.mixer.music.load(os.path.join(SFX_DIR, "ost_fighter.ogg"))
pygame.mixer.music.set_volume(0.4)

# Sprite Groups ===================================================================

# Sprite groups
sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
p_lasers = pygame.sprite.Group()
e_lasers = pygame.sprite.Group()
upgrades = pygame.sprite.Group()
particles = list()

# Sprite supergroups
p_spr_supergroup = {"sprites": sprites, "p_lasers": p_lasers}
e_spr_supergroup = {"sprites": sprites, "e_lasers": e_lasers}

# Spawner Functions ===============================================================

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

def spawn_particles(x, y, amnt):
    for _ in range(amnt):
        p = Particle(window, WIN_RES, random.randrange(x-10,x), random.randrange(y-10,y))
        particles.append(p)

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
        choices = random.choices(monsters, [0.25, 0.70, 0.05], k=1)
        roll = choices[0]
    else:
        choices = random.choices(monsters, [0.30,0.55,0.15], k=1)
        roll = choices[0]

    if roll == "raider":
        spawn_raider()
    elif roll == "hellfighter":
        spawn_hfighter()
    elif roll == "fatty":
        spawn_fatty()

# Game loop =======================================================================

# Play the soundtrack
pygame.mixer.music.play(loops=-1)

running = True
menu = True
gaming = False
game_over = False

while running:

    # Empty the sprites
    sprites.empty()
    enemies.empty()
    p_lasers.empty()
    e_lasers.empty()
    upgrades.empty()
    particles[:] = []

    # Instantiate the player ==========================================================
    player = Player(WIN_RES, player_imgs, p_spr_supergroup, Laser, p_laser_img, laser_sfx)
    player_group.add(player)
    sprites.add(player)
    spawn_timer = 0
    score = 0

    while menu:

        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 2
        backgroundp_y += 4

        # Get input ===========================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    menu = False
                    gaming = True
                elif event.key == pygame.K_h:
                    pass
                    # TODO
                elif event.key == pygame.K_x:
                    running = False
                    menu = False

        # Update objects ======================================================

        # Draw objects
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
        window.blit(logo_img, (window_rect.centerx-240, -64))
        draw_text(window, f"powered by pygame", 16, game_font, window_rect.centerx, window_rect.centery-32, GRAY)
        draw_text(window, f"[C] Play", 32, game_font, window_rect.centerx, window_rect.centery+64, WHITE)
        #draw_text(window, f"[H] Scores", 32, game_font, window_rect.centerx, window_rect.centery+64, WHITE)
        draw_text(window, f"[X] Exit", 32, game_font, window_rect.centerx, window_rect.centery+96, WHITE)
        draw_text(window, f"(c) 2020 zyenapz.", 16, game_font, window_rect.centerx, window_rect.bottom-98, GRAY)
        draw_text(window, f"All rights reserved.", 16, game_font, window_rect.centerx, window_rect.bottom-82, GRAY)
        draw_text(window, f"Game & Art by zyenapz", 16, game_font, window_rect.centerx, window_rect.bottom-66, GRAY)
        draw_text(window, f"Music by YoItsRion", 16, game_font, window_rect.centerx, window_rect.bottom-50, GRAY)
        draw_text(window, f"Font by codeman38", 16, game_font, window_rect.centerx, window_rect.bottom-34, GRAY)

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

            # Get input ===========================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = True

            # Update objects ======================================================
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
                    spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(10,16))

            # Check if the player collides with an enemy
            hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
            for hit in hits:
                player.health -= 5
                spawn_explosion(Explosion, explosion_data, hit.rect.centerx, hit.rect.bottom, sprites)
                spawn_explosion(Explosion, explosion_data, player.rect.centerx, player.rect.bottom, sprites)
                offset = shake(20, 10)
                spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(10,16))

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
                spawn_particles(player.rect.centerx, player.rect.centery, 50)
                gaming = False
                game_over = True
                player.kill()

            sprites.update()

            # Draw objects ========================================================
            draw_background(window, background_img, background_rect, background_y)
            draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
            sprites.draw(window)
            window.blit(score_img, (score_rect.x, score_rect.y))
            draw_text(window, f"{str(score).zfill(3)}", 24, game_font, score_rect.x*8.5, score_rect.y+4, WHITE)
            draw_hp(window, 10, 10, player.health, RED, hp_bar_img)
            window.blit(window, next(offset))
            update_particles()

            # Update the window
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                    elif event.key == pygame.K_x:
                        paused = False
                        gaming = False
                        menu = True

            draw_text(window, f"PAUSED", 32, game_font, window_rect.centerx, window_rect.centery-32, WHITE)
            draw_text(window, f"[ESC] Resume", 32, game_font, window_rect.centerx, window_rect.centery, WHITE)
            draw_text(window, f"[X] Quit", 32, game_font, window_rect.centerx, window_rect.centery+32, WHITE)
            pygame.display.flip()

    while game_over:
        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 1
        backgroundp_y += 2

        # Get input ===========================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gaming = True
                    game_over = False
                elif event.key == pygame.K_x:
                    game_over = False
                    menu = True

        # Update objects ======================================================

        sprites.update()

        # Draw objects ========================================================
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
        sprites.draw(window)
        update_particles()
        window.blit(score_img, (10, 50))
        draw_text(window, f"{str(score).zfill(3)}", 24, game_font, score_rect.x*8.5, score_rect.y+4, WHITE)
        draw_hp(window, 10, 10, player.health, RED, hp_bar_img)
        draw_text(window, f"GAME OVER", 64, game_font, window_rect.centerx, window_rect.centery-64, WHITE)
        draw_text(window, f"[C] Retry", 32, game_font, window_rect.centerx, window_rect.centery+32, WHITE)
        draw_text(window, f"[X] Quit", 32, game_font, window_rect.centerx, window_rect.centery+64, WHITE)
        window.blit(window, next(offset))
        # Update the window
        pygame.display.flip()

# Quit pygame
pygame.quit()

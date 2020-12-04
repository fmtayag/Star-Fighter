#####################################
# StarFighter                       #
# Programmed by: zyenapz            #
#   - E-mail: zyenapz@gmail.com     #
#   - Website: zyenapz.github.io    #
# Soundtrack by: yoitsrion          #
#   - Soundcloud: yoitsrion         #
# Font: VCR OSD Mono                #
#   - By: Riciery Leal              #
#   - Downloaded from dafont.com    #
#####################################

# TODO: Change fireball's damage as it dissolves (DONE)
# TODO: Clean up the spawner functions
# TODO: Bundle relevant sprite groups into individual dictionaries. For Monsters class.
    # TODO: Maybe just add a method that calls a "spawn_laser" function??

# Import libraries
try:
    import pygame, os, random, numpy, math
    from itertools import repeat
    from scripts.bullets import Laser, Fireball
    from scripts.monsters import Hellfighter, Raider, Fatty
    from scripts.player import Player
    from scripts.effects import Explosion, Particle
    from scripts.gameflow import max_enemy, sd_subtractor
    from scripts.draw import draw_background, draw_text, draw_hp, shake
    from scripts.upgrade import Upgrade
    from scripts.spawner import spawn_explosion
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
BLACK = (0,0,0)
WHITE = (235,235,235)
RED = (180,32,42)
FPS = 60
GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, "img")
SFX_DIR = os.path.join(GAME_DIR, "sfx")
game_font = "font/VCR_OSD_MONO.ttf"
clock = pygame.time.Clock()
score = 0
spawn_delay = 2000
spawn_timer = pygame.time.get_ticks()
background_y = 0
backgroundp_y = 0
running = True
game_over = False
paused = False
offset = repeat((0, 0)) # For screen shake

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
    load_png("player_cadet_l1.png", IMG_DIR, 4),
    load_png("player_cadet_l2.png", IMG_DIR, 4)
]
player_cadet["normal"] = [
    load_png("player_cadet_n1.png", IMG_DIR, 4),
    load_png("player_cadet_n2.png", IMG_DIR, 4)
]
player_cadet["right"] = [
    load_png("player_cadet_r1.png", IMG_DIR, 4),
    load_png("player_cadet_r2.png", IMG_DIR, 4)
]
player_imgs["cadet"] = player_cadet

# Load and store captain player frames
player_captain = dict()
player_captain["left"] = [
    load_png("player_captain_l1.png", IMG_DIR, 4),
    load_png("player_captain_l2.png", IMG_DIR, 4)
]
player_captain["normal"] = [
    load_png("player_captain_n1.png", IMG_DIR, 4),
    load_png("player_captain_n2.png", IMG_DIR, 4)
]
player_captain["right"] = [
    load_png("player_captain_r1.png", IMG_DIR, 4),
    load_png("player_captain_r2.png", IMG_DIR, 4)
]
player_imgs["captain"] = player_captain

# Load and store admiral player frames
player_admiral = dict()
player_admiral["left"] = [
    load_png("player_admiral_l1.png", IMG_DIR, 4),
    load_png("player_admiral_l2.png", IMG_DIR, 4)
]
player_admiral["normal"] = [
    load_png("player_admiral_n1.png", IMG_DIR, 4),
    load_png("player_admiral_n2.png", IMG_DIR, 4)
]
player_admiral["right"] = [
    load_png("player_admiral_r1.png", IMG_DIR, 4),
    load_png("player_admiral_r2.png", IMG_DIR, 4)
]
player_imgs["admiral"] = player_admiral

# Load and store hellfighter images
hfighter_imgs = dict()
hfighter_imgs["normal"] = [
    load_png("hellfighter1.png", IMG_DIR, 4),
    load_png("hellfighter2.png", IMG_DIR, 4)
]
hfighter_imgs["spawning"] = [
    load_png("hf_spawn1.png", IMG_DIR, 4),
    load_png("hf_spawn2.png", IMG_DIR, 4),
    load_png("hf_spawn3.png", IMG_DIR, 4),
    load_png("hf_spawn4.png", IMG_DIR, 4)
]

# Load and store raider images
raider_imgs = dict()
raider_imgs["normal"] = [
    load_png("raider1.png", IMG_DIR, 4),
    load_png("raider2.png", IMG_DIR, 4)
]
raider_imgs["spawning"] = [
    load_png("raider_spawn1.png", IMG_DIR, 4),
    load_png("raider_spawn2.png", IMG_DIR, 4),
    load_png("raider_spawn3.png", IMG_DIR, 4),
    load_png("raider_spawn4.png", IMG_DIR, 4),
]

# Load and store fatty images
fatty_imgs = dict()
fatty_imgs["normal"] = [
    load_png("fatty1.png", IMG_DIR, 4),
    load_png("fatty2.png", IMG_DIR, 4)
]
fatty_imgs["spawning"] = [
    load_png("fatty_spawn1.png", IMG_DIR, 4),
    load_png("fatty_spawn2.png", IMG_DIR, 4),
    load_png("fatty_spawn3.png", IMG_DIR, 4),
    load_png("fatty_spawn4.png", IMG_DIR, 4)
]

# Load and store explosion images
explosion_imgs = [
    load_png("explosion1.png", IMG_DIR, 4),
    load_png("explosion2.png", IMG_DIR, 4),
    load_png("explosion3.png", IMG_DIR, 4),
    load_png("explosion4.png", IMG_DIR, 4)
]

# Load and store upgrade images
upgrade_imgs = dict()
upgrade_imgs["hp"] = [ load_png("upgrd_hp1.png", IMG_DIR, 4),
                       load_png("upgrd_hp2.png", IMG_DIR, 4),
                       load_png("upgrd_hp3.png", IMG_DIR, 4),
                       load_png("upgrd_hp4.png", IMG_DIR, 4) ]
upgrade_imgs["gun"] = [ load_png("upgrd_gun1.png", IMG_DIR, 4),
                        load_png("upgrd_gun2.png", IMG_DIR, 4),
                        load_png("upgrd_gun3.png", IMG_DIR, 4),
                        load_png("upgrd_gun4.png", IMG_DIR, 4) ]
upgrade_imgs["coin"] = [ load_png("upgrd_coin1.png", IMG_DIR, 4),
                         load_png("upgrd_coin2.png", IMG_DIR, 4),
                         load_png("upgrd_coin3.png", IMG_DIR, 4),
                         load_png("upgrd_coin4.png", IMG_DIR, 4) ]

p_laser_img = load_png("laser_player.png", IMG_DIR, 4)
e_laser_img = load_png("laser_enemy.png", IMG_DIR, 4)
#particle_img = load_png("particle.png", IMG_DIR, 2)
fireball_img = load_png("fireball.png", IMG_DIR, 4)
background_img = load_png("background.png", IMG_DIR, 4)
background_rect = background_img.get_rect()
backgroundp_img = load_png("background_parallax.png", IMG_DIR, 4)
backgroundp_rect = backgroundp_img.get_rect()
hp_bar_img = load_png("hp_bar.png", IMG_DIR, 4)
hp_bar_rect = hp_bar_img.get_rect()
hp_bar_rect.x = 20
hp_bar_rect.y = 20
score_img = load_png("score_icon.png", IMG_DIR, 4)
score_rect = score_img.get_rect()
score_rect.x = 10
score_rect.y = hp_bar_rect.y + 30

# Sounds ==========================================================================

def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

laser_sfx = load_sound("sfx_lasershoot.wav", SFX_DIR, 0.3)
upgrade_sfx = load_sound("sfx_powerup.wav", SFX_DIR, 0.3)
coin_sfx = load_sound("sfx_coinpickup.wav", SFX_DIR, 0.3)
explosions_sfx = [ load_sound("sfx_explosion1.wav", SFX_DIR, 0.3),
                   load_sound("sfx_explosion2.wav", SFX_DIR, 0.3),
                   load_sound("sfx_explosion3.wav", SFX_DIR, 0.3) ]

pygame.mixer.music.load(os.path.join(SFX_DIR, "ost_fighter.ogg"))
pygame.mixer.music.set_volume(0.5)

# Sprite Groups ===================================================================

# Sprite groups
sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
p_lasers = pygame.sprite.Group()
e_lasers = pygame.sprite.Group()
upgrades = pygame.sprite.Group()
particles = list() # I know...this isn't really a sprite group

# Sprite supergroups
p_spr_supergroup = {"sprites": sprites, "p_lasers": p_lasers}
e_spr_supergroup = {"sprites": sprites, "e_lasers": e_lasers}

# Instantiate the player ==========================================================
player = Player(WIN_RES, player_imgs, p_spr_supergroup, Laser, p_laser_img, laser_sfx)
player_group.add(player)
sprites.add(player)

# Spawner Functions ===============================================================

explosion_data = { "surface": window,
                   "images": explosion_imgs,
                   "explosions_sfx": explosions_sfx}

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
        roll = numpy.random.choice(monsters, p=[0.25, 0.70, 0.05])
    else:
        roll = numpy.random.choice(monsters, p=[0.30,0.55,0.15])

    if roll == "raider":
        spawn_raider()
    elif roll == "hellfighter":
        spawn_hfighter()
    elif roll == "fatty":
        spawn_fatty()

# Game loop =======================================================================

# Play the soundtrack
pygame.mixer.music.play(loops=-1)

while running:
    if not paused:
        # Lock the FPS
        clock.tick(FPS)

        # Increment the background and parallax's ypos
        background_y += 1
        backgroundp_y += 2

        # Get input ===========================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(6,12))
                
        # Check if the player collides with an enemy
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.health -= 5
            spawn_explosion(Explosion, explosion_data, hit.rect.centerx, hit.rect.bottom, sprites)
            spawn_explosion(Explosion, explosion_data, player.rect.centerx, player.rect.bottom, sprites)
            offset = shake(20, 10)
            spawn_particles(hit.rect.centerx, hit.rect.centery, random.randrange(6,12))

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
                player.cur_lvl += 1
                player.cur_lvl = numpy.clip(player.cur_lvl, 0, 2)
                player.lvl = player.lvls[player.cur_lvl]
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
            running = False
            #player.kill()

        sprites.update()
        cur_fps = round(clock.get_fps(), 2)
        pygame.display.set_caption(f"Star Fighter (FPS: {cur_fps})")

        # Draw objects ========================================================
        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
        sprites.draw(window)
        window.blit(score_img, (score_rect.x, score_rect.y))
        draw_text(window, f"{str(score).zfill(3)}", 20, game_font, score_rect.x*8, score_rect.y+6, WHITE)
        draw_hp(window, 10, 10, player.health, RED, hp_bar_img)
        window.blit(window, next(offset))
        update_particles()

        # Update the window
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        draw_text(window, f"PAUSED", 32, game_font, window_rect.centerx, window_rect.centery-32, WHITE)
        draw_text(window, f"ESC to Resume", 32, game_font, window_rect.centerx, window_rect.centery, WHITE)
        draw_text(window, f"X to Exit", 32, game_font, window_rect.centerx, window_rect.centery+32, WHITE)
        pygame.display.flip()

##def game_over():
##    # TODO
##
##    running = True
##    while running:
##        # Lock the FPS
##        clock.tick(FPS)
##
##        # Increment the background and parallax's ypos
##        background_y += 1
##        backgroundp_y += 2
##
##        # Get input ===========================================================
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                running = False
##            elif event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_RETURN:
##                    game_loop()
##
##        # Update objects ======================================================
##
##        sprites.update()
##        cur_fps = round(clock.get_fps(), 2)
##        pygame.display.set_caption(f"Star Fighter (FPS: {cur_fps})")
##
##        # Draw objects ========================================================
##        draw_background(window, background_img, background_rect, background_y)
##        draw_background(window, backgroundp_img, backgroundp_rect, backgroundp_y)
##        sprites.draw(window)
##        window.blit(score_img, (10, 50))
##        draw_text(window, f"{score}", 24, game_font, 60, 54, WHITE)
##        draw_hp(window, 10, 10, player.health, RED, hp_bar_img)
##        draw_text(window, f"GAME OVER", 32, game_font, window_rect.centerx, window_rect.centery-32, WHITE)
##        draw_text(window, f"RETURN to play again", 32, game_font, window_rect.centerx, window_rect.centery, WHITE)
##        draw_text(window, f"X to exit", 32, game_font, window_rect.centerx, window_rect.centery+32, WHITE)
##        window.blit(window, next(offset))
##        # Update the window
##        pygame.display.flip()

# Quit pygame
pygame.quit()

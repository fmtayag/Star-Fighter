# TODO list
# 1. (DONE) Make spawning animations for raider
# 2. (DONE) Finish implementing the raider enemy
# 3. (DONE) Implement the "Fatty" enemy
# 3.1 (DONE) Implement the "fireball" bullet. IT BOUNCES!
# 4. Make spawning animation / opening animation for player
# 5. Make start, game over, and high score screens
# 6. Add unique sound cues played on each monster's spawn animation
# 7. Limit the number of Fattys at any given time to 1.

# Import libraries
try:
    import pygame, os, random, numpy, math
    from scripts.bullets import Laser, Fireball
    from scripts.monsters import Hellfighter, Raider, Fatty
    from scripts.player import Player
    from scripts.effects import Explosion, SpawnAnim, Particle
    #from scripts.objects import Player, Hellfighter, Explosion, SpawnAnim
except Exception as e:
    print(e)
    exit()

# Initialize pygame
pygame.init()

# Program variables
running = True
clock = pygame.time.Clock()
WIDTH = 640
HEIGHT = 576
RES = (WIDTH, HEIGHT)
TITLE = "Star Fighter"
AUTHOR = "zyenapz"
VERSION = "1.0"
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
FPS = 60
GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, "img")
SFX_DIR = os.path.join(GAME_DIR, "sfx")
score = 0
spawn_delay = 2000
spawn_timer = pygame.time.get_ticks()
in_debugmode = True # For debugging
background_y = 0
backgroundp_y = 0

# Images
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

# Initialize the window
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode(RES)
pygame.display.set_caption(TITLE)
window_icon = load_png("upgrd_life.png", IMG_DIR, 1)
pygame.display.set_icon(window_icon)

# Images ==========================================================================

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

# Load and store player spawning frames
player_spawn_imgs = [
    load_png("player_spawn1.png", IMG_DIR, 4),
    load_png("player_spawn2.png", IMG_DIR, 4),
    load_png("player_spawn3.png", IMG_DIR, 4),
    load_png("player_spawn4.png", IMG_DIR, 4)
]
player_imgs["spawning"] = player_spawn_imgs

# Load and store hellfighter images
hellfighter_imgs = [
    load_png("hellfighter1.png", IMG_DIR, 4),
    load_png("hellfighter2.png", IMG_DIR, 4)
]

# Load and store hellfighter spawn images
hf_spawn_imgs = [
    load_png("hf_spawn1.png", IMG_DIR, 4),
    load_png("hf_spawn2.png", IMG_DIR, 4),
    load_png("hf_spawn3.png", IMG_DIR, 4),
    load_png("hf_spawn4.png", IMG_DIR, 4)
]

# Load and store raider images
raider_imgs = [
    load_png("raider1.png", IMG_DIR, 4),
    load_png("raider2.png", IMG_DIR, 4)
]

# Load and store raider spawn images
raider_spawn_imgs = [
    load_png("raider_spawn1.png", IMG_DIR, 4),
    load_png("raider_spawn2.png", IMG_DIR, 4),
    load_png("raider_spawn3.png", IMG_DIR, 4),
    load_png("raider_spawn4.png", IMG_DIR, 4),
]

# Load and store fatty images
fatty_imgs = [
    load_png("fatty1.png", IMG_DIR, 4),
    load_png("fatty2.png", IMG_DIR, 4)
]

# Load and store explosion images
explosion_imgs = [
    load_png("explosion1.png", IMG_DIR, 4),
    load_png("explosion2.png", IMG_DIR, 4),
    load_png("explosion3.png", IMG_DIR, 4),
    load_png("explosion4.png", IMG_DIR, 4)
]

p_laser_img = load_png("laser_player.png", IMG_DIR, 4)
e_laser_img = load_png("laser_enemy.png", IMG_DIR, 4)
particle_img = load_png("particle.png", IMG_DIR, 2)
fireball_img = load_png("fireball.png", IMG_DIR, 4)
background_img = load_png("background.png", IMG_DIR, 4).convert_alpha()
background_rect = background_img.get_rect()
backgroundp_img = load_png("background_parallax.png", IMG_DIR, 4).convert_alpha()
backgroundp_rect = backgroundp_img.get_rect()

# Sounds ==========================================================================

def load_sound(filename, sfx_dir):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    return snd

laser_sfx = load_sound("sfx_lasershoot.wav", SFX_DIR)
laser_sfx.set_volume(0.2)
explosion1_sfx = load_sound("sfx_explosion1.wav", SFX_DIR)
explosion1_sfx.set_volume(0.5)

## TODO: UNUSED YET
##sfx_explosion2 = load_sound("sfx_explosion2.wav")
##sfx_explosion3 = load_sound("sfx_explosion2.wav")
##sfx_powerup = load_sound("sfx_powerup.wav")

pygame.mixer.music.load(os.path.join(SFX_DIR, "ost_fighter.ogg"))
pygame.mixer.music.set_volume(0.3)

# Sprite Groups ===================================================================

sprites = pygame.sprite.Group()
player = pygame.sprite.Group()
enemies = pygame.sprite.Group()
p_lasers = pygame.sprite.Group()
e_lasers = pygame.sprite.Group()

# Spawner Functions ===============================================================
# Instantiate the player
player_data = { "surface": window,
                "images": player_imgs,
                "coords": (WIDTH/2, HEIGHT-64),
                "sprite_groups": (sprites, p_lasers),
                "laser_img": p_laser_img,
                "laser_sfx": laser_sfx,
                "spawn_imgs": player_spawn_imgs,
                "bullet_class": Laser }
player = Player(player_data)
sprites.add(player)

def spawn_hellfighter():
    # TODO: Clean up later
    hf_data = { "surface": window,
                 "images": hellfighter_imgs,
                 "coords": [random.randrange(64, WIDTH-64), random.randrange(0, 100)],
                 "spritegroups": [sprites, e_lasers],
                 "bullet_img": e_laser_img,
                 "bullet_class": Laser}
    hf_spawn_data = { "images": hf_spawn_imgs,
                      "coords": hf_data["coords"],
                      "spritegroups": [sprites, enemies],
                      "spawndata": hf_data,
                      "spawnclass": Hellfighter}
    hf_spawn = SpawnAnim(hf_spawn_data)
    sprites.add(hf_spawn)

def spawn_raider():
    # TODO: Clean up later
    raider_data = { "surface": window,
                    "images": raider_imgs,
                    "coords": [player.rect.x, 0],
                    "spritegroups": [sprites]}
    raider_spawn_data = { "images": raider_spawn_imgs,
                          "coords": raider_data["coords"],
                          "spritegroups": [sprites, enemies],
                          "spawndata": raider_data,
                          "spawnclass": Raider}
    raider_spawn = SpawnAnim(raider_spawn_data)
    sprites.add(raider_spawn)

def spawn_fatty():
    # TODO: Clean up later
    fatty_data = { "surface": window,
                 "images": fatty_imgs,
                 "coords": [random.randrange(64, WIDTH-64), -64],
                 "spritegroups": [sprites, e_lasers],
                 "bullet_img": fireball_img,
                 "bullet_class": Fireball,}
    fatty = Fatty(fatty_data)
    sprites.add(fatty)
    enemies.add(fatty)

def spawn_explosion(xpos, ypos):
    # TODO: Clean up later
    explosion_data = { "surface": window,
                       "images": explosion_imgs,
                       "coords": (xpos, ypos),
                       "explosion_sfx": explosion1_sfx}
    e = Explosion(explosion_data)
    sprites.add(e)

def roll_spawn():
    roll = numpy.random.choice(["raider","hellfighter", "fatty"], p=[0.2, 0.7, 0.1])
    #roll = numpy.random.choice(["raider","hellfighter", "fatty"], p=[0, 0, 1])
    if roll == "raider":
        spawn_raider()
    elif roll == "hellfighter":
        spawn_hellfighter()
    elif roll == "fatty":
        spawn_fatty()

# Game Flow Functions ===============================================================
# Functions that controls the "game flow"

def max_enemy(score):
    # Computes the maximum number of enemies that can spawn
    if score < 2:
        return 1
    else:
        limit = math.log(score)*2
        if limit >= 8: # Caps the limit at 8
            return 8
        else:
            return limit

def sd_subtractor(score):
    # Calculates the subtractor of the spawn delay (sd_s) based on score
    if score == 0:
        return 0
    else:
        sd_s = math.pow(score, 2)
        return numpy.clip(sd_s, 0, 1500)

# Draw functions =================================================================
def draw_background(background_y):
    rel_y = background_y % background_rect.height
    window.blit(background_img, (0, rel_y - background_rect.height))

    if rel_y < HEIGHT:
        window.blit(background_img, (0, rel_y))

def draw_backgroundp(backgroundp_y):
    rel_y = backgroundp_y % backgroundp_rect.height
    window.blit(backgroundp_img, (0, rel_y - backgroundp_rect.height))

    if rel_y < HEIGHT:
        window.blit(backgroundp_img, (0, rel_y))

# Game loop =======================================================================

# Play the soundtrack
pygame.mixer.music.play(loops=-1)

while running:

    # Lock the FPS
    clock.tick(FPS)

    # Get input ===================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and in_debugmode:
            # For debugging only
            if event.key == pygame.K_q:
                player.cur_lvl -= 1
                player.cur_lvl = numpy.clip(player.cur_lvl, 0, 2)
                player.lvl = player.lvls[player.cur_lvl]
            elif event.key == pygame.K_e:
                player.cur_lvl += 1
                player.cur_lvl = numpy.clip(player.cur_lvl, 0, 2)
                player.lvl = player.lvls[player.cur_lvl]

    # Update objects ==============================================================
    now = pygame.time.get_ticks()
    if (now - spawn_timer > spawn_delay - sd_subtractor(score) and
        len(enemies) < max_enemy(score)):
        spawn_timer = now
        roll_spawn()

    # Check if enemy is hit by lasers
    hits = pygame.sprite.groupcollide(enemies, p_lasers, False, True)
    for hit in hits:
        hit.spdy = -6 # Knockback effect
        hit.health -= 1
        hit.explode(spawn_explosion, hit.rect.centerx, hit.rect.bottom)
        if hit.health <= 0:
            score += 1

    # Check if player is hit by enemy lasers
    hits = pygame.sprite.spritecollide(player, e_lasers, True, pygame.sprite.collide_circle)
    for hit in hits:
        # Knockback effect (x-axis).
        if player.rect.x < hit.rect.left:
            player.spdx -= 3
        else:
            player.spdx += 3
        # Knockback effect (y-axis).
        if player.rect.y < hit.rect.top:
            player.spdy -= 3
        else:
            player.spdy += 3

        player.health -= random.randrange(5,10)
        player.explode(spawn_explosion, player.rect.centerx, player.rect.bottom)

    # Check if the player collides with an enemy
    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        # Knockback effect.
        if player.rect.y < hit.rect.top:
            player.spdy -= 6
        else:
            player.spdy += 6
        player.health -= random.randrange(25,50)
        hit.explode(spawn_explosion, hit.rect.centerx, hit.rect.bottom)
        player.explode(spawn_explosion, player.rect.centerx, player.rect.bottom)

    if player.health <= 0:
        running = False
    
    sprites.update()
    cur_fps = round(clock.get_fps(), 2)
    pygame.display.set_caption(f"Star Fighter (FPS: {cur_fps})")

    # Draw objects ================================================================
    background_y += 1
    backgroundp_y += 2
    draw_background(background_y)
    draw_backgroundp(backgroundp_y)
    sprites.draw(window)

    # Update the window
    pygame.display.flip()

# Quit pygame
pygame.quit()

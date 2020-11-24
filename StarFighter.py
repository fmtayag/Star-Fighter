# TODO list
# 1. (DONE) Make spawning animations for raider
# 2. (DONE) Finish implementing the raider enemy
# 3. (DONE) Implement the "Fatty" enemy
# 3.1 (DONE) Implement the "fireball" bullet. IT BOUNCES!
# 4. Make spawning animation / opening animation for player
# 5. Make start, game over, and high score screens
# 6. Add unique sound cues played on each monster's spawn animation

# Import libraries
try:
    import pygame, os, random, numpy, math
    from bullets import Laser, Fireball
    from monsters import Hellfighter, Raider, Fatty
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
spawn_delay = 1500
spawn_timer = pygame.time.get_ticks()
in_debugmode = True # For debugging 

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

# Classes =========================================================================
class Player(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.orient = "normal"
        self.lvls = ["cadet", "captain", "admiral"]
        self.cur_lvl = 0
        self.lvl = self.lvls[self.cur_lvl]
        self.surf = data["surface"]
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()
        self.images = data["images"]
        self.image = self.images[self.lvl][self.orient][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = data["coords"][0]
        self.rect.bottom = data["coords"][1]
        self.laser_img = data["laser_img"]
        self.laser_sfx = data["laser_sfx"]
        self.health = 100
        # Sprite groups
        self.spritegroups = data["sprite_groups"]
        self.sprites = self.spritegroups[0]
        self.p_lasers = self.spritegroups[1]
        # Speed
        self.movspd = 1
        self.maxspd = 5
        self.spdx = 0
        self.spdy = 0
        # Shooting
        self.shoot_delay = 250
        self.shoot_timer = pygame.time.get_ticks()
        # For animation
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        self.frame = 0
        # For collision detection
        self.radius = 16
        # For spawning animation
        self.spawn_imgs = data["spawn_imgs"] # TODO

    def update(self):
        # Reset ship's orientation
        self.orient = "normal"
 
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.spdy -= self.movspd
            self.spdy = numpy.clip(self.spdy, -self.maxspd, self.maxspd)
        if pressed[pygame.K_s]:
            self.spdy += self.movspd
            self.spdy = numpy.clip(self.spdy, -self.maxspd, self.maxspd)
        if pressed[pygame.K_a]:
            self.spdx -= self.movspd
            self.spdx = numpy.clip(self.spdx, -self.maxspd, self.maxspd)
            self.orient = "left"
        if pressed[pygame.K_d]:
            self.spdx += self.movspd
            self.spdx = numpy.clip(self.spdx, -self.maxspd, self.maxspd)
            self.orient = "right"
        if pressed[pygame.K_SPACE]:
            self.shoot()

        # Check if object collides with window bounds
        if self.rect.top < 0:
            self.spdy = 1
        elif self.rect.bottom > self.surf_h:
            self.spdy = -1
        elif self.rect.left < 0:
            self.spdx = 1
        elif self.rect.right > self.surf_w:
            self.spdx = -1

        # Animate the sprite
        self.animate()
        #self.draw_hp()

        # Move the object
        self.rect.x += self.spdx
        self.rect.y += self.spdy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            self.laser_sfx.play()
            if self.lvl == "cadet":
                l = Laser(self.surf, self.laser_img, self.rect.centerx,
                          self.rect.top-32, 0, -8)
                self.sprites.add(l)
                self.p_lasers.add(l)
            elif self.lvl == "captain":
                offset_x = [-13,13]
                speed_x = [-1,1]
                for i in range(2):
                    l = Laser(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
                              self.rect.top-32, speed_x[i], -8)
                    self.sprites.add(l)
                    self.p_lasers.add(l)
            elif self.lvl == "admiral":
                offset_x = [-13,0,13]
                offset_y = [-6,-32,-6]
                speed_x = [-1,0,1]
                for i in range(3):
                    l = Laser(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
                              self.rect.top+offset_y[i], speed_x[i], -8)
                    self.sprites.add(l)
                    self.p_lasers.add(l)

    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images[self.lvl][self.orient][self.frame]
            self.rect = self.image.get_rect()
            #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
            self.rect.x = old_rectx
            self.rect.y = old_recty

    def explode(self, explode_func, xpos, ypos):
        explode_func(xpos, ypos)

class Particle(pygame.sprite.Sprite):
    def __init__(self, image, xpos, ypos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.bottom = ypos
        self.lifetime = 100
        self.timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.timer > self.lifetime:
            self.kill()

class SpawnAnim(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = data["coords"][0]
        self.rect.y = data["coords"][1]
        self.spritegroups = data["spritegroups"]
        self.sprites = self.spritegroups[0]
        self.enemies = self.spritegroups[1]
        self.spawndata = data["spawndata"]
        self.spawnclass = data["spawnclass"]
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        self.frame = 0

    def update(self):
        self.animate()
        if self.frame == 3:
            spawn = self.spawnclass(self.spawndata)
            self.sprites.add(spawn)
            self.enemies.add(spawn)
            self.kill()
            
    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame == 4:
                self.frame = 0
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect()
            #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
            self.rect.x = old_rectx
            self.rect.y = old_recty

class Explosion(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.surface = data["surface"]
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = data["coords"][0]
        self.rect.bottom = data["coords"][1]
        # variables for animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        # Play the explosion sound effect
        data["explosion_sfx"].play()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1

            if self.frame == 4:
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

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
                "spawn_imgs": player_spawn_imgs }
player = Player(player_data)
sprites.add(player)

def spawn_hellfighter():
    # TODO: Clean up later
    hf_data = { "surface": window,
                 "images": hellfighter_imgs,
                 "coords": (random.randrange(64, WIDTH-64), random.randrange(0, 100)),
                 "spritegroups": (sprites, e_lasers),
                 "laser_img": e_laser_img,
                 "bullet": Laser}
    hf_spawn_data = { "images": hf_spawn_imgs,
                      "coords": hf_data["coords"],
                      "spritegroups": (sprites, enemies),
                      "spawndata": hf_data,
                      "spawnclass": Hellfighter}
    hf_spawn = SpawnAnim(hf_spawn_data)
    sprites.add(hf_spawn)

def spawn_raider():
    # TODO: Clean up later
    raider_data = { "surface": window,
                    "images": raider_imgs,
                    "coords": (player.rect.x, 0),
                    "spritegroups": (sprites)}
    raider_spawn_data = { "images": raider_spawn_imgs,
                          "coords": raider_data["coords"],
                          "spritegroups": (sprites, enemies),
                          "spawndata": raider_data,
                          "spawnclass": Raider}
    raider_spawn = SpawnAnim(raider_spawn_data)
    sprites.add(raider_spawn)

def spawn_fatty():
    # TODO: Clean up later
    fatty_data = { "surface": window,
                 "images": fatty_imgs,
                 "coords": (random.randrange(64, WIDTH-64), -64),
                 "spritegroups": (sprites, e_lasers),
                 "laser_img": fireball_img,
                 "bullet": Fireball}
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
        if limit >= 30: # Caps the limit at 15
            return 30
        else:
            return limit

def sd_subtractor(score):
    # Calculates the subtractor of the spawn delay (sd_s) based on score
    if score == 0:
        return 0
    else:
        sd_s = math.pow(score, 2)
        return numpy.clip(sd_s, 0, 500)
    
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
        hit.spdy = -3 # Knockback effect
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
            
        player.explode(spawn_explosion, player.rect.centerx, player.rect.bottom)

    # Check if the player collides with an enemy
    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        # Knockback effect.
        if player.rect.y < hit.rect.top:
            player.spdy -= 6
        else:
            player.spdy += 6
        hit.explode(spawn_explosion, hit.rect.centerx, hit.rect.bottom)
        player.explode(spawn_explosion, player.rect.centerx, player.rect.bottom)

    sprites.update()
    cur_fps = round(clock.get_fps(), 2)
    pygame.display.set_caption(f"Star Fighter (FPS: {cur_fps})")

    # Draw objects ================================================================
    window.fill(BLACK)
    sprites.draw(window)

    # Update the window
    pygame.display.flip()

# Quit pygame
pygame.quit()

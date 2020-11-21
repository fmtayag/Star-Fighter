# Import libraries
try:
    import pygame, os, random, numpy
    #from objects import Player
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
SPAWN_DELAY = 1500
spawn_timer = pygame.time.get_ticks()

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

# Add cadet player frames
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

# Add captain player frames
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

# Add admiral player frames
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

# Add hellfighter images
hellfighter_imgs = [
    load_png("hellfighter1.png", IMG_DIR, 4),
    load_png("hellfighter2.png", IMG_DIR, 4)
]

# Add hellfighter spawn images
hf_spawn_imgs = [
    load_png("hf_spawn1.png", IMG_DIR, 4),
    load_png("hf_spawn2.png", IMG_DIR, 4),
    load_png("hf_spawn3.png", IMG_DIR, 4),
    load_png("hf_spawn4.png", IMG_DIR, 4)
]

p_laser_img = load_png("laser_player.png", IMG_DIR, 4)
e_laser_img = load_png("laser_enemy.png", IMG_DIR, 4)
particle_img = load_png("particle.png", IMG_DIR, 2)

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

    def update(self):
        # Reset ship's orientation
        self.orient = "normal"
        #print(f"X: {self.spdx}, Y: {self.spdy}")
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
            if self.lvl == "cadet":
                l = Laser(self.surf, self.laser_img, self.rect.centerx,
                          self.rect.top-32, 0, -10)
                self.sprites.add(l)
                self.p_lasers.add(l)
            elif self.lvl == "captain":
                offset_x = [-13,13]
                speed_x = [-1,1]
                for i in range(2):
                    l = Laser(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
                              self.rect.top-32, speed_x[i], -10)
                    self.sprites.add(l)
                    self.p_lasers.add(l)
            elif self.lvl == "admiral":
                offset_x = [-13,0,13]
                offset_y = [-6,-32,-6]
                speed_x = [-1,0,1]
                for i in range(3):
                    l = Laser(self.surf, self.laser_img, self.rect.centerx+offset_x[i],
                              self.rect.top+offset_y[i], speed_x[i], -10)
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

class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, image, xpos, ypos, speedx, speedy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos
        self.spdx = speedx
        self.spdy = speedy
        self.surf = surface
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()

    def update(self):
        self.rect.x += self.spdx
        self.rect.y += self.spdy

        if (self.rect.bottom < 0 or
            self.rect.top > self.surf_h):
            self.kill()

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

class Hellfighter(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.surf = data["surface"]
        self.surf_w = self.surf.get_width()
        self.surf_h = self.surf.get_height()
        self.images = data["images"]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = data["coords"][0]
        self.rect.y = data["coords"][1]
        self.spritegroups = data["spritegroups"]
        self.sprites = self.spritegroups[0]
        self.e_lasers = self.spritegroups[1]
        self.laser_img = data["laser_img"]
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 100
        self.shoot_timer = random.randrange(50, 200)
        self.shoot_delay = 1000
        self.movspd = 3
        self.spdx = self.movspd

    def update(self):
        
        if self.rect.left < 0:
            self.spdx = self.movspd
        elif self.rect.right > self.surf_w:
            self.spdx = -self.movspd
        
        # Animate the object
        self.animate()
        self.shoot()

        self.rect.x += self.spdx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            l = Laser(self.surf, self.laser_img, self.rect.centerx,
                      self.rect.bottom, 0, 10)
            self.sprites.add(l)
            self.e_lasers.add(l)

    def animate(self):
        now = pygame.time.get_ticks()
        old_rectx = self.rect.x
        old_recty = self.rect.y
        if now - self.frame_timer > self.frame_delay:
            self.frame_timer = now
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect()
            #pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)
            self.rect.x = old_rectx
            self.rect.y = old_recty

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

# Initialize sprite groups
sprites = pygame.sprite.Group()
player = pygame.sprite.Group()
enemies = pygame.sprite.Group()
p_lasers = pygame.sprite.Group()
e_lasers = pygame.sprite.Group()

# Instantiate the player
player_data = { "surface": window,
                "images": player_imgs,
                "coords": (WIDTH/2, HEIGHT-20),
                "sprite_groups": (sprites, p_lasers),
                "laser_img": p_laser_img }
player = Player(player_data)
sprites.add(player)

# Instantiate a hellfighter
def spawn_hellfighter():
    hf_data = { "surface": window,
                 "images": hellfighter_imgs,
                 "coords": (random.randrange(0, 256), random.randrange(0, 256)),
                 "spritegroups": (sprites, e_lasers),
                 "laser_img": e_laser_img }
    hf_spawn_data = { "images": hf_spawn_imgs,
                      "coords": hf_data["coords"],
                      "spritegroups": (sprites, enemies),
                      "spawndata": hf_data,
                      "spawnclass": Hellfighter}
    hf_spawn = SpawnAnim(hf_spawn_data)
    sprites.add(hf_spawn)

# Game loop
while running:
    
    # Lock the FPS
    clock.tick(FPS)

    # Get input ===================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
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
    if now - spawn_timer > SPAWN_DELAY and len(enemies) < 3:
        spawn_timer = now
        spawn_hellfighter()

    pygame.sprite.groupcollide(p_lasers, enemies, True, True)
        
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

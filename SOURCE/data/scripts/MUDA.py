# The Mostly Useful Development Assemblage (MUDA)
# Version: 1.0.0
#   > Release date: March 12th 2021
# Just a collection of utility code to make development of games easier.
# Author: zyenapz
#   > Email: zyenapz@gmail.com
#   > Website: zyenapz.github.io
#   > GitHub: github.com/zyenapz
#   > Twitter: @zyenapz

import pygame, os, pickle

# SCENES & MANAGERS

class Scene():
    def __init__(self):
        pass
    
    def handle_events(self, events):
        raise NotImplementedError
    
    def update(self, dt):
        raise NotImplementedError

    def draw(self, window):
        raise NotImplementedError

class SceneManager():
    def __init__(self, InitScene):
        self.go_to(InitScene)

    def go_to(self, Scene):
        self.scene = Scene
        self.scene.manager = self

# SPRITE STATE MACHINES
class SpriteState():
    def __init__(self):
        pass

    def update(self, dt):
        raise NotImplementedError

class SpriteStateManager():
    def __init__(self, InitState):
        self.transition(InitState)

    def transition(self, State):
        self.state = State 
        self.state.manager = self

# ASSET LOADING / SAVING

def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

def load_img(file, directory, scale, convert_alpha=False):
    try:
        path = os.path.join(directory, file)
        if not convert_alpha:
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.image.load(path).convert()
            transColor = img.get_at((0,0))
            img.set_colorkey(transColor)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(f"ERROR loading {file}: {e}. Loading default texture instead.")
        s = pygame.Surface((32,32))
        s.fill('red')
        return s

def image_at(spritesheet, rectangle, convert_alpha=False):
    # Code stolen from the pygame wiki and modified for personal use. The boons of open source!
    rect = pygame.Rect(rectangle)
    if not convert_alpha:
        image = pygame.Surface(rect.size).convert()
        image.blit(spritesheet, (0,0), rect)
    else:
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(spritesheet, (0,0), rect)
        image.set_colorkey("BLACK")
    return image

def read_savedata(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            return data
        except EOFError:
            return list()

def write_savedata(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

# UTILITIES

def sort(arr):
    n = len(arr)

    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] < arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr

def slice_list(inlist, n):
    return [inlist[i:i+n] for i in range(0, len(inlist), n)]

def clamp(val, minim, maxim):
    if val < minim:
        return minim
    elif val > maxim:
        return maxim
    else:
        return val

def scale_rect(scale, rect):
    scaled = map((lambda x: x * scale), rect)
    return tuple(scaled)

# DRAWING

def draw_background(surf, img, img_rect, ypos):
    # Code from Paget Teaches
    surf_h = surf.get_height()
    rel_y = ypos % img_rect.height
    surf.blit(img, (0, rel_y - img_rect.height))

    if rel_y < surf_h:
        surf.blit(img, (0, rel_y))

def draw_text(surf, text, size, font, x, y, color, align="normal"):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "centered":
        text_rect.centerx = x
        text_rect.y = y
    elif align == "normal":
        text_rect.x = x
        text_rect.y = y
    surf.blit(text_surface, (text_rect.x, text_rect.y))

def draw_text2(surf, text, font, font_size, position, color, align="normal", italic=False):
    # Just a function with slightly better argument formatting and functionalities
    
    # Create Font object
    font = pygame.font.Font(font, font_size)

    # Italic settings
    if italic:
        font.italic = True
    
    # Create surface
    text_surface = font.render(text, True, color)
    
    # Find dest
    dest = [0,0]
    if align == "normal":
        dest[0] = position[0]
        dest[1] = position[1]
    elif align == "center":
        dest[0] = surf.get_width() / 2 - text_surface.get_width() / 2
        dest[1] = position[1]

    # Display text on surface
    surf.blit(text_surface, dest)

def shake(intensity, n):
    # Code from Sloth from StackOverflow
    shake = -1
    for _ in range(n):
        for x in range(0, intensity, 5):
            yield (x*shake, 0)
        for x in range(intensity, 0, 5):
            yield (x*shake, 0)
        shake *= -1
    while True:
        yield (0, 0)

def draw_hpbar(surf, bar_image, rect, hp_amnt, color):
    if hp_amnt < 0:
        hp_amnt = 0
    x = rect[0]
    y = rect[1]
    w = (hp_amnt * rect[2]) / 16
    h = rect[3] 
    img = pygame.Surface((w,h))
    img.blit(bar_image, (0,0))
    surf.blit(img, (x, y))